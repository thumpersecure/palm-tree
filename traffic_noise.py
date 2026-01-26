#!/usr/bin/env python3
"""
Traffic Noise Generator - Python Version with Dynamic Terminal UI

"I'm not paranoid, I'm just really popular with advertisers."
    - Every user of this tool

Generates randomized network traffic to obscure browsing patterns.
Features live headline display using Rich terminal library.

Side effects may include:
- Confused ad algorithms
- Data brokers questioning their career choices
- A sudden increase in ads for PlayStation 5s and Samsung Smart Fridges
- The warm fuzzy feeling of digital privacy

Not responsible for any existential crises caused to tracking scripts.
"""

import asyncio
import argparse
import random
import string
import hashlib
import socket
import signal
import sys
import re
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Deque
from collections import deque
from contextlib import suppress

import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.style import Style
from rich import box

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config:
    mode: str = "news"
    vps_target: Optional[str] = None
    show_headlines: bool = True
    randomize_identity: bool = False
    chaos_mode: bool = False
    parallel_workers: int = 3
    duration: int = 0  # 0 = continuous
    interface: str = "eth0"
    quiet: bool = False
    max_headlines: int = 3

# Timing ranges
MIN_DELAY = 3
MAX_DELAY = 45
MIN_SESSION = 60
MAX_SESSION = 300
CHAOS_MIN_DELAY = 1
CHAOS_MAX_DELAY = 120

# ============================================================================
# USER AGENTS
# ============================================================================

USER_AGENTS = [
    # Windows Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Windows Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Windows Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    # macOS Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    # macOS Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    # iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    # Android
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    # Bots (intentional)
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    # Exotic - The Hall of Fame 🏆
    "Mozilla/5.0 (PlayStation; PlayStation 5/1.0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",  # Gaming at 3am
    "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/609.4 (KHTML, like Gecko) NF/6.0.2.21.3 NintendoBrowser/5.1.0.22474",  # Mario needs news too
    "Mozilla/5.0 (SMART-TV; Linux; Tizen 6.5) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/85.0.4183.93 TV Safari/537.36",  # Couch surfing
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Tesla/2021.44.25.2",  # Stuck in traffic, browsing traffic
    "Mozilla/5.0 (SmartFridge; Linux) AppleWebKit/537.36 LG/1.0",  # Your fridge judging your browsing
    "Mozilla/5.0 (Roomba; Linux; iRobot) AppleWebKit/537.36 Vacuum/3.0",  # Cleaning the web
    "Mozilla/5.0 (SmartToaster; Linux) AppleWebKit/537.36 Toast/2.0",  # Browsing while you breakfast
    # Old browsers - The Nostalgia Section 👴
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",  # Grandma's computer still works
    "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",  # XP never dies
]

# ============================================================================
# DNS SERVERS
# ============================================================================

DNS_SERVERS = [
    "8.8.8.8", "8.8.4.4",           # Google
    "1.1.1.1", "1.0.0.1",           # Cloudflare
    "9.9.9.9", "149.112.112.112",   # Quad9
    "208.67.222.222", "208.67.220.220",  # OpenDNS
    "64.6.64.6", "64.6.65.6",       # Verisign
    "185.228.168.9",                # CleanBrowsing
    "94.140.14.14",                 # AdGuard
]

# ============================================================================
# NEWS SITES BY CATEGORY
# ============================================================================

