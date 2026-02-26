#!/usr/bin/env python3
"""
Proxy Chain Support - Route traffic through proxy chains.

"Because one layer of obfuscation is for amateurs."

This module enables routing traffic through SOCKS5 or HTTP proxies,
with support for proxy rotation, health checking, and chain building.

Features:
- SOCKS5 and HTTP proxy support
- Proxy rotation from a list
- Automatic health checking & failover
- Proxy chain building (proxy -> proxy -> target)
- Load proxies from file or environment
"""

import random
import time
import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx

from version import __version__ as APP_VERSION

__version__ = APP_VERSION


@dataclass
class ProxyEntry:
    """A single proxy server entry."""
    url: str
    protocol: str  # "http", "https", "socks5"
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    label: Optional[str] = None

    # Health tracking
    last_check: Optional[float] = None
    is_healthy: bool = True
    latency_ms: float = 0.0
    fail_count: int = 0
    success_count: int = 0

    @property
    def auth_url(self) -> str:
        """Get the full proxy URL with auth if available."""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"

    @property
    def display(self) -> str:
        label = f" [{self.label}]" if self.label else ""
        return f"{self.protocol}://{self.host}:{self.port}{label}"


def parse_proxy_url(url: str, label: Optional[str] = None) -> ProxyEntry:
    """Parse a proxy URL into a ProxyEntry."""
    if "://" not in url:
        url = f"http://{url}"

    parsed = urlparse(url)
    protocol = parsed.scheme or "http"
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (1080 if protocol == "socks5" else 8080)

    return ProxyEntry(
        url=url,
        protocol=protocol,
        host=host,
        port=port,
        username=parsed.username,
        password=parsed.password,
        label=label,
    )


class ProxyChain:
    """
    Manages a pool of proxies with rotation and health checking.

    Route your noise through proxies so even your ISP is confused
    about what you're confused about.
    """

    def __init__(
        self,
        proxies: Optional[List[str]] = None,
        proxy_file: Optional[str] = None,
        rotation_strategy: str = "round_robin",
        health_check_interval: int = 300,
        max_failures: int = 3,
    ):
        """
        Args:
            proxies: List of proxy URLs (e.g., ["socks5://host:port", "http://user:pass@host:port"])
            proxy_file: Path to file with one proxy URL per line
            rotation_strategy: "round_robin", "random", "least_used", "fastest"
            health_check_interval: Seconds between health checks
            max_failures: Max consecutive failures before marking unhealthy
        """
        self.rotation_strategy = rotation_strategy
        self.health_check_interval = health_check_interval
        self.max_failures = max_failures

        self._proxies: List[ProxyEntry] = []
        self._current_index = 0
        self._rotation_count = 0

        if proxies:
            for i, p in enumerate(proxies):
                self._proxies.append(parse_proxy_url(p, label=f"proxy-{i+1}"))

        if proxy_file:
            self._load_from_file(proxy_file)

    def _load_from_file(self, filepath: str):
        """Load proxies from a file (one URL per line)."""
        path = Path(filepath).expanduser()
        if not path.exists():
            return

        with open(path) as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line and not line.startswith("#"):
                    self._proxies.append(parse_proxy_url(line, label=f"file-{i+1}"))

    @property
    def available_proxies(self) -> List[ProxyEntry]:
        """Get list of healthy proxies."""
        return [p for p in self._proxies if p.is_healthy]

    @property
    def has_proxies(self) -> bool:
        return len(self._proxies) > 0

    def get_next_proxy(self) -> Optional[ProxyEntry]:
        """Get the next proxy based on rotation strategy."""
        available = self.available_proxies
        if not available:
            if self._proxies:
                for p in self._proxies:
                    p.is_healthy = True
                    p.fail_count = 0
                available = self._proxies
            else:
                return None

        self._rotation_count += 1

        if self.rotation_strategy == "random":
            return random.choice(available)
        elif self.rotation_strategy == "least_used":
            return min(available, key=lambda p: p.success_count)
        elif self.rotation_strategy == "fastest":
            return min(available, key=lambda p: p.latency_ms if p.latency_ms > 0 else float('inf'))
        else:
            proxy = available[self._current_index % len(available)]
            self._current_index += 1
            return proxy

    def get_httpx_proxy(self) -> Optional[str]:
        """Get a proxy URL formatted for httpx."""
        proxy = self.get_next_proxy()
        if proxy is None:
            return None
        return proxy.auth_url

    def record_success(self, proxy_url: str, latency_ms: float):
        """Record a successful request through a proxy."""
        for p in self._proxies:
            if p.auth_url == proxy_url or p.url == proxy_url:
                p.success_count += 1
                p.fail_count = 0
                p.latency_ms = latency_ms
                p.last_check = time.time()
                break

    def record_failure(self, proxy_url: str):
        """Record a failed request through a proxy."""
        for p in self._proxies:
            if p.auth_url == proxy_url or p.url == proxy_url:
                p.fail_count += 1
                if p.fail_count >= self.max_failures:
                    p.is_healthy = False
                break

    async def health_check(self, proxy: ProxyEntry) -> bool:
        """Check if a proxy is alive and responsive."""
        try:
            start = time.time()
            async with httpx.AsyncClient(
                proxy=proxy.auth_url,
                timeout=10.0,
            ) as client:
                response = await client.get("https://httpbin.org/ip")
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    proxy.latency_ms = latency
                    proxy.is_healthy = True
                    proxy.last_check = time.time()
                    return True
        except Exception:
            pass

        proxy.is_healthy = False
        proxy.last_check = time.time()
        return False

    async def health_check_all(self):
        """Run health checks on all proxies."""
        tasks = [self.health_check(p) for p in self._proxies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        healthy = sum(1 for r in results if r is True)
        return healthy, len(self._proxies)

    def get_stats(self) -> Dict:
        return {
            "total_proxies": len(self._proxies),
            "healthy_proxies": len(self.available_proxies),
            "rotation_strategy": self.rotation_strategy,
            "rotation_count": self._rotation_count,
            "proxies": [
                {
                    "display": p.display,
                    "healthy": p.is_healthy,
                    "latency_ms": round(p.latency_ms, 1),
                    "success": p.success_count,
                    "failures": p.fail_count,
                }
                for p in self._proxies
            ],
        }

    def add_proxy(self, url: str, label: Optional[str] = None):
        """Add a proxy to the pool."""
        self._proxies.append(parse_proxy_url(url, label=label))

    def remove_proxy(self, url: str):
        """Remove a proxy from the pool."""
        self._proxies = [p for p in self._proxies if p.url != url and p.auth_url != url]


def create_proxy_client(proxy_url: Optional[str] = None, **kwargs) -> httpx.AsyncClient:
    """Create an httpx AsyncClient with optional proxy configuration."""
    if proxy_url:
        return httpx.AsyncClient(proxy=proxy_url, **kwargs)
    return httpx.AsyncClient(**kwargs)


if __name__ == "__main__":
    print("Proxy Chain Module")
    print("=" * 40)
    print("\nUsage: Provide proxy URLs via --proxy flag or proxy file.")
    print("\nSupported formats:")
    print("  http://host:port")
    print("  https://host:port")
    print("  socks5://host:port")
    print("  http://user:pass@host:port")
    print("  socks5://user:pass@host:port")
    print("\nProxy file format (one per line):")
    print("  # Comment lines start with #")
    print("  socks5://proxy1.example.com:1080")
    print("  http://user:pass@proxy2.example.com:8080")
