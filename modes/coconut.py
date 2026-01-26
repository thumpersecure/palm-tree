#!/usr/bin/env python3
"""
Coconut Mode - Headless browser army.

🥥 COCONUTS FROM THE PALM-TREE 🌴

"Like coconuts falling from a palm tree - silent, unexpected,
and occasionally hitting data collectors on the head."

This mode spawns headless browser instances that visit top websites
silently. No windows, no traces, just vibes and confused trackers.

Features:
- Headless Chrome/Firefox via Playwright
- Top 100 websites rotation
- Full browser fingerprint (not just HTTP)
- JavaScript execution (looks more real)
- Bandwidth throttling
- Automatic browser installation

Side Effects:
- May cause tracker algorithms to question their existence
- Ad networks filing for emotional distress
- Your ISP wondering if you're okay
"""

from __future__ import annotations  # Allows string type hints without importing

import asyncio
import random
import sys
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable, Any, TYPE_CHECKING
from datetime import datetime
import os

# Type hints only - not imported at runtime (prevents NameError when playwright missing)
if TYPE_CHECKING:
    from playwright.async_api import Browser, Page, BrowserContext

# Check for playwright availability at runtime
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    async_playwright = None  # type: ignore


@dataclass
class CoconutConfig:
    """
    Configuration for Coconut Mode.

    Tune these to balance stealth vs resource usage.
    """
    # Number of concurrent browsers (coconuts)
    max_concurrent: int = 2

    # Browser settings
    headless: bool = True
    browser_type: str = "chromium"  # chromium, firefox, or webkit

    # Resource limits
    disable_images: bool = True  # 80% less bandwidth
    disable_media: bool = True   # No video/audio
    disable_fonts: bool = False  # Keep fonts for realism

    # Timing
    min_visit_duration: float = 3.0   # Minimum seconds on page
    max_visit_duration: float = 15.0  # Maximum seconds on page
    spawn_delay: float = 5.0          # Seconds between spawning new coconuts

    # Bandwidth (approximate)
    max_bandwidth_kbps: int = 500

    # User activity simulation
    scroll_pages: bool = True
    click_links: bool = False  # Risky - might navigate away


# Top 100 websites (based on global traffic)
TOP_SITES = [
    # Search & Portals
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.baidu.com",
    "https://www.wikipedia.org",
    "https://www.yahoo.com",
    "https://www.reddit.com",
    "https://www.tiktok.com",

    # E-commerce
    "https://www.amazon.com",
    "https://www.ebay.com",
    "https://www.aliexpress.com",
    "https://www.walmart.com",
    "https://www.etsy.com",
    "https://www.target.com",
    "https://www.bestbuy.com",
    "https://www.costco.com",

    # News & Media
    "https://www.cnn.com",
    "https://www.bbc.com",
    "https://www.nytimes.com",
    "https://www.theguardian.com",
    "https://www.reuters.com",
    "https://www.forbes.com",
    "https://www.bloomberg.com",
    "https://www.huffpost.com",
    "https://www.washingtonpost.com",
    "https://www.usatoday.com",

    # Technology
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.linkedin.com",
    "https://www.netflix.com",
    "https://www.twitch.tv",
    "https://www.spotify.com",
    "https://www.zoom.us",
    "https://www.slack.com",

    # Tech News
    "https://www.theverge.com",
    "https://techcrunch.com",
    "https://www.wired.com",
    "https://arstechnica.com",
    "https://www.cnet.com",
    "https://www.engadget.com",

    # Finance
    "https://www.paypal.com",
    "https://www.chase.com",
    "https://www.bankofamerica.com",
    "https://www.wellsfargo.com",
    "https://www.fidelity.com",
    "https://www.schwab.com",
    "https://www.coinbase.com",

    # Entertainment
    "https://www.imdb.com",
    "https://www.rottentomatoes.com",
    "https://www.espn.com",
    "https://www.nfl.com",
    "https://www.mlb.com",
    "https://www.nba.com",
    "https://www.ign.com",
    "https://www.gamespot.com",

    # Social
    "https://www.pinterest.com",
    "https://www.tumblr.com",
    "https://www.quora.com",
    "https://www.discord.com",
    "https://www.snapchat.com",
    "https://www.telegram.org",

    # Lifestyle
    "https://www.yelp.com",
    "https://www.tripadvisor.com",
    "https://www.airbnb.com",
    "https://www.booking.com",
    "https://www.expedia.com",
    "https://www.zillow.com",
    "https://www.realtor.com",

    # Health
    "https://www.webmd.com",
    "https://www.healthline.com",
    "https://www.mayoclinic.org",
    "https://www.nih.gov",

    # Education
    "https://www.khanacademy.org",
    "https://www.coursera.org",
    "https://www.udemy.com",
    "https://www.edx.org",

    # Reference
    "https://www.weather.com",
    "https://www.dictionary.com",
    "https://www.merriam-webster.com",

    # International
    "https://www.bbc.co.uk",
    "https://www.lemonde.fr",
    "https://www.spiegel.de",
    "https://www.elpais.com",
    "https://www.corriere.it",
    "https://www.asahi.com",

    # Misc Popular
    "https://www.craigslist.org",
    "https://www.indeed.com",
    "https://www.glassdoor.com",
    "https://www.dropbox.com",
    "https://www.wordpress.com",
    "https://www.medium.com",
]


