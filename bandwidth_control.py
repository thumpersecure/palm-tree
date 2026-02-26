#!/usr/bin/env python3
"""
Bandwidth Control - Intelligent traffic throttling.

"Generate noise, not a DDoS against yourself."

This module provides adaptive bandwidth management so the traffic
generator doesn't nuke your Netflix streaming or video calls.
It monitors throughput and backs off intelligently.

Features:
- Hard bandwidth cap (KB/s)
- Adaptive mode: detects high usage and backs off
- Time-based profiles: less bandwidth during work hours
- Per-worker rate limiting
- Burst allowance with token bucket algorithm
"""

import time
import asyncio
import math
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime
from collections import deque
from threading import Lock

from version import __version__ as APP_VERSION

__version__ = APP_VERSION


@dataclass
class BandwidthProfile:
    """Bandwidth limit profile for a time period."""
    name: str
    max_kbps: int
    max_requests_per_minute: int
    burst_allowance: int
    description: str


BANDWIDTH_PROFILES: Dict[str, BandwidthProfile] = {
    "unlimited": BandwidthProfile(
        name="Unlimited",
        max_kbps=0,
        max_requests_per_minute=0,
        burst_allowance=0,
        description="No limits. Full speed ahead.",
    ),
    "conservative": BandwidthProfile(
        name="Conservative",
        max_kbps=100,
        max_requests_per_minute=30,
        burst_allowance=5,
        description="Gentle on your network. Good for shared connections.",
    ),
    "moderate": BandwidthProfile(
        name="Moderate",
        max_kbps=500,
        max_requests_per_minute=60,
        burst_allowance=10,
        description="Balanced noise generation. Recommended default.",
    ),
    "aggressive": BandwidthProfile(
        name="Aggressive",
        max_kbps=2000,
        max_requests_per_minute=120,
        burst_allowance=20,
        description="Heavy traffic. Use on dedicated connections.",
    ),
    "stealth": BandwidthProfile(
        name="Stealth",
        max_kbps=50,
        max_requests_per_minute=15,
        burst_allowance=3,
        description="Minimal footprint. Barely detectable.",
    ),
}


class TokenBucket:
    """
    Token bucket rate limiter.

    Allows bursts up to a limit while maintaining a steady average rate.
    """

    def __init__(self, rate: float, capacity: int):
        """
        Args:
            rate: Tokens per second to refill
            capacity: Maximum tokens (burst limit)
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = float(capacity)
        self._last_refill = time.monotonic()
        self._lock = Lock()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self._last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if allowed."""
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    async def wait_for_token(self, tokens: int = 1):
        """Wait until tokens are available."""
        while not self.consume(tokens):
            wait_time = (tokens - self.tokens) / self.rate if self.rate > 0 else 1.0
            await asyncio.sleep(min(wait_time, 1.0))


