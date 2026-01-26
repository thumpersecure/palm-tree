#!/usr/bin/env python3
"""
Resource Throttling System - Be a good neighbor.

"With great power comes great responsibility to not crash Netflix."
    - Uncle Ben, if he was a sysadmin

This module provides bandwidth and CPU throttling to ensure Coconuts
doesn't interfere with your normal internet usage. Because what's the
point of privacy if you can't watch cat videos in peace?
"""

import asyncio
import time
import os
import sys
from dataclasses import dataclass, field
from typing import Optional, Callable, List, Dict
from datetime import datetime, timedelta
from collections import deque


@dataclass
class ResourceLimits:
    """
    Resource limits configuration.

    "These limits exist because past-you made bad decisions."
    """
    # Bandwidth limits
    max_bandwidth_kbps: int = 500       # Cap at 500 KB/s (leaves plenty for you)
    max_concurrent_requests: int = 5     # No connection flooding

    # CPU limits
    max_cpu_percent: int = 15            # Never exceed 15% CPU
    use_nice: bool = True                # Use nice for low priority

    # Network scheduling
    use_low_priority: bool = True        # Low priority traffic

    # Auto-throttle based on user activity
    yield_to_user: bool = True           # Pause when user is active
    user_activity_threshold: float = 0.7  # If network is 70%+ busy, back off

    # Request rate limiting
    min_request_interval: float = 0.5    # Minimum 500ms between requests
    burst_limit: int = 10                # Max requests in a burst
    burst_window: float = 10.0           # Burst window in seconds


class BandwidthMonitor:
    """
    Monitors bandwidth usage and provides throttling.

    "Counting bytes so you don't have to count complaints
    from your housemates."
    """

    def __init__(self, max_kbps: int = 500, window_seconds: float = 1.0):
        """
        Initialize the bandwidth monitor.

        Args:
            max_kbps: Maximum kilobytes per second
            window_seconds: Window for calculating bandwidth
        """
        self.max_kbps = max_kbps
        self.max_bytes_per_window = (max_kbps * 1024) * window_seconds
        self.window_seconds = window_seconds

        # Track bytes transferred in sliding window
        self.transfer_log: deque = deque()
        self.total_bytes = 0

    def record_transfer(self, bytes_count: int) -> None:
        """Record a data transfer."""
        now = time.time()
        self.transfer_log.append((now, bytes_count))
        self.total_bytes += bytes_count

        # Clean old entries
        self._cleanup_old_entries(now)

    def _cleanup_old_entries(self, now: float) -> None:
        """Remove entries outside the window."""
        cutoff = now - self.window_seconds
        while self.transfer_log and self.transfer_log[0][0] < cutoff:
            self.transfer_log.popleft()

    def get_current_bandwidth(self) -> float:
        """Get current bandwidth usage in KB/s."""
        now = time.time()
        self._cleanup_old_entries(now)

        if not self.transfer_log:
            return 0.0

        total_bytes = sum(b for _, b in self.transfer_log)
        elapsed = now - self.transfer_log[0][0] if self.transfer_log else self.window_seconds

        if elapsed > 0:
            return (total_bytes / 1024) / elapsed  # KB/s
        return 0.0

    def should_throttle(self) -> bool:
        """Check if we should slow down."""
        return self.get_current_bandwidth() > self.max_kbps * 0.9

    async def wait_for_bandwidth(self) -> None:
        """Wait until bandwidth is available."""
        while self.should_throttle():
            await asyncio.sleep(0.1)

    def get_delay_for_transfer(self, bytes_count: int) -> float:
        """Calculate delay needed before a transfer."""
        current_rate = self.get_current_bandwidth()

        if current_rate <= 0:
            return 0.0

        # If we're at or above limit, calculate wait time
        if current_rate >= self.max_kbps:
            # Wait for enough bandwidth to free up
            return (bytes_count / 1024) / self.max_kbps

        return 0.0