class Coconut:
    """
    A single coconut - one headless browser instance.

    "I am but a humble coconut, falling from the palm tree
    of privacy into the ocean of the internet."
    """

    def __init__(
        self,
        coconut_id: int,
        browser: Any,  # Browser type when playwright available
        config: CoconutConfig,
        identity_forge: Optional[Any] = None,
    ):
        """
        Initialize a coconut.

        Args:
            coconut_id: Unique ID for this coconut (for logging purposes and existential identity)
            browser: Playwright Browser instance (the vessel for our chaos)
            config: Configuration settings (the rules we'll probably bend)
            identity_forge: Optional identity generator (for becoming someone else)
        """
        self.coconut_id = coconut_id
        self.browser = browser
        self.config = config
        self.identity_forge = identity_forge

        self.context: Any = None  # BrowserContext when available
        self.page: Any = None     # Page when available
        self.visits = 0
        self.errors = 0

    async def setup(self) -> None:
        """Set up the browser context with a random identity."""
        # Get identity if forge is available
        if self.identity_forge:
            identity = self.identity_forge.mint_identity()
            user_agent = identity.user_agent
            viewport = self._parse_resolution(identity.screen_resolution)
            locale = f"{identity.language_code}-{identity.country_code}"
            timezone = identity.timezone
        else:
            user_agent = random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 Safari/605.1.15",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            ])
            viewport = {"width": 1920, "height": 1080}
            locale = "en-US"
            timezone = "America/New_York"

        # Create context with identity
        self.context = await self.browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            locale=locale,
            timezone_id=timezone,
            # Permissions
            permissions=["geolocation"] if random.random() > 0.5 else [],
            # Emulate device features
            has_touch=random.random() > 0.8,
            is_mobile=random.random() > 0.9,
        )

        # Block resources if configured
        if self.config.disable_images or self.config.disable_media:
            await self.context.route("**/*", self._route_handler)

        self.page = await self.context.new_page()

    async def _route_handler(self, route, request):
        """Handle resource blocking."""
        resource_type = request.resource_type

        if self.config.disable_images and resource_type in ["image", "imageset"]:
            await route.abort()
        elif self.config.disable_media and resource_type in ["media", "font"]:
            await route.abort()
        else:
            await route.continue_()

    def _parse_resolution(self, resolution: str) -> Dict[str, int]:
        """Parse resolution string to viewport dict."""
        try:
            w, h = resolution.split("x")
            return {"width": int(w), "height": int(h)}
        except Exception:
            return {"width": 1920, "height": 1080}

    async def visit(self, url: str) -> bool:
        """
        Visit a URL and simulate human behavior.

        Returns True if successful, False otherwise.
        """
        if not self.page:
            return False

        try:
            # Navigate to the page
            await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # Wait a bit for JavaScript to run
            await asyncio.sleep(random.uniform(1, 3))

            # Simulate scrolling if enabled
            if self.config.scroll_pages:
                await self._simulate_scroll()

            # Wait for the configured duration
            duration = random.uniform(
                self.config.min_visit_duration,
                self.config.max_visit_duration
            )
            await asyncio.sleep(duration)

            self.visits += 1
            return True

        except Exception as e:
            self.errors += 1
            return False

    async def _simulate_scroll(self) -> None:
        """Simulate human-like scrolling."""
        try:
            # Get page height
            scroll_height = await self.page.evaluate("document.body.scrollHeight")

            # Scroll down in random increments
            current_position = 0
            max_scrolls = random.randint(2, 5)

            for _ in range(max_scrolls):
                scroll_amount = random.randint(100, 500)
                current_position = min(current_position + scroll_amount, scroll_height)

                await self.page.evaluate(f"window.scrollTo(0, {current_position})")
                await asyncio.sleep(random.uniform(0.3, 1.0))

        except Exception:
            pass  # Scrolling is optional

    async def cleanup(self) -> None:
        """Clean up browser resources."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()


class CoconutMode:
    """
    Coconut Mode - Headless browser army visiting top 100 sites.

    🥥 COCONUTS FROM THE PALM-TREE 🌴

    "Each coconut is a complete browser instance with its own
    identity, visiting real websites in the background."
    """

    def __init__(
        self,
        config: Optional[CoconutConfig] = None,
        identity_forge: Optional[object] = None,
        sites: Optional[List[str]] = None,
    ):
        """
        Initialize Coconut Mode.

        Args:
            config: Configuration for coconut behavior
            identity_forge: IdentityForge instance for generating identities
            sites: Custom list of sites to visit (uses TOP_SITES if None)
        """
        self.config = config or CoconutConfig()
        self.identity_forge = identity_forge
        self.sites = sites or TOP_SITES

        self.browser: Optional[Browser] = None
        self.coconuts: List[Coconut] = []
        self.running = False

        self.stats = {
            "total_visits": 0,
            "total_errors": 0,
            "sites_visited": set(),
            "start_time": None,
        }

    async def _check_playwright(self) -> bool:
        """Check if Playwright is available and browsers are installed."""
        if not PLAYWRIGHT_AVAILABLE:
            print("[Coconut] Playwright not installed!")
            print("[Coconut] Install with: pip install playwright && playwright install chromium")
            return False
        return True

    async def start(self) -> bool:
        """Start the browser and prepare for coconut spawning."""
        if not await self._check_playwright():
            return False

        try:
            self.playwright = await async_playwright().start()

            # Select browser type
            if self.config.browser_type == "firefox":
                browser_type = self.playwright.firefox
            elif self.config.browser_type == "webkit":
                browser_type = self.playwright.webkit
            else:
                browser_type = self.playwright.chromium

            # Launch browser
            self.browser = await browser_type.launch(headless=self.config.headless)
            self.running = True
            self.stats["start_time"] = datetime.now()

            print(f"[Coconut] Browser started: {self.config.browser_type}")
            return True

        except Exception as e:
            print(f"[Coconut] Failed to start browser: {e}")
            print("[Coconut] Try running: playwright install")
            return False

    async def spawn_coconut(self) -> Optional[Coconut]:
        """Spawn a new coconut (browser context)."""
        if not self.browser or not self.running:
            return None

        coconut_id = len(self.coconuts) + 1
        coconut = Coconut(
            coconut_id=coconut_id,
            browser=self.browser,
            config=self.config,
            identity_forge=self.identity_forge,
        )

        try:
            await coconut.setup()
            self.coconuts.append(coconut)
            print(f"[Coconut] 🥥 Spawned coconut #{coconut_id}")
            return coconut
        except Exception as e:
            print(f"[Coconut] Failed to spawn coconut: {e}")
            return None

    async def run_coconut(self, coconut: Coconut, num_visits: int = 10) -> None:
        """Run a coconut through multiple site visits."""
        for _ in range(num_visits):
            if not self.running:
                break

            # Pick a random site
            site = random.choice(self.sites)

            print(f"[Coconut #{coconut.coconut_id}] Visiting: {site}")
            success = await coconut.visit(site)

            if success:
                self.stats["total_visits"] += 1
                self.stats["sites_visited"].add(site)
                print(f"[Coconut #{coconut.coconut_id}] ✓ Visit complete")
            else:
                self.stats["total_errors"] += 1
                print(f"[Coconut #{coconut.coconut_id}] ✗ Visit failed")

            # Delay before next visit
            await asyncio.sleep(random.uniform(2, 5))

        # Cleanup this coconut
        await coconut.cleanup()
        print(f"[Coconut #{coconut.coconut_id}] 🥥 Coconut biodegraded")

    async def run(
        self,
        duration_minutes: int = 60,
        visits_per_coconut: int = 10,
    ) -> None:
        """
        Run Coconut Mode.

        Args:
            duration_minutes: How long to run (0 = continuous)
            visits_per_coconut: Number of visits before coconut biodegrades
        """
        if not await self.start():
            return

        print(f"\n{'=' * 50}")
        print("🥥 COCONUTS FROM THE PALM-TREE 🌴")
        print(f"{'=' * 50}")
        print(f"Max concurrent coconuts: {self.config.max_concurrent}")
        print(f"Sites in rotation: {len(self.sites)}")
        print(f"Duration: {'Continuous' if duration_minutes == 0 else f'{duration_minutes} minutes'}")
        print(f"{'=' * 50}\n")

        try:
            tasks = []
            coconuts_spawned = 0
            start_time = datetime.now()

            while self.running:
                # Check duration
                if duration_minutes > 0:
                    elapsed = (datetime.now() - start_time).total_seconds() / 60
                    if elapsed >= duration_minutes:
                        print("[Coconut] Duration reached, stopping...")
                        break

                # Spawn coconuts up to max concurrent
                active_coconuts = len([t for t in tasks if not t.done()])

                if active_coconuts < self.config.max_concurrent:
                    coconut = await self.spawn_coconut()
                    if coconut:
                        coconuts_spawned += 1
                        task = asyncio.create_task(
                            self.run_coconut(coconut, visits_per_coconut)
                        )
                        tasks.append(task)

                # Wait before checking again
                await asyncio.sleep(self.config.spawn_delay)

                # Clean up completed tasks
                tasks = [t for t in tasks if not t.done()]

            # Wait for remaining tasks
            if tasks:
                print("[Coconut] Waiting for remaining coconuts to finish...")
                await asyncio.gather(*tasks, return_exceptions=True)

        except asyncio.CancelledError:
            print("[Coconut] Cancelled")
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Stop Coconut Mode and clean up resources."""
        self.running = False

        # Clean up coconuts
        for coconut in self.coconuts:
            try:
                await coconut.cleanup()
            except Exception:
                pass

        # Close browser
        if self.browser:
            await self.browser.close()

        # Close playwright
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

        self._print_stats()

    def _print_stats(self) -> None:
        """Print session statistics."""
        print(f"\n{'=' * 50}")
        print("Coconut Mode Complete")
        print(f"{'=' * 50}")
        print(f"Total visits: {self.stats['total_visits']}")
        print(f"Total errors: {self.stats['total_errors']}")
        print(f"Unique sites visited: {len(self.stats['sites_visited'])}")
        if self.stats['start_time']:
            duration = datetime.now() - self.stats['start_time']
            print(f"Duration: {duration}")