class BandwidthController:
    """
    Intelligent bandwidth management for traffic generation.

    Tracks usage, enforces limits, and adapts based on conditions.
    """

    def __init__(
        self,
        profile: str = "moderate",
        max_kbps: Optional[int] = None,
        max_rpm: Optional[int] = None,
        adaptive: bool = True,
    ):
        """
        Args:
            profile: Named bandwidth profile to use
            max_kbps: Override max KB/s (0 = unlimited)
            max_rpm: Override max requests per minute (0 = unlimited)
            adaptive: Enable adaptive throttling based on time of day
        """
        prof = BANDWIDTH_PROFILES.get(profile, BANDWIDTH_PROFILES["moderate"])

        self.max_kbps = max_kbps if max_kbps is not None else prof.max_kbps
        self.max_rpm = max_rpm if max_rpm is not None else prof.max_requests_per_minute
        self.burst_allowance = prof.burst_allowance
        self.adaptive = adaptive
        self.profile_name = prof.name

        if self.max_rpm > 0:
            rate = self.max_rpm / 60.0
            self._request_bucket = TokenBucket(rate=rate, capacity=self.burst_allowance or int(rate * 5))
        else:
            self._request_bucket = None

        if self.max_kbps > 0:
            self._bandwidth_bucket = TokenBucket(rate=self.max_kbps, capacity=self.max_kbps * 5)
        else:
            self._bandwidth_bucket = None

        self._bytes_history: deque = deque(maxlen=600)
        self._request_history: deque = deque(maxlen=600)
        self._lock = Lock()

        self.total_bytes = 0
        self.total_requests = 0
        self.throttle_events = 0

    def _get_adaptive_multiplier(self) -> float:
        """Adjust limits based on time of day."""
        if not self.adaptive:
            return 1.0

        hour = datetime.now().hour
        day = datetime.now().weekday()

        if day >= 5:
            return 1.2

        if 9 <= hour < 17:
            return 0.6
        elif 17 <= hour < 22:
            return 0.8
        elif 22 <= hour or hour < 6:
            return 1.5
        else:
            return 1.0

    async def acquire(self, estimated_bytes: int = 5000):
        """
        Acquire permission to make a request.

        Blocks until bandwidth is available within limits.
        """
        if self._request_bucket:
            await self._request_bucket.wait_for_token(1)

        if self._bandwidth_bucket:
            kb_needed = max(1, estimated_bytes // 1024)
            multiplier = self._get_adaptive_multiplier()
            adjusted_kb = max(1, int(kb_needed / multiplier))
            await self._bandwidth_bucket.wait_for_token(adjusted_kb)

    def record(self, bytes_transferred: int):
        """Record completed transfer."""
        with self._lock:
            now = time.time()
            self._bytes_history.append((now, bytes_transferred))
            self._request_history.append(now)
            self.total_bytes += bytes_transferred
            self.total_requests += 1

    def get_current_rate(self) -> Dict[str, float]:
        """Get current transfer rates."""
        now = time.time()
        one_minute_ago = now - 60

        with self._lock:
            recent_bytes = sum(b for t, b in self._bytes_history if t > one_minute_ago)
            recent_requests = sum(1 for t in self._request_history if t > one_minute_ago)

        return {
            "kbps": recent_bytes / 1024 / 60 if recent_bytes else 0,
            "rpm": recent_requests,
            "total_mb": self.total_bytes / (1024 * 1024),
            "total_requests": self.total_requests,
        }

    def get_stats(self) -> Dict:
        rates = self.get_current_rate()
        return {
            "profile": self.profile_name,
            "max_kbps": self.max_kbps,
            "max_rpm": self.max_rpm,
            "adaptive": self.adaptive,
            "adaptive_multiplier": self._get_adaptive_multiplier(),
            "current_kbps": round(rates["kbps"], 2),
            "current_rpm": rates["rpm"],
            "total_mb": round(rates["total_mb"], 2),
            "total_requests": rates["total_requests"],
            "throttle_events": self.throttle_events,
        }

    async def get_recommended_delay(self) -> float:
        """Get a recommended delay based on current bandwidth usage."""
        rates = self.get_current_rate()

        if self.max_rpm > 0 and rates["rpm"] > self.max_rpm * 0.9:
            self.throttle_events += 1
            return 5.0 + (rates["rpm"] / self.max_rpm) * 10.0

        if self.max_kbps > 0 and rates["kbps"] > self.max_kbps * 0.9:
            self.throttle_events += 1
            return 3.0 + (rates["kbps"] / self.max_kbps) * 5.0

        return 0.0


def list_profiles() -> None:
    """Print all available bandwidth profiles."""
    print("\nAvailable Bandwidth Profiles:\n")
    for name, profile in BANDWIDTH_PROFILES.items():
        limit = f"{profile.max_kbps} KB/s" if profile.max_kbps else "Unlimited"
        rpm = f"{profile.max_requests_per_minute} req/min" if profile.max_requests_per_minute else "Unlimited"
        print(f"  {name:15s} - {profile.description}")
        print(f"  {'':15s}   Limits: {limit}, {rpm}")
    print()


if __name__ == "__main__":
    list_profiles()

    async def demo():
        controller = BandwidthController(profile="moderate", adaptive=True)
        print(f"Profile: {controller.profile_name}")
        print(f"Adaptive multiplier: {controller._get_adaptive_multiplier()}")

        for i in range(10):
            await controller.acquire(5000)
            controller.record(random.randint(2000, 8000))
            stats = controller.get_stats()
            print(f"Request {i+1}: {stats['current_kbps']:.1f} KB/s, {stats['current_rpm']} RPM")
            await asyncio.sleep(0.5)

    import random
    asyncio.run(demo())