NEWS_SITES = {
    "Lifestyle": [
        "https://www.buzzfeed.com",
        "https://www.huffpost.com/life",
        "https://www.refinery29.com",
        "https://www.goodhousekeeping.com",
        "https://www.allrecipes.com",
        "https://www.foodnetwork.com",
    ],
    "World": [
        "https://www.bbc.com/news/world",
        "https://www.reuters.com/world",
        "https://www.aljazeera.com",
        "https://www.theguardian.com/world",
        "https://apnews.com/world-news",
        "https://www.france24.com/en",
        "https://www.dw.com/en",
        "https://www.npr.org/sections/world",
    ],
    "Technology": [
        "https://www.theverge.com",
        "https://techcrunch.com",
        "https://arstechnica.com",
        "https://www.wired.com",
        "https://www.cnet.com",
        "https://www.engadget.com",
        "https://www.zdnet.com",
    ],
    "Health": [
        "https://www.webmd.com",
        "https://www.healthline.com",
        "https://www.medicalnewstoday.com",
        "https://www.health.com",
        "https://www.prevention.com",
    ],
    "Trending": [
        "https://news.google.com",
        "https://www.reddit.com/r/news",
        "https://news.ycombinator.com",
        "https://www.usatoday.com",
        "https://www.nbcnews.com",
        "https://www.cnn.com",
    ],
}

# ============================================================================
# FINGERPRINT VARIATIONS
# ============================================================================

LANGUAGES = [
    "en-US,en;q=0.9", "en-GB,en;q=0.9", "en-US,en;q=0.9,es;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8", "pt-BR,pt;q=0.9,en;q=0.8",
    "ja-JP,ja;q=0.9,en;q=0.8", "zh-CN,zh;q=0.9,en;q=0.8",
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.reddit.com/",
    "",  # Direct
]

ACCEPT_HEADERS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "*/*",
]

ENCODINGS = ["gzip, deflate, br", "gzip, deflate", "gzip"]

PLATFORMS = ["Windows", "macOS", "Linux", "Android", "iOS"]

BROWSING_PATTERNS = ["normal", "bursty", "slow", "erratic", "scanner"]

# ============================================================================
# GLOBAL STATE
# ============================================================================

@dataclass
class AppState:
    headlines: Deque[dict] = field(default_factory=lambda: deque(maxlen=10))
    request_count: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    workers_active: int = 0
    last_category: str = ""
    last_url: str = ""
    running: bool = True
    errors: int = 0

console = Console()
state = AppState()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_session_id() -> str:
    """Generate a session ID that looks legit but is totally fake.
    Like my confidence during code reviews."""
    return ''.join(random.choices(string.hexdigits.lower(), k=32))

def generate_mac() -> str:
    return ':'.join([
        format((random.randint(0, 255) & 0xFE) | 0x02, '02x'),
        *[format(random.randint(0, 255), '02x') for _ in range(5)]
    ])

def get_random_news_url() -> tuple[str, str]:
    category = random.choice(list(NEWS_SITES.keys()))
    url = random.choice(NEWS_SITES[category])
    return category, url

def get_pattern_delay(pattern: str, chaos: bool = False) -> float:
    if chaos:
        return random.uniform(CHAOS_MIN_DELAY, CHAOS_MAX_DELAY)

    delays = {
        "normal": (5, 30),
        "bursty": (1, 3) if random.random() < 0.7 else (30, 90),
        "slow": (45, 180),
        "erratic": (1, 120),
        "scanner": (1, 5),
    }
    min_d, max_d = delays.get(pattern, (MIN_DELAY, MAX_DELAY))
    return random.uniform(min_d, max_d)

def build_headers() -> dict:
    """
    Build randomized HTTP headers.

    Creates headers so diverse that ad networks will think you're
    simultaneously a Windows user, a Mac enthusiast, a Linux nerd,
    and someone who browses the web on their refrigerator.
    """
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": random.choice(ACCEPT_HEADERS),
        "Accept-Language": random.choice(LANGUAGES),
        "Accept-Encoding": random.choice(ENCODINGS),
        "Connection": random.choice(["keep-alive", "close"]),
    }

    # Random DNT
    if random.random() > 0.3:
        headers["DNT"] = str(random.randint(0, 1))

    # Random referer
    referer = random.choice(REFERERS)
    if referer:
        headers["Referer"] = referer

    # Random cache control
    if random.random() > 0.5:
        headers["Cache-Control"] = random.choice(["max-age=0", "no-cache", "no-store"])

    # Sec-CH-UA headers (modern browsers)
    if random.random() > 0.5:
        headers["Sec-CH-UA-Mobile"] = f"?{random.randint(0, 1)}"
        headers["Sec-CH-UA-Platform"] = f'"{random.choice(PLATFORMS)}"'

    # Fake cookies
    if random.random() > 0.3:
        session_id = generate_session_id()
        ts = int(datetime.now().timestamp())
        headers["Cookie"] = f"_ga=GA1.2.{random.randint(1000000, 9999999)}.{ts}; session={session_id}"

    return headers

