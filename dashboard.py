#!/usr/bin/env python3
"""
🥥 COCONUTS DASHBOARD - See the chaos unfold in real-time 🌴

A beautiful TUI dashboard that shows exactly what madness is happening.

"Finally, a way to watch your privacy tools invade your privacy."
    - Irony, 2024

Features:
- Live request feed
- Bandwidth monitoring
- Identity rotation display
- Worker status
- Statistics that would make a data analyst cry
"""

import asyncio
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Callable
from threading import Lock
import random

from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.text import Text
from rich import box
from rich.align import Align
from rich.style import Style


# ============================================================================
# STATISTICS TRACKER - The all-seeing eye
# ============================================================================

@dataclass
class RequestLog:
    """A single request log entry."""
    timestamp: datetime
    url: str
    status: str  # "success", "error", "pending"
    identity: str
    response_time: float
    bytes_transferred: int
    worker_id: str


@dataclass
class GlobalStats:
    """
    Global statistics tracker.

    "Counting things so you can feel productive."
    """
    # Request counts
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0

    # Bandwidth
    total_bytes: int = 0
    bytes_per_second: float = 0.0

    # Timing
    start_time: Optional[datetime] = None
    avg_response_time: float = 0.0

    # Workers
    active_workers: int = 0
    total_workers_spawned: int = 0

    # Identities
    identities_used: int = 0
    current_identity: str = "Initializing..."

    # Sites
    sites_visited: set = field(default_factory=set)

    # Current mode
    active_mode: str = "None"

    # Fun stats
    ads_confused: int = 0
    trackers_crying: int = 0
    data_brokers_puzzled: int = 0

    # Response time tracking for average
    _response_times: List[float] = field(default_factory=list)
    _bytes_history: deque = field(default_factory=lambda: deque(maxlen=60))

    _lock: Lock = field(default_factory=Lock)

    def record_request(self, success: bool, response_time: float, bytes_count: int, url: str, identity: str):
        """Record a request."""
        with self._lock:
            self.total_requests += 1
            if success:
                self.successful_requests += 1
                # Fun stats increase on success
                self.ads_confused += random.randint(1, 5)
                self.trackers_crying += random.randint(0, 2)
                self.data_brokers_puzzled += random.randint(0, 1)
            else:
                self.failed_requests += 1

            self.total_bytes += bytes_count
            self._response_times.append(response_time)
            self._bytes_history.append((time.time(), bytes_count))

            # Keep only last 100 response times for average
            if len(self._response_times) > 100:
                self._response_times = self._response_times[-100:]

            self.avg_response_time = sum(self._response_times) / len(self._response_times)
            self.sites_visited.add(url)
            self.current_identity = identity
            self.identities_used += 1

            # Calculate bytes per second
            self._update_bandwidth()

    def _update_bandwidth(self):
        """Update bandwidth calculation."""
        now = time.time()
        cutoff = now - 1.0  # Last second

        recent_bytes = sum(b for t, b in self._bytes_history if t > cutoff)
        self.bytes_per_second = recent_bytes

    def get_uptime(self) -> str:
        """Get formatted uptime."""
        if not self.start_time:
            return "00:00:00"

        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_success_rate(self) -> float:
        """Get success rate percentage."""
        if self.total_requests == 0:
            return 100.0
        return (self.successful_requests / self.total_requests) * 100


# Global stats instance
STATS = GlobalStats()


# ============================================================================
# ACTIVITY LOG - What's happening right now
# ============================================================================

class ActivityLog:
    """
    Rolling activity log.

    "A timeline of questionable decisions."
    """

    def __init__(self, max_entries: int = 50):
        self.entries: deque = deque(maxlen=max_entries)
        self._lock = Lock()

    def add(self, message: str, level: str = "info"):
        """Add a log entry."""
        with self._lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.entries.append({
                "time": timestamp,
                "message": message,
                "level": level,
            })

    def get_recent(self, count: int = 10) -> List[Dict]:
        """Get recent entries."""
        with self._lock:
            return list(self.entries)[-count:]


# Global activity log
ACTIVITY_LOG = ActivityLog()


# ============================================================================
# DASHBOARD COMPONENTS
# ============================================================================

def make_header() -> Panel:
    """Create the header panel."""
    header_text = Text()
    header_text.append("🥥 ", style="bold")
    header_text.append("COCONUTS DASHBOARD", style="bold magenta")
    header_text.append(" 🌴", style="bold")
    header_text.append("\n")
    header_text.append("Real-time chaos monitoring", style="dim italic")

    return Panel(
        Align.center(header_text),
        box=box.DOUBLE,
        style="magenta",
        height=4,
    )