class RateLimiter:
    """
    Rate limiter for controlling request frequency.

    "Slow and steady wins the race.
    Also doesn't get IP banned."
    """

    def __init__(
        self,
        min_interval: float = 0.5,
        burst_limit: int = 10,
        burst_window: float = 10.0
    ):
        """
        Initialize the rate limiter.

        Args:
            min_interval: Minimum seconds between requests
            burst_limit: Maximum requests allowed in burst_window
            burst_window: Time window for burst limiting
        """
        self.min_interval = min_interval
        self.burst_limit = burst_limit
        self.burst_window = burst_window

        self.last_request_time = 0.0
        self.request_times: deque = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        async with self._lock:
            now = time.time()

            # Check minimum interval
            time_since_last = now - self.last_request_time
            if time_since_last < self.min_interval:
                await asyncio.sleep(self.min_interval - time_since_last)
                now = time.time()

            # Check burst limit
            self._cleanup_old_requests(now)
            while len(self.request_times) >= self.burst_limit:
                # Wait for oldest request to expire from window
                wait_time = self.request_times[0] + self.burst_window - now
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                now = time.time()
                self._cleanup_old_requests(now)

            # Record this request
            self.request_times.append(now)
            self.last_request_time = now

    def _cleanup_old_requests(self, now: float) -> None:
        """Remove requests outside the burst window."""
        cutoff = now - self.burst_window
        while self.request_times and self.request_times[0] < cutoff:
            self.request_times.popleft()


class UserActivityDetector:
    """
    Detects if the user is actively using the network.

    "Being a good roommate means not hogging the WiFi
    when someone's trying to have a Zoom call."

    This is a best-effort detector - it monitors network
    activity that isn't from our tool.
    """

    def __init__(self, threshold: float = 0.7, sample_interval: float = 1.0):
        """
        Initialize the activity detector.

        Args:
            threshold: Network utilization threshold (0.0-1.0) that indicates user activity
            sample_interval: How often to check (seconds)
        """
        self.threshold = threshold
        self.sample_interval = sample_interval
        self.our_bytes = 0
        self._last_check = time.time()
        self._network_baseline: Optional[Dict] = None

    def record_our_transfer(self, bytes_count: int) -> None:
        """Record bytes transferred by our tool."""
        self.our_bytes += bytes_count

    def is_user_active(self) -> bool:
        """
        Check if the user appears to be actively using the network.

        This is a simplified heuristic - we check if there's been
        significant network activity beyond what we've generated.
        """
        # Try to get network stats (Linux-specific)
        try:
            net_stats = self._get_network_stats()
            if net_stats and self._network_baseline:
                # Calculate total network activity since last check
                total_rx = net_stats.get('rx', 0) - self._network_baseline.get('rx', 0)
                total_tx = net_stats.get('tx', 0) - self._network_baseline.get('tx', 0)

                # If total activity is much higher than ours, user is active
                total_activity = total_rx + total_tx
                if total_activity > 0:
                    our_ratio = self.our_bytes / total_activity
                    return our_ratio < (1 - self.threshold)

            self._network_baseline = net_stats
            self.our_bytes = 0

        except Exception:
            pass

        # Default to not active (don't throttle unnecessarily)
        return False

    def _get_network_stats(self) -> Optional[Dict]:
        """Get network statistics (Linux only)."""
        try:
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()

            total_rx = 0
            total_tx = 0

            for line in lines[2:]:  # Skip headers
                parts = line.split()
                if len(parts) >= 10:
                    # Skip loopback
                    if parts[0].startswith('lo'):
                        continue
                    total_rx += int(parts[1])
                    total_tx += int(parts[9])

            return {'rx': total_rx, 'tx': total_tx}

        except Exception:
            return None