# ============================================================================
# HEADLINE EXTRACTION
# ============================================================================

def extract_headlines(html: str, url: str, category: str) -> List[dict]:
    headlines = []
    try:
        soup = BeautifulSoup(html, 'lxml')

        # Try various headline selectors
        selectors = [
            'h1', 'h2', 'h3',
            'article h2', 'article h3',
            '.headline', '.title',
            '[class*="headline"]', '[class*="title"]',
        ]

        seen = set()
        for selector in selectors:
            for elem in soup.select(selector)[:5]:
                text = elem.get_text(strip=True)
                # Clean and validate
                text = re.sub(r'\s+', ' ', text)
                if len(text) > 20 and len(text) < 200 and text not in seen:
                    seen.add(text)
                    headlines.append({
                        "text": text[:120] + "..." if len(text) > 120 else text,
                        "category": category,
                        "source": url.split('/')[2],
                        "time": datetime.now().strftime("%H:%M:%S"),
                    })
                    if len(headlines) >= 5:
                        break
            if len(headlines) >= 5:
                break

        # Fallback to title tag
        if not headlines:
            title = soup.find('title')
            if title:
                text = title.get_text(strip=True)
                if len(text) > 10:
                    headlines.append({
                        "text": text[:120],
                        "category": category,
                        "source": url.split('/')[2],
                        "time": datetime.now().strftime("%H:%M:%S"),
                    })
    except Exception:
        pass

    return headlines

# ============================================================================
# NETWORK FUNCTIONS
# ============================================================================

async def fetch_url(client: httpx.AsyncClient, url: str, worker_id: int) -> Optional[str]:
    headers = build_headers()

    try:
        response = await client.get(url, headers=headers, timeout=30.0, follow_redirects=True)
        state.request_count += 1
        return response.text
    except Exception:
        state.errors += 1
        return None

async def connect_to_vps(client: httpx.AsyncClient, target: str) -> bool:
    headers = build_headers()

    # Parse target
    if ':' in target:
        host, port = target.rsplit(':', 1)
    else:
        host, port = target, "80"

    # Try HTTPS, then HTTP
    for scheme in ["https", "http"]:
        try:
            url = f"{scheme}://{host}:{port}"
            response = await client.get(url, headers=headers, timeout=30.0)
            state.request_count += 1
            return True
        except Exception:
            continue

    # Fallback: raw TCP ping
    try:
        reader, writer = await asyncio.open_connection(host, int(port))
        writer.write(f"PING_{int(datetime.now().timestamp())}\n".encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        state.request_count += 1
        return True
    except Exception:
        state.errors += 1
        return False

def send_local_udp(port: int = 19999):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = f"NOISE_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}"
        sock.sendto(message.encode(), ("127.0.0.1", port))
        sock.close()
    except Exception:
        pass

# ============================================================================
# TERMINAL UI
# ============================================================================

def create_display(config: Config) -> Layout:
    layout = Layout()

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="headlines", size=config.max_headlines + 4),
        Layout(name="stats", size=6),
        Layout(name="footer", size=3),
    )

    return layout

