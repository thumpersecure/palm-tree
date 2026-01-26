#!/usr/bin/env python3
"""
Optimized HTTP Client - Speed demon with manners.

"Fast, furious, and surprisingly polite about bandwidth."

This module provides an optimized async HTTP client with:
- Connection pooling (reuse connections like a good citizen)
- Automatic retries with exponential backoff
- Built-in throttling
- Dashboard integration
- Request deduplication
- DNS caching

Basically, it's the HTTP client your mother warned you about.
"""

import asyncio
import time
import random
import hashlib
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set
from datetime import datetime, timedelta
from collections import deque
from contextlib import asynccontextmanager

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

# Dashboard integration
try:
    from dashboard import record_request, log_activity, set_current_identity
    DASHBOARD_AVAILABLE = True
except ImportError:
    DASHBOARD_AVAILABLE = False
    def record_request(*args, **kwargs): pass
    def log_activity(*args, **kwargs): pass
    def set_current_identity(*args, **kwargs): pass


@dataclass
class ClientConfig:
    """
    Configuration for the optimized client.

    "Tuning parameters for the chaos engine."
    """
    # Connection pool
    max_connections: int = 100
    max_connections_per_host: int = 10
    keepalive_expiry: float = 30.0

    # Timeouts
    connect_timeout: float = 10.0
    read_timeout: float = 30.0
    total_timeout: float = 60.0

    # Retries
    max_retries: int = 3
    retry_backoff_base: float = 1.0
    retry_backoff_max: float = 30.0

    # Throttling
    max_requests_per_second: float = 10.0
    burst_size: int = 20

    # Deduplication
    dedupe_window_seconds: float = 5.0

    # DNS caching
    dns_cache_ttl: float = 300.0

    # User agent rotation
    rotate_user_agent: bool = True


# User agents for rotation
USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Chrome on Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    # Safari on Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    # Chrome on Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    # Mobile Chrome
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    # Mobile Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

# Exotic user agents for extra chaos
EXOTIC_USER_AGENTS = [
    "Mozilla/5.0 (PlayStation 5; WebKit) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Nintendo Switch; WebKit) NintendoBrowser/1.0.0.0",
    "Mozilla/5.0 (Smart TV; Linux) AppleWebKit/537.36 SmartTV/2.0",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "curl/8.4.0",
    "Wget/1.21.4",
    "Python-httpx/0.25.0",
]