# Fallback mode when Playwright isn't available
class CoconutModeLite:
    """
    Lite version of Coconut Mode using httpx instead of Playwright.

    "When you can't have a full browser, make do with HTTP."

    This is a fallback that uses regular HTTP requests instead of
    headless browsers. Less realistic, but works without heavy dependencies.
    """

    def __init__(self, config: Optional[CoconutConfig] = None):
        self.config = config or CoconutConfig()
        self.sites = TOP_SITES
        self.running = False
        self.stats = {"visits": 0, "errors": 0}

    async def run(self, duration_minutes: int = 60) -> None:
        """Run the lite version using httpx."""
        try:
            import httpx
        except ImportError:
            print("[Coconut Lite] httpx not available. Install with: pip install httpx")
            return

        print("[Coconut Lite] Running in lite mode (HTTP only, no browser)")
        print("[Coconut Lite] For full browser mode: pip install playwright && playwright install")

        self.running = True
        start_time = datetime.now()

        async with httpx.AsyncClient(timeout=30.0) as client:
            while self.running:
                # Check duration
                if duration_minutes > 0:
                    elapsed = (datetime.now() - start_time).total_seconds() / 60
                    if elapsed >= duration_minutes:
                        break

                site = random.choice(self.sites)
                print(f"[Coconut Lite] Visiting: {site}")

                try:
                    response = await client.get(site, follow_redirects=True)
                    self.stats["visits"] += 1
                    print(f"[Coconut Lite] ✓ {response.status_code}")
                except Exception as e:
                    self.stats["errors"] += 1
                    print(f"[Coconut Lite] ✗ {e}")

                await asyncio.sleep(random.uniform(3, 10))

        print(f"\n[Coconut Lite] Complete: {self.stats['visits']} visits, {self.stats['errors']} errors")


# For testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Coconut Mode - Headless browser army")
    parser.add_argument("--lite", action="store_true", help="Use lite mode (HTTP only)")
    parser.add_argument("--duration", type=int, default=5, help="Duration in minutes")
    parser.add_argument("--concurrent", type=int, default=2, help="Max concurrent browsers")
    args = parser.parse_args()

    async def main():
        if args.lite or not PLAYWRIGHT_AVAILABLE:
            mode = CoconutModeLite()
            await mode.run(args.duration)
        else:
            config = CoconutConfig(max_concurrent=args.concurrent)
            mode = CoconutMode(config=config)
            await mode.run(duration_minutes=args.duration)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Coconut] Interrupted")