def update_display(layout: Layout, config: Config):
    # Header
    elapsed = datetime.now() - state.start_time
    elapsed_str = str(elapsed).split('.')[0]

    mode_text = f"[bold cyan]CHAOS MODE[/]" if config.chaos_mode else f"[cyan]{config.mode.upper()}[/]"
    header_text = Text()
    header_text.append("🌐 Traffic Noise Generator ", style="bold green")
    header_text.append(f"| Mode: {mode_text} ", style="white")
    header_text.append(f"| Workers: [yellow]{config.parallel_workers}[/] ", style="white")
    header_text.append(f"| Runtime: [magenta]{elapsed_str}[/]", style="white")

    layout["header"].update(Panel(header_text, box=box.ROUNDED))

    # Headlines
    headline_table = Table(
        show_header=True,
        header_style="bold blue",
        box=box.SIMPLE,
        expand=True,
        padding=(0, 1),
    )
    headline_table.add_column("Time", style="dim", width=10)
    headline_table.add_column("Category", style="cyan", width=12)
    headline_table.add_column("Headline", style="white", ratio=1)
    headline_table.add_column("Source", style="dim green", width=25)

    # Get most recent headlines
    recent = list(state.headlines)[-config.max_headlines:]
    for h in recent:
        headline_table.add_row(
            h.get("time", ""),
            h.get("category", "")[:10],
            h.get("text", "")[:80],
            h.get("source", "")[:23],
        )

    # Pad with empty rows if needed
    while len(recent) < config.max_headlines:
        headline_table.add_row("", "", "[dim]Waiting for headlines...[/]", "")
        recent.append({})

    layout["headlines"].update(Panel(
        headline_table,
        title="[bold]📰 Live Headlines[/]",
        border_style="blue",
        box=box.ROUNDED,
    ))

    # Stats
    stats_table = Table(show_header=False, box=None, expand=True, padding=(0, 2))
    stats_table.add_column("Label", style="dim")
    stats_table.add_column("Value", style="bold")
    stats_table.add_column("Label2", style="dim")
    stats_table.add_column("Value2", style="bold")

    stats_table.add_row(
        "Requests:", f"[green]{state.request_count}[/]",
        "Errors:", f"[red]{state.errors}[/]",
    )
    stats_table.add_row(
        "Last Category:", f"[cyan]{state.last_category or 'N/A'}[/]",
        "Active Workers:", f"[yellow]{state.workers_active}[/]",
    )
    stats_table.add_row(
        "Last URL:", f"[dim]{(state.last_url or 'N/A')[:50]}[/]",
        "", "",
    )

    layout["stats"].update(Panel(
        stats_table,
        title="[bold]📊 Statistics[/]",
        border_style="green",
        box=box.ROUNDED,
    ))

    # Footer
    if config.vps_target:
        target_text = f"[yellow]VPS Target: {config.vps_target}[/]"
    else:
        target_text = "[dim]Browsing news sites[/]"

    footer_text = Text()
    footer_text.append("Press Ctrl+C to stop | ", style="dim")
    footer_text.append(target_text)

    layout["footer"].update(Panel(footer_text, box=box.ROUNDED))

# ============================================================================
# WORKER
# ============================================================================

async def worker(worker_id: int, config: Config, layout: Layout, live: Live):
    pattern = random.choice(BROWSING_PATTERNS)
    state.workers_active += 1

    async with httpx.AsyncClient() as client:
        while state.running:
            try:
                # Local UDP noise occasionally
                if random.random() < 0.2:
                    send_local_udp(19999 + worker_id)

                # Fetch content
                if config.mode == "vps" and config.vps_target:
                    await connect_to_vps(client, config.vps_target)
                    state.last_url = config.vps_target
                    state.last_category = "VPS"
                else:
                    category, url = get_random_news_url()
                    state.last_category = category
                    state.last_url = url

                    html = await fetch_url(client, url, worker_id)

                    if html and config.show_headlines:
                        headlines = extract_headlines(html, url, category)
                        for h in headlines[:2]:  # Add up to 2 headlines per fetch
                            state.headlines.append(h)

                # Update display
                update_display(layout, config)
                live.refresh()

                # Delay based on pattern
                delay = get_pattern_delay(pattern, config.chaos_mode)

                # Chaos mode: occasionally change pattern
                if config.chaos_mode and random.random() < 0.1:
                    pattern = random.choice(BROWSING_PATTERNS)

                await asyncio.sleep(delay)

            except asyncio.CancelledError:
                break
            except Exception:
                state.errors += 1
                await asyncio.sleep(5)

    state.workers_active -= 1