def make_stats_panel() -> Panel:
    """Create the statistics panel."""
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column("Stat", style="cyan")
    table.add_column("Value", style="green")

    # Format bytes
    bytes_str = format_bytes(STATS.total_bytes)
    bandwidth_str = f"{format_bytes(int(STATS.bytes_per_second))}/s"

    table.add_row("⏱️  Uptime", STATS.get_uptime())
    table.add_row("📊 Total Requests", f"{STATS.total_requests:,}")
    table.add_row("✅ Successful", f"{STATS.successful_requests:,}")
    table.add_row("❌ Failed", f"{STATS.failed_requests:,}")
    table.add_row("📈 Success Rate", f"{STATS.get_success_rate():.1f}%")
    table.add_row("", "")
    table.add_row("📦 Data Transfer", bytes_str)
    table.add_row("🚀 Bandwidth", bandwidth_str)
    table.add_row("⚡ Avg Response", f"{STATS.avg_response_time*1000:.0f}ms")
    table.add_row("", "")
    table.add_row("👷 Active Workers", str(STATS.active_workers))
    table.add_row("🌐 Sites Visited", str(len(STATS.sites_visited)))
    table.add_row("🎭 Identities Used", str(STATS.identities_used))

    return Panel(
        table,
        title="[bold cyan]📊 Statistics[/]",
        border_style="cyan",
    )


def make_fun_stats_panel() -> Panel:
    """Create the fun statistics panel."""
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column("Stat", style="yellow")
    table.add_column("Value", style="bold white")

    table.add_row("🎯 Ads Confused", f"{STATS.ads_confused:,}")
    table.add_row("😢 Trackers Crying", f"{STATS.trackers_crying:,}")
    table.add_row("🤔 Data Brokers Puzzled", f"{STATS.data_brokers_puzzled:,}")
    table.add_row("", "")
    table.add_row("🔥 Chaos Level", get_chaos_bar())

    return Panel(
        table,
        title="[bold yellow]🎪 Chaos Metrics[/]",
        border_style="yellow",
    )


def make_identity_panel() -> Panel:
    """Create the current identity panel."""
    identity_text = Text()
    identity_text.append("Current Identity:\n", style="dim")
    identity_text.append(f"{STATS.current_identity}\n\n", style="bold green")
    identity_text.append("Mode: ", style="dim")
    identity_text.append(STATS.active_mode, style="bold magenta")

    return Panel(
        identity_text,
        title="[bold green]🎭 Identity[/]",
        border_style="green",
    )


def make_activity_panel(max_entries: int = 15) -> Panel:
    """Create the activity log panel."""
    table = Table(box=None, show_header=True, padding=(0, 1), expand=True)
    table.add_column("Time", style="dim", width=8)
    table.add_column("Event", style="white", ratio=1)
    table.add_column("Status", style="cyan", width=8)

    for entry in ACTIVITY_LOG.get_recent(max_entries):
        level = entry["level"]
        style = {
            "info": "white",
            "success": "green",
            "error": "red",
            "warning": "yellow",
        }.get(level, "white")

        icon = {
            "info": "📝",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
        }.get(level, "📝")

        status_text = {
            "info": "INFO",
            "success": "OK",
            "error": "FAIL",
            "warning": "WARN",
        }.get(level, "INFO")

        # Truncate message if too long
        message = entry['message']
        if len(message) > 50:
            message = message[:47] + "..."

        table.add_row(
            entry["time"],
            Text(f"{icon} {message}", style=style),
            Text(status_text, style=style)
        )

    # Add placeholder rows if needed
    current_count = len(ACTIVITY_LOG.get_recent(max_entries))
    if current_count == 0:
        table.add_row("--:--:--", Text("Waiting for activity...", style="dim"), "")

    return Panel(
        table,
        title="[bold white]📜 Activity Log[/]",
        border_style="white",
    )