class ThrottledClient:
    """
    HTTP client wrapper with built-in throttling.

    "The responsible way to generate traffic noise."
    """

    def __init__(
        self,
        limits: Optional[ResourceLimits] = None,
        httpx_client: Optional[object] = None
    ):
        """
        Initialize the throttled client.

        Args:
            limits: Resource limits configuration
            httpx_client: Optional httpx.AsyncClient to wrap
        """
        self.limits = limits or ResourceLimits()

        # Initialize components
        self.bandwidth_monitor = BandwidthMonitor(self.limits.max_bandwidth_kbps)
        self.rate_limiter = RateLimiter(
            min_interval=self.limits.min_request_interval,
            burst_limit=self.limits.burst_limit,
            burst_window=self.limits.burst_window
        )
        self.activity_detector = UserActivityDetector(
            threshold=self.limits.user_activity_threshold
        ) if self.limits.yield_to_user else None

        self._client = httpx_client
        self.stats = {
            "requests": 0,
            "bytes_transferred": 0,
            "throttle_events": 0,
            "user_yield_events": 0,
        }

    async def _ensure_client(self):
        """Ensure httpx client exists."""
        if self._client is None:
            try:
                import httpx
                self._client = httpx.AsyncClient(timeout=30.0)
            except ImportError:
                raise ImportError("httpx is required. Install with: pip install httpx")

    async def fetch(self, url: str, **kwargs) -> Optional[object]:
        """
        Fetch a URL with throttling.

        Args:
            url: URL to fetch
            **kwargs: Additional arguments for httpx

        Returns:
            Response object or None on failure
        """
        await self._ensure_client()

        # Check user activity
        if self.activity_detector and self.activity_detector.is_user_active():
            self.stats["user_yield_events"] += 1
            # Back off significantly
            await asyncio.sleep(5.0)

        # Rate limit
        await self.rate_limiter.acquire()

        # Bandwidth check
        if self.bandwidth_monitor.should_throttle():
            self.stats["throttle_events"] += 1
            await self.bandwidth_monitor.wait_for_bandwidth()

        # Make request
        try:
            response = await self._client.get(url, **kwargs)

            # Record transfer
            content_length = len(response.content) if hasattr(response, 'content') else 0
            self.bandwidth_monitor.record_transfer(content_length)
            if self.activity_detector:
                self.activity_detector.record_our_transfer(content_length)

            self.stats["requests"] += 1
            self.stats["bytes_transferred"] += content_length

            return response

        except Exception as e:
            return None

    async def close(self):
        """Close the client."""
        if self._client:
            await self._client.aclose()

    def get_stats(self) -> Dict:
        """Get usage statistics."""
        return {
            **self.stats,
            "current_bandwidth_kbps": self.bandwidth_monitor.get_current_bandwidth(),
        }


def apply_nice_priority() -> bool:
    """
    Apply nice priority to the current process.

    "Making ourselves as unimportant as possible,
    just like in high school."
    """
    try:
        # Set nice value to maximum (lowest priority)
        os.nice(19)
        return True
    except Exception:
        return False


def apply_io_priority() -> bool:
    """
    Apply I/O priority (Linux only).

    "Idle I/O priority - we only do work when no one else wants to."
    """
    try:
        # Set I/O class to idle (3)
        import subprocess
        pid = os.getpid()
        subprocess.run(['ionice', '-c', '3', '-p', str(pid)], capture_output=True)
        return True
    except Exception:
        return False


# For testing
if __name__ == "__main__":
    async def test():
        print("Testing Throttling System...")
        print("=" * 50)

        limits = ResourceLimits(
            max_bandwidth_kbps=100,  # 100 KB/s for testing
            max_concurrent_requests=3,
            min_request_interval=1.0,
        )

        client = ThrottledClient(limits=limits)

        print(f"\nLimits:")
        print(f"  Max bandwidth: {limits.max_bandwidth_kbps} KB/s")
        print(f"  Min interval: {limits.min_request_interval}s")

        # Test with a few requests
        test_urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/headers",
            "https://httpbin.org/ip",
        ]

        print("\nMaking throttled requests...")
        for url in test_urls:
            start = time.time()
            response = await client.fetch(url)
            elapsed = time.time() - start
            if response:
                print(f"  {url}: {response.status_code} ({elapsed:.2f}s)")
            else:
                print(f"  {url}: Failed")

        print(f"\nStats: {client.get_stats()}")
        await client.close()

    asyncio.run(test())