# ============================================================================
# MAIN
# ============================================================================

async def main_async(config: Config):
    layout = create_display(config)

    with Live(layout, console=console, refresh_per_second=2, screen=True) as live:
        update_display(layout, config)

        # Create workers
        tasks = [
            asyncio.create_task(worker(i, config, layout, live))
            for i in range(config.parallel_workers)
        ]

        try:
            if config.duration > 0:
                await asyncio.sleep(config.duration * 60)
                state.running = False
            else:
                # Run until interrupted
                await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass
        finally:
            state.running = False
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

def signal_handler(sig, frame):
    state.running = False
    console.print("\n[yellow]Shutting down...[/]")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Traffic Noise Generator - Network obfuscation with live headlines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -n -H                    # News mode with headlines
  %(prog)s -c -w 5                  # Chaos mode with 5 workers
  %(prog)s -v 192.168.1.100:8080    # Connect to VPS
  %(prog)s -c -w 10 -d 60           # Max obfuscation for 60 min
        """
    )

    parser.add_argument("-n", "--news-only", action="store_true", default=True,
                        help="Browse random news sites (default)")
    parser.add_argument("-v", "--vps", type=str, metavar="IP:PORT",
                        help="Connect to specific VPS endpoint")
    parser.add_argument("-H", "--headlines", action="store_true", default=True,
                        help="Show live headlines (default: on)")
    parser.add_argument("--no-headlines", action="store_true",
                        help="Disable headline display")
    parser.add_argument("-r", "--randomize-id", action="store_true",
                        help="Full identity randomization")
    parser.add_argument("-c", "--chaos", action="store_true",
                        help="Chaos mode - erratic multi-bot simulation")
    parser.add_argument("-w", "--workers", type=int, default=3, metavar="NUM",
                        help="Number of parallel workers (default: 3, max: 10)")
    parser.add_argument("-d", "--duration", type=int, default=0, metavar="MINS",
                        help="Run duration in minutes (default: continuous)")
    parser.add_argument("-i", "--interface", type=str, default="eth0",
                        help="Network interface (default: eth0)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Minimal output")
    parser.add_argument("--max-headlines", type=int, default=3,
                        help="Max headlines to display (default: 3)")

    args = parser.parse_args()

    # Build config
    config = Config(
        mode="vps" if args.vps else "news",
        vps_target=args.vps,
        show_headlines=not args.no_headlines,
        randomize_identity=args.randomize_id,
        chaos_mode=args.chaos,
        parallel_workers=min(max(args.workers, 1), 10),
        duration=args.duration,
        interface=args.interface,
        quiet=args.quiet,
        max_headlines=args.max_headlines,
    )

    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Show banner
    if not config.quiet:
        console.print(Panel.fit(
            "[bold green]Traffic Noise Generator[/]\n"
            f"[dim]Mode: {'VPS' if config.vps_target else 'News'} | "
            f"Workers: {config.parallel_workers} | "
            f"Chaos: {config.chaos_mode}[/]",
            border_style="green",
        ))
        console.print("[dim]Starting... Press Ctrl+C to stop[/]\n")

    # Run
    try:
        asyncio.run(main_async(config))
    except KeyboardInterrupt:
        pass
    finally:
        console.print("\n[green]Cleanup complete.[/]")

if __name__ == "__main__":
    main()