def make_workers_panel() -> Panel:
    """Create the workers status panel."""
    if STATS.active_workers == 0:
        content = Text("No active workers\nWaiting for chaos to begin...", style="dim italic")
    else:
        table = Table(box=None, show_header=True, padding=(0, 1), expand=True)
        table.add_column("Worker", style="cyan", width=10)
        table.add_column("Status", style="green", width=12)
        table.add_column("Reqs", style="yellow", width=6)
        table.add_column("Pattern", style="magenta", width=10)

        # Worker status simulation (more realistic)
        statuses = ["🟢 Active", "🔄 Fetch", "⏳ Wait", "📡 Send"]
        patterns = ["normal", "bursty", "slow", "erratic", "scanner"]

        for i in range(min(STATS.active_workers, 8)):
            # Use consistent random based on worker ID for stability
            status_idx = (i + int(STATS.total_requests / 10)) % len(statuses)
            pattern_idx = (i * 7 + int(STATS.total_requests / 5)) % len(patterns)

            table.add_row(
                f"W-{i+1}",
                statuses[status_idx],
                str((i + 1) * 5 + STATS.total_requests // STATS.active_workers if STATS.active_workers > 0 else 0),
                patterns[pattern_idx]
            )

        content = table

    return Panel(
        content,
        title="[bold blue]👷 Workers[/]",
        border_style="blue",
    )


def make_footer() -> Panel:
    """Create the footer panel."""
    footer_messages = [
        "Press Ctrl+C to stop the chaos",
        "Your ISP is probably confused right now",
        "Data brokers hate this one weird trick",
        "Kevin at the NSA is taking notes",
        "Trackers are questioning their existence",
        "This is fine. Everything is fine.",
        "Remember to touch grass occasionally",
        "Sponsored by caffeine and bad decisions",
    ]

    message = random.choice(footer_messages)

    footer_text = Text()
    footer_text.append("🥥 ", style="bold")
    footer_text.append(message, style="italic dim")
    footer_text.append(" 🌴", style="bold")

    return Panel(
        Align.center(footer_text),
        box=box.MINIMAL,
        style="dim",
        height=3,
    )


def get_chaos_bar() -> str:
    """Get a visual chaos level bar."""
    # Chaos level based on activity
    chaos = min(100, STATS.total_requests // 10)
    filled = chaos // 10
    empty = 10 - filled
    return "█" * filled + "░" * empty + f" {chaos}%"


def format_bytes(bytes_count: int) -> str:
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} TB"


# ============================================================================
# MAIN DASHBOARD CLASS
# ============================================================================

class Dashboard:
    """
    The main dashboard controller.

    "A window into the beautiful chaos."
    """

    def __init__(self, max_activity_entries: int = 15):
        self.console = Console()
        self.running = False
        self._refresh_rate = 4  # Refreshes per second
        self._max_activity = max_activity_entries

    def make_layout(self) -> Layout:
        """Create the dashboard layout."""
        layout = Layout()

        # Main structure - improved proportions
        layout.split_column(
            Layout(name="header", size=4),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3),
        )

        # Body split - better balance for content
        layout["body"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=3),
        )

        # Left side - stats panels
        layout["left"].split_column(
            Layout(name="stats", ratio=2),
            Layout(name="fun_stats", ratio=1),
            Layout(name="identity", size=7),
        )

        # Right side - activity and workers
        layout["right"].split_column(
            Layout(name="activity", ratio=2),
            Layout(name="workers", ratio=1),
        )

        return layout

    def update_layout(self, layout: Layout) -> Layout:
        """Update all layout panels."""
        layout["header"].update(make_header())
        layout["stats"].update(make_stats_panel())
        layout["fun_stats"].update(make_fun_stats_panel())
        layout["identity"].update(make_identity_panel())
        layout["workers"].update(make_workers_panel())
        layout["activity"].update(make_activity_panel(self._max_activity))
        layout["footer"].update(make_footer())
        return layout

    async def run(self):
        """Run the dashboard."""
        self.running = True
        STATS.start_time = datetime.now()

        layout = self.make_layout()

        with Live(layout, refresh_per_second=self._refresh_rate, console=self.console) as live:
            while self.running:
                self.update_layout(layout)
                await asyncio.sleep(1 / self._refresh_rate)

    def stop(self):
        """Stop the dashboard."""
        self.running = False


# ============================================================================
# INTEGRATION HELPERS
# ============================================================================

def log_activity(message: str, level: str = "info"):
    """Log an activity to the dashboard."""
    ACTIVITY_LOG.add(message, level)


def record_request(
    success: bool,
    url: str,
    response_time: float = 0.0,
    bytes_count: int = 0,
    identity: str = "Anonymous"
):
    """Record a request to the dashboard stats."""
    STATS.record_request(success, response_time, bytes_count, url, identity)


def set_active_mode(mode: str):
    """Set the active mode display."""
    STATS.active_mode = mode


def set_active_workers(count: int):
    """Set active worker count."""
    STATS.active_workers = count


def set_current_identity(identity: str):
    """Set current identity display."""
    STATS.current_identity = identity


# ============================================================================
# STANDALONE DEMO
# ============================================================================

async def demo_dashboard():
    """Run a demo of the dashboard with fake data."""
    dashboard = Dashboard()

    # Start dashboard in background
    dashboard_task = asyncio.create_task(dashboard.run())

    # Simulate activity
    set_active_mode("Demo Mode 🎪")
    set_active_workers(3)

    urls = [
        "https://www.google.com",
        "https://www.reddit.com",
        "https://www.github.com",
        "https://www.amazon.com",
        "https://www.twitter.com",
    ]

    identities = [
        "Karen from Wisconsin",
        "Chad the Crypto Bro",
        "Paranoid Pete",
        "3am You",
        "Corporate Carl",
    ]

    try:
        for i in range(1000):
            await asyncio.sleep(random.uniform(0.3, 1.0))

            url = random.choice(urls)
            identity = random.choice(identities)
            success = random.random() > 0.1

            record_request(
                success=success,
                url=url,
                response_time=random.uniform(0.1, 2.0),
                bytes_count=random.randint(1000, 50000),
                identity=identity
            )

            set_current_identity(identity)

            if success:
                log_activity(f"Visited {url.split('//')[1]}", "success")
            else:
                log_activity(f"Failed to reach {url.split('//')[1]}", "error")

            # Occasionally change workers
            if random.random() > 0.95:
                workers = random.randint(1, 5)
                set_active_workers(workers)
                log_activity(f"Worker count changed to {workers}", "info")

    except asyncio.CancelledError:
        pass
    finally:
        dashboard.stop()
        await dashboard_task


if __name__ == "__main__":
    print("🥥 Starting Dashboard Demo... Press Ctrl+C to stop\n")
    try:
        asyncio.run(demo_dashboard())
    except KeyboardInterrupt:
        print("\n\n🥥 Dashboard demo complete!")
