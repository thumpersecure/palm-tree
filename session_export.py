#!/usr/bin/env python3
"""
Session Export & Analytics - Know thy chaos.

"What good is noise if you can't measure how noisy you are?"

This module tracks detailed session analytics and exports them as
JSON reports. See exactly how confused you've made the trackers,
with metrics over time, category breakdowns, identity rotation
history, and a privacy confusion trend.

Features:
- Real-time session tracking
- JSON export with full analytics
- Privacy score trend over time
- Category and identity distribution
- Request timeline with metadata
- Summary statistics
"""

import json
import time
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

from version import __version__


@dataclass
class RequestRecord:
    """A single request record for analytics."""
    timestamp: str
    url: str
    category: str
    user_agent: str
    status: str
    response_time_ms: float
    bytes_transferred: int
    geo_location: Optional[str] = None
    proxy_used: Optional[str] = None
    identity_name: Optional[str] = None


@dataclass
class PrivacySnapshot:
    """A point-in-time privacy score snapshot."""
    timestamp: str
    confusion_score: int
    unique_fingerprints: int
    categories_visited: int
    identity_changes: int
    requests_count: int


class SessionTracker:
    """
    Tracks all session activity for analytics and export.

    Every request, every identity change, every category visit -
    all recorded for your post-chaos review pleasure.
    """

    def __init__(self, session_name: Optional[str] = None):
        self.session_id = f"session_{int(time.time())}_{os.getpid()}"
        self.session_name = session_name or self.session_id
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None

        self.requests: List[RequestRecord] = []
        self.privacy_snapshots: List[PrivacySnapshot] = []
        self.identity_history: List[Dict[str, str]] = []
        self.geo_rotation_history: List[Dict[str, str]] = []
        self.errors: List[Dict[str, str]] = []

        self._category_counter: Counter = Counter()
        self._ua_counter: Counter = Counter()
        self._site_counter: Counter = Counter()
        self._hourly_requests: Dict[int, int] = defaultdict(int)

        self._snapshot_interval = 60
        self._last_snapshot = time.time()

    def record_request(
        self,
        url: str,
        category: str,
        user_agent: str,
        status: str = "success",
        response_time_ms: float = 0.0,
        bytes_transferred: int = 0,
        geo_location: Optional[str] = None,
        proxy_used: Optional[str] = None,
        identity_name: Optional[str] = None,
    ):
        """Record a completed request."""
        record = RequestRecord(
            timestamp=datetime.now().isoformat(),
            url=url,
            category=category,
            user_agent=user_agent,
            status=status,
            response_time_ms=response_time_ms,
            bytes_transferred=bytes_transferred,
            geo_location=geo_location,
            proxy_used=proxy_used,
            identity_name=identity_name,
        )
        self.requests.append(record)

        self._category_counter[category] += 1
        self._ua_counter[user_agent[:50]] += 1
        domain = url.split("/")[2] if "/" in url and len(url.split("/")) > 2 else url
        self._site_counter[domain] += 1
        self._hourly_requests[datetime.now().hour] += 1

    def record_identity_change(self, identity_name: str, platform: str = ""):
        """Record an identity rotation."""
        self.identity_history.append({
            "timestamp": datetime.now().isoformat(),
            "identity": identity_name,
            "platform": platform,
        })

    def record_geo_rotation(self, country: str, timezone: str):
        """Record a geo location rotation."""
        self.geo_rotation_history.append({
            "timestamp": datetime.now().isoformat(),
            "country": country,
            "timezone": timezone,
        })

    def record_error(self, url: str, error: str):
        """Record an error."""
        self.errors.append({
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "error": str(error),
        })

    def take_privacy_snapshot(
        self,
        confusion_score: int,
        unique_fingerprints: int,
        categories_visited: int,
        identity_changes: int,
    ):
        """Take a point-in-time privacy metrics snapshot."""
        snapshot = PrivacySnapshot(
            timestamp=datetime.now().isoformat(),
            confusion_score=confusion_score,
            unique_fingerprints=unique_fingerprints,
            categories_visited=categories_visited,
            identity_changes=identity_changes,
            requests_count=len(self.requests),
        )
        self.privacy_snapshots.append(snapshot)
        self._last_snapshot = time.time()

    def should_snapshot(self) -> bool:
        """Check if it's time for another privacy snapshot."""
        return time.time() - self._last_snapshot >= self._snapshot_interval

    def get_summary(self) -> Dict[str, Any]:
        """Generate a summary of the session."""
        self.end_time = datetime.now()
        duration = self.end_time - self.start_time
        total_bytes = sum(r.bytes_transferred for r in self.requests)
        successful = sum(1 for r in self.requests if r.status == "success")
        failed = sum(1 for r in self.requests if r.status != "success")
        avg_response = (
            sum(r.response_time_ms for r in self.requests) / len(self.requests)
            if self.requests else 0
        )

        return {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration_seconds": int(duration.total_seconds()),
            "duration_human": str(duration).split(".")[0],
            "total_requests": len(self.requests),
            "successful_requests": successful,
            "failed_requests": failed,
            "success_rate": round(successful / max(len(self.requests), 1) * 100, 1),
            "total_bytes": total_bytes,
            "total_mb": round(total_bytes / (1024 * 1024), 2),
            "avg_response_ms": round(avg_response, 1),
            "unique_categories": len(self._category_counter),
            "unique_user_agents": len(self._ua_counter),
            "unique_sites": len(self._site_counter),
            "identity_changes": len(self.identity_history),
            "geo_rotations": len(self.geo_rotation_history),
            "errors": len(self.errors),
        }

    def get_category_distribution(self) -> Dict[str, int]:
        """Get request counts by category."""
        return dict(self._category_counter.most_common())

    def get_top_sites(self, limit: int = 20) -> Dict[str, int]:
        """Get most visited sites."""
        return dict(self._site_counter.most_common(limit))

    def get_hourly_distribution(self) -> Dict[int, int]:
        """Get request counts by hour of day."""
        return dict(sorted(self._hourly_requests.items()))

    def get_privacy_trend(self) -> List[Dict]:
        """Get privacy score over time."""
        return [
            {
                "timestamp": s.timestamp,
                "confusion_score": s.confusion_score,
                "fingerprints": s.unique_fingerprints,
                "categories": s.categories_visited,
                "identities": s.identity_changes,
                "requests": s.requests_count,
            }
            for s in self.privacy_snapshots
        ]

    def export_json(self, filepath: Optional[str] = None) -> str:
        """
        Export full session report as JSON.

        Args:
            filepath: Path to save the JSON file. If None, uses default naming.

        Returns:
            Path to the saved file.
        """
        if filepath is None:
            export_dir = Path.home() / ".traffic_noise" / "reports"
            export_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(export_dir / f"session_{timestamp}.json")

        report = {
            "report_version": __version__,
            "generator": f"Traffic Noise Generator v{__version__}",
            "summary": self.get_summary(),
            "category_distribution": self.get_category_distribution(),
            "top_sites": self.get_top_sites(),
            "hourly_distribution": self.get_hourly_distribution(),
            "privacy_trend": self.get_privacy_trend(),
            "identity_history": self.identity_history[-100:],
            "geo_rotation_history": self.geo_rotation_history[-100:],
            "recent_errors": self.errors[-50:],
            "request_sample": [
                {
                    "timestamp": r.timestamp,
                    "url": r.url[:100],
                    "category": r.category,
                    "status": r.status,
                    "response_time_ms": r.response_time_ms,
                    "geo_location": r.geo_location,
                }
                for r in self.requests[-200:]
            ],
        }

        with open(filepath, "w") as f:
            json.dump(report, f, indent=2, default=str)

        return filepath

    def print_summary(self):
        """Print a formatted session summary to console."""
        summary = self.get_summary()
        categories = self.get_category_distribution()
        top_sites = self.get_top_sites(10)

        lines = [
            "",
            "=" * 60,
            "SESSION REPORT",
            "=" * 60,
            f"Session: {summary['session_name']}",
            f"Duration: {summary['duration_human']}",
            f"",
            f"Requests:  {summary['total_requests']} total ({summary['successful_requests']} ok, {summary['failed_requests']} failed)",
            f"Data:      {summary['total_mb']} MB transferred",
            f"Avg Time:  {summary['avg_response_ms']} ms",
            f"",
            f"Diversity:",
            f"  Categories:    {summary['unique_categories']}",
            f"  User Agents:   {summary['unique_user_agents']}",
            f"  Sites:         {summary['unique_sites']}",
            f"  Identities:    {summary['identity_changes']}",
            f"  Geo Rotations: {summary['geo_rotations']}",
        ]

        if categories:
            lines.append("")
            lines.append("Top Categories:")
            for cat, count in list(categories.items())[:10]:
                lines.append(f"  {cat:25s} {count:5d}")

        if top_sites:
            lines.append("")
            lines.append("Top Sites:")
            for site, count in list(top_sites.items())[:10]:
                lines.append(f"  {site:35s} {count:5d}")

        if self.privacy_snapshots:
            latest = self.privacy_snapshots[-1]
            lines.append("")
            lines.append(f"Final Privacy Score: {latest.confusion_score}/100")

        lines.append("")
        lines.append("=" * 60)

        print("\n".join(lines))


if __name__ == "__main__":
    tracker = SessionTracker(session_name="demo_session")

    for i in range(20):
        tracker.record_request(
            url=f"https://example{i % 5}.com/page",
            category=["Technology", "News", "Social", "Privacy", "Hobbies"][i % 5],
            user_agent=f"Mozilla/5.0 Agent-{i % 3}",
            status="success" if i % 7 != 0 else "error",
            response_time_ms=100 + i * 10,
            bytes_transferred=5000 + i * 100,
        )

    tracker.take_privacy_snapshot(
        confusion_score=65,
        unique_fingerprints=8,
        categories_visited=5,
        identity_changes=3,
    )

    tracker.print_summary()

    filepath = tracker.export_json()
    print(f"\nReport saved to: {filepath}")