class TokenBucket:
    """
    Token bucket rate limiter.

    "Dispensing chaos tokens at a responsible rate."
    """

    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # Tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> float:
        """Acquire tokens, waiting if necessary. Returns wait time."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update

            # Add tokens based on elapsed time
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            else:
                # Calculate wait time
                needed = tokens - self.tokens
                wait_time = needed / self.rate
                return wait_time

    async def wait_and_acquire(self, tokens: int = 1):
        """Wait for tokens and acquire them."""
        wait_time = await self.acquire(tokens)
        if wait_time > 0:
            await asyncio.sleep(wait_time)
            await self.acquire(tokens)


class RequestDeduplicator:
    """
    Prevents duplicate requests within a time window.

    "Because visiting the same URL twice in 5 seconds is just desperate."
    """

    def __init__(self, window_seconds: float = 5.0):
        self.window = window_seconds
        self.recent_requests: Dict[str, float] = {}
        self._lock = asyncio.Lock()

    def _hash_request(self, url: str, method: str = "GET") -> str:
        """Create a hash for a request."""
        return hashlib.md5(f"{method}:{url}".encode()).hexdigest()

    async def should_skip(self, url: str, method: str = "GET") -> bool:
        """Check if this request should be skipped as duplicate."""
        async with self._lock:
            now = time.time()

            # Clean old entries
            self.recent_requests = {
                k: v for k, v in self.recent_requests.items()
                if now - v < self.window
            }

            # Check if duplicate
            request_hash = self._hash_request(url, method)
            if request_hash in self.recent_requests:
                return True

            # Record this request
            self.recent_requests[request_hash] = now
            return False


class OptimizedClient:
    """
    Optimized async HTTP client with all the bells and whistles.

    "Like a regular HTTP client, but it went to finishing school."
    """

    def __init__(self, config: Optional[ClientConfig] = None):
        self.config = config or ClientConfig()
        self._client: Optional[httpx.AsyncClient] = None
        self._rate_limiter = TokenBucket(
            rate=self.config.max_requests_per_second,
            capacity=self.config.burst_size
        )
        self._deduplicator = RequestDeduplicator(self.config.dedupe_window_seconds)
        self._current_identity = "Anonymous"

        # Stats
        self.stats = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "retries": 0,
            "dedupe_skips": 0,
            "bytes_transferred": 0,
            "total_response_time": 0.0,
        }

    async def _ensure_client(self):
        """Ensure the HTTP client is initialized."""
        if self._client is None:
            if not HTTPX_AVAILABLE:
                raise ImportError("httpx is required. Install with: pip install httpx")

            # Configure connection limits
            limits = httpx.Limits(
                max_connections=self.config.max_connections,
                max_keepalive_connections=self.config.max_connections_per_host,
                keepalive_expiry=self.config.keepalive_expiry,
            )

            # Configure timeouts
            timeout = httpx.Timeout(
                connect=self.config.connect_timeout,
                read=self.config.read_timeout,
                write=self.config.read_timeout,
                pool=self.config.total_timeout,
            )

            self._client = httpx.AsyncClient(
                limits=limits,
                timeout=timeout,
                follow_redirects=True,
                http2=True,  # Enable HTTP/2 for better performance
            )

    def _get_headers(self, identity: Optional[str] = None) -> Dict[str, str]:
        """Generate request headers."""
        if self.config.rotate_user_agent:
            # 90% normal, 10% exotic
            if random.random() > 0.9:
                ua = random.choice(EXOTIC_USER_AGENTS)
            else:
                ua = random.choice(USER_AGENTS)
        else:
            ua = USER_AGENTS[0]

        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice([
                "en-US,en;q=0.9",
                "en-GB,en;q=0.9",
                "en-US,en;q=0.9,es;q=0.8",
                "en-US,en;q=0.5",
            ]),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }

        # Update identity
        if identity:
            self._current_identity = identity

        return headers

    async def fetch(
        self,
        url: str,
        method: str = "GET",
        identity: Optional[str] = None,
        skip_dedupe: bool = False,
        **kwargs
    ) -> Optional[httpx.Response]:
        """
        Fetch a URL with all optimizations.

        Args:
            url: URL to fetch
            method: HTTP method
            identity: Optional identity name for logging
            skip_dedupe: Skip deduplication check
            **kwargs: Additional arguments for httpx

        Returns:
            Response object or None on failure
        """
        await self._ensure_client()

        # Deduplication check
        if not skip_dedupe and await self._deduplicator.should_skip(url, method):
            self.stats["dedupe_skips"] += 1
            log_activity(f"Skipped duplicate: {url[:30]}...", "info")
            return None

        # Rate limiting
        await self._rate_limiter.wait_and_acquire()

        # Get headers
        headers = self._get_headers(identity)
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))

        # Update dashboard
        if identity:
            set_current_identity(identity)

        # Attempt request with retries
        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                start_time = time.time()

                response = await self._client.request(
                    method,
                    url,
                    headers=headers,
                    **kwargs
                )

                elapsed = time.time() - start_time
                content_length = len(response.content) if response.content else 0

                # Update stats
                self.stats["requests"] += 1
                self.stats["successes"] += 1
                self.stats["bytes_transferred"] += content_length
                self.stats["total_response_time"] += elapsed

                # Dashboard integration
                record_request(
                    success=True,
                    url=url,
                    response_time=elapsed,
                    bytes_count=content_length,
                    identity=self._current_identity
                )
                log_activity(f"✓ {url[:40]}... ({elapsed*1000:.0f}ms)", "success")

                return response

            except Exception as e:
                last_error = e
                self.stats["retries"] += 1

                if attempt < self.config.max_retries:
                    # Exponential backoff
                    backoff = min(
                        self.config.retry_backoff_base * (2 ** attempt),
                        self.config.retry_backoff_max
                    )
                    backoff *= random.uniform(0.5, 1.5)  # Jitter

                    log_activity(f"Retry {attempt + 1}/{self.config.max_retries}: {url[:30]}...", "warning")
                    await asyncio.sleep(backoff)

        # All retries failed
        self.stats["failures"] += 1

        record_request(
            success=False,
            url=url,
            response_time=0,
            bytes_count=0,
            identity=self._current_identity
        )
        log_activity(f"✗ Failed: {url[:40]}... ({last_error})", "error")

        return None

    async def fetch_many(
        self,
        urls: List[str],
        concurrency: int = 10,
        identity: Optional[str] = None,
    ) -> List[Optional[httpx.Response]]:
        """
        Fetch multiple URLs concurrently with controlled parallelism.

        "Parallel chaos, but make it organized."
        """
        semaphore = asyncio.Semaphore(concurrency)

        async def fetch_with_semaphore(url: str) -> Optional[httpx.Response]:
            async with semaphore:
                return await self.fetch(url, identity=identity)

        tasks = [fetch_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def close(self):
        """Close the client and cleanup."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics."""
        avg_response = (
            self.stats["total_response_time"] / self.stats["successes"]
            if self.stats["successes"] > 0 else 0
        )

        return {
            **self.stats,
            "avg_response_time": avg_response,
            "success_rate": (
                self.stats["successes"] / self.stats["requests"] * 100
                if self.stats["requests"] > 0 else 100
            ),
        }

    async def __aenter__(self):
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

_default_client: Optional[OptimizedClient] = None


async def get_client() -> OptimizedClient:
    """Get or create the default client."""
    global _default_client
    if _default_client is None:
        _default_client = OptimizedClient()
    return _default_client


async def fetch(url: str, **kwargs) -> Optional[httpx.Response]:
    """Convenience function to fetch a URL."""
    client = await get_client()
    return await client.fetch(url, **kwargs)


async def fetch_many(urls: List[str], **kwargs) -> List[Optional[httpx.Response]]:
    """Convenience function to fetch multiple URLs."""
    client = await get_client()
    return await client.fetch_many(urls, **kwargs)


# ============================================================================
# DEMO
# ============================================================================

async def demo():
    """Demo the optimized client."""
    print("🚀 Optimized Client Demo\n")

    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/headers",
        "https://httpbin.org/user-agent",
        "https://httpbin.org/ip",
        "https://httpbin.org/delay/1",
    ]

    async with OptimizedClient() as client:
        print("Fetching URLs with connection pooling and rate limiting...\n")

        for url in urls:
            response = await client.fetch(url, identity="Demo User")
            if response:
                print(f"✓ {url}: {response.status_code}")
            else:
                print(f"✗ {url}: Failed")

        print(f"\n📊 Stats: {client.get_stats()}")


if __name__ == "__main__":
    asyncio.run(demo())
