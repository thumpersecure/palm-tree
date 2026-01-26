#!/usr/bin/env python3
"""
Personality Modes - Because normal browsing is for normies.

🎭 BROWSE LIKE SOMEONE ELSE (OR SOMETHING ELSE) 🎭

These modes don't just generate traffic - they generate CHARACTERS.
Each personality has its own browsing patterns, site preferences,
and existential crises.

WARNING: Side effects may include:
- Your ISP thinking you need therapy
- Ad algorithms having breakdowns
- Trackers filing restraining orders
"""

import asyncio
import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from datetime import datetime, time
import math


@dataclass
class PersonalityProfile:
    """
    A complete browsing personality.

    "Today I'm not me. Today I'm... *checks notes* ...a sleep-deprived
    philosophy major who day-trades crypto and has strong opinions about fonts."
    """
    name: str
    description: str
    site_categories: Dict[str, float]  # category -> weight
    active_hours: tuple  # (start_hour, end_hour)
    typing_speed: str  # "hunt_and_peck", "normal", "caffeinated", "possessed"
    attention_span: str  # "goldfish", "normal", "hyperfocus", "adhd"
    chaos_level: float  # 0.0 - 1.0
    catchphrase: str


# ============================================================================
# THE PERSONALITIES (Choose your fighter)
# ============================================================================

PERSONALITIES = {
    "paranoid": PersonalityProfile(
        name="The Paranoid Privacy Nut",
        description="Thinks everyone is watching. Because they are. Probably.",
        site_categories={
            "privacy_tools": 0.3,
            "vpn_reviews": 0.2,
            "conspiracy": 0.15,
            "security_news": 0.15,
            "encryption": 0.1,
            "off_grid_living": 0.1,
        },
        active_hours=(2, 5),  # Only browses at 2-5am like a true paranoid
        typing_speed="hunt_and_peck",  # Types slowly, checking over shoulder
        attention_span="adhd",  # Constantly switching tabs
        chaos_level=0.8,
        catchphrase="They're definitely watching this request..."
    ),

    "drunk": PersonalityProfile(
        name="Friday Night Browser",
        description="It's always Friday night somewhere. Browsing gets progressively worse.",
        site_categories={
            "social_media": 0.25,
            "food_delivery": 0.2,
            "ex_stalking": 0.15,  # We've all been there
            "online_shopping": 0.15,
            "youtube_rabbit_holes": 0.15,
            "regrettable_purchases": 0.1,
        },
        active_hours=(22, 3),  # 10pm - 3am
        typing_speed="possessed",  # Erratic, lots of typos
        attention_span="goldfish",
        chaos_level=0.95,
        catchphrase="I shoul defintiely buy this at 2am..."
    ),

    "existential": PersonalityProfile(
        name="The Existential Crisis",
        description="Googles 'why are we here' at 3am. Buys self-help books. Repeats.",
        site_categories={
            "philosophy": 0.25,
            "self_help": 0.2,
            "meditation_apps": 0.15,
            "career_change": 0.15,
            "meaning_of_life": 0.15,
            "amazon_self_help": 0.1,
        },
        active_hours=(1, 4),  # Peak existential crisis hours
        typing_speed="normal",
        attention_span="hyperfocus",  # Deep rabbit holes
        chaos_level=0.5,
        catchphrase="What even IS the internet, really?"
    ),

    "corporate": PersonalityProfile(
        name="The LinkedIn Lunatic",
        description="Synergizes deliverables. Circles back. Thinks 'hustle' is a personality.",
        site_categories={
            "linkedin": 0.3,
            "business_news": 0.2,
            "productivity_apps": 0.15,
            "thought_leadership": 0.15,
            "startup_news": 0.1,
            "expensive_coffee": 0.1,
        },
        active_hours=(5, 22),  # Grinds 5am-10pm because "sleep is for the weak"
        typing_speed="caffeinated",
        attention_span="normal",
        chaos_level=0.3,
        catchphrase="Let's take this offline and circle back..."
    ),

    "gamer": PersonalityProfile(
        name="The Gamer",
        description="Has opinions about frame rates. Strong ones. Will tell you about them.",
        site_categories={
            "gaming_news": 0.25,
            "twitch": 0.2,
            "reddit_gaming": 0.15,
            "hardware_reviews": 0.15,
            "discord": 0.15,
            "energy_drinks": 0.1,
        },
        active_hours=(16, 4),  # 4pm - 4am (no sleep, only game)
        typing_speed="caffeinated",
        attention_span="adhd",  # Alt-tabbing constantly
        chaos_level=0.7,
        catchphrase="It's not lag, it's the servers..."
    ),

    "boomer": PersonalityProfile(
        name="The Tech-Confused Parent",
        description="Clicks every popup. Types google.com into Google. Sends chain emails.",
        site_categories={
            "facebook": 0.3,
            "weather": 0.2,
            "news_home_page": 0.15,
            "chain_emails": 0.15,
            "grandkid_photos": 0.1,
            "scam_susceptible": 0.1,
        },
        active_hours=(6, 20),  # Normal hours, as God intended
        typing_speed="hunt_and_peck",
        attention_span="normal",
        chaos_level=0.2,
        catchphrase="Is this the Google? How do I print this?"
    ),

    "doomscroller": PersonalityProfile(
        name="The Doomscroller",
        description="Refreshes news every 30 seconds. Knows it's bad. Can't stop.",
        site_categories={
            "breaking_news": 0.3,
            "twitter_discourse": 0.25,
            "reddit_news": 0.2,
            "apocalypse_prep": 0.15,
            "anxiety_symptoms": 0.1,
        },
        active_hours=(0, 24),  # Never stops. Never.
        typing_speed="caffeinated",
        attention_span="goldfish",  # Refresh refresh refresh
        chaos_level=0.85,
        catchphrase="Just one more refresh then I'll sleep..."
    ),

    "catperson": PersonalityProfile(
        name="The Cat Person",
        description="Every search somehow leads back to cats. It's a gift.",
        site_categories={
            "cat_videos": 0.3,
            "cat_adoption": 0.2,
            "cat_products": 0.2,
            "cat_subreddits": 0.15,
            "cat_facts": 0.1,
            "dogs_are_okay_too": 0.05,
        },
        active_hours=(0, 24),  # Cats don't sleep, neither do cat people
        typing_speed="normal",
        attention_span="hyperfocus",  # On cats specifically
        chaos_level=0.4,
        catchphrase="Did you know cats have over 20 vocalizations?"
    ),

    "crypto_bro": PersonalityProfile(
        name="The Crypto Bro",
        description="Diamond hands. Paper brain. HODL mentality.",
        site_categories={
            "crypto_prices": 0.3,
            "crypto_twitter": 0.2,
            "trading_charts": 0.2,
            "lambo_dealerships": 0.1,
            "copium_reddit": 0.1,
            "bankruptcy_lawyers": 0.1,  # Just in case
        },
        active_hours=(0, 24),  # Markets never sleep
        typing_speed="possessed",  # Panic checking
        attention_span="goldfish",  # Chart check. Chart check. Chart check.
        chaos_level=0.9,
        catchphrase="This is good for Bitcoin actually..."
    ),

    "3am_you": PersonalityProfile(
        name="3am You",
        description="It's you. At 3am. We both know what happens at 3am.",
        site_categories={
            "youtube_weird": 0.25,
            "wikipedia_rabbit_holes": 0.2,
            "online_shopping": 0.15,
            "weird_questions": 0.15,
            "snacks_delivery": 0.15,
            "existential_searches": 0.1,
        },
        active_hours=(2, 5),
        typing_speed="caffeinated",
        attention_span="adhd",
        chaos_level=1.0,  # Pure chaos
        catchphrase="I'll just watch one more video..."
    ),
}


# Site lists for each category
PERSONALITY_SITES = {
    # Paranoid
    "privacy_tools": [
        "https://www.privacytools.io",
        "https://www.eff.org",
        "https://www.torproject.org",
    ],
    "vpn_reviews": [
        "https://www.vpnmentor.com",
        "https://www.comparitech.com/vpn/",
    ],
    "conspiracy": [
        "https://www.reddit.com/r/conspiracy",
        "https://www.abovetopsecret.com",
    ],
    "security_news": [
        "https://www.schneier.com",
        "https://krebsonsecurity.com",
        "https://www.bleepingcomputer.com",
    ],
    "encryption": [
        "https://www.gnupg.org",
        "https://signal.org",
    ],
    "off_grid_living": [
        "https://www.reddit.com/r/preppers",
        "https://www.survivalistboards.com",
    ],

    # Drunk
    "social_media": [
        "https://www.instagram.com",
        "https://www.twitter.com",
        "https://www.tiktok.com",
    ],
    "food_delivery": [
        "https://www.doordash.com",
        "https://www.ubereats.com",
        "https://www.grubhub.com",
    ],
    "ex_stalking": [
        "https://www.facebook.com",
        "https://www.instagram.com",
        "https://www.linkedin.com",  # "Just checking if they got promoted"
    ],
    "online_shopping": [
        "https://www.amazon.com",
        "https://www.ebay.com",
        "https://www.wish.com",  # Regret incoming
    ],
    "youtube_rabbit_holes": [
        "https://www.youtube.com",
    ],
    "regrettable_purchases": [
        "https://www.amazon.com",
        "https://www.aliexpress.com",
        "https://www.wish.com",
    ],

    # Existential
    "philosophy": [
        "https://plato.stanford.edu",
        "https://www.reddit.com/r/philosophy",
        "https://existentialcomics.com",
    ],
    "self_help": [
        "https://www.psychologytoday.com",
        "https://www.goodreads.com",
        "https://www.ted.com",
    ],
    "meditation_apps": [
        "https://www.headspace.com",
        "https://www.calm.com",
    ],
    "career_change": [
        "https://www.indeed.com",
        "https://www.glassdoor.com",
        "https://www.linkedin.com",
    ],
    "meaning_of_life": [
        "https://www.google.com/search?q=meaning+of+life",
        "https://en.wikipedia.org/wiki/Meaning_of_life",
    ],
    "amazon_self_help": [
        "https://www.amazon.com/s?k=self+help+books",
    ],

    # Corporate
    "linkedin": [
        "https://www.linkedin.com",
        "https://www.linkedin.com/feed/",
    ],
    "business_news": [
        "https://www.bloomberg.com",
        "https://www.wsj.com",
        "https://www.forbes.com",
    ],
    "productivity_apps": [
        "https://www.notion.so",
        "https://www.asana.com",
        "https://slack.com",
    ],
    "thought_leadership": [
        "https://hbr.org",
        "https://www.medium.com",
    ],
    "startup_news": [
        "https://techcrunch.com",
        "https://www.ycombinator.com/news",
    ],
    "expensive_coffee": [
        "https://www.bluebottlecoffee.com",
        "https://www.starbucks.com",
    ],

    # Gamer
    "gaming_news": [
        "https://www.ign.com",
        "https://www.gamespot.com",
        "https://www.polygon.com",
    ],
    "twitch": [
        "https://www.twitch.tv",
    ],
    "reddit_gaming": [
        "https://www.reddit.com/r/gaming",
        "https://www.reddit.com/r/pcgaming",
    ],
    "hardware_reviews": [
        "https://www.tomshardware.com",
        "https://www.pcgamer.com",
    ],
    "discord": [
        "https://discord.com",
    ],
    "energy_drinks": [
        "https://www.redbull.com",
        "https://www.monsterenergy.com",
    ],

    # Boomer
    "facebook": [
        "https://www.facebook.com",
    ],
    "weather": [
        "https://www.weather.com",
        "https://www.accuweather.com",
    ],
    "news_home_page": [
        "https://www.cnn.com",
        "https://www.foxnews.com",
        "https://www.msnbc.com",
    ],
    "chain_emails": [
        "https://mail.google.com",
        "https://outlook.live.com",
    ],
    "grandkid_photos": [
        "https://www.facebook.com",
        "https://photos.google.com",
    ],
    "scam_susceptible": [
        "https://www.google.com/search?q=free+iphone",
        "https://www.google.com/search?q=you+won",
    ],

    # Doomscroller
    "breaking_news": [
        "https://www.cnn.com",
        "https://www.bbc.com",
        "https://www.reuters.com",
        "https://apnews.com",
    ],
    "twitter_discourse": [
        "https://www.twitter.com",
        "https://www.twitter.com/explore",
    ],
    "reddit_news": [
        "https://www.reddit.com/r/news",
        "https://www.reddit.com/r/worldnews",
    ],
    "apocalypse_prep": [
        "https://www.reddit.com/r/preppers",
        "https://www.ready.gov",
    ],
    "anxiety_symptoms": [
        "https://www.webmd.com",
        "https://www.mayoclinic.org",
    ],

    # Cat Person
    "cat_videos": [
        "https://www.youtube.com/results?search_query=cats",
        "https://www.tiktok.com/tag/cats",
    ],
    "cat_adoption": [
        "https://www.petfinder.com",
        "https://www.adoptapet.com",
    ],
    "cat_products": [
        "https://www.chewy.com",
        "https://www.amazon.com/s?k=cat+supplies",
    ],
    "cat_subreddits": [
        "https://www.reddit.com/r/cats",
        "https://www.reddit.com/r/CatAdvice",
        "https://www.reddit.com/r/IllegallySmolCats",
    ],
    "cat_facts": [
        "https://en.wikipedia.org/wiki/Cat",
    ],
    "dogs_are_okay_too": [
        "https://www.reddit.com/r/dogs",  # For balance
    ],

    # Crypto Bro
    "crypto_prices": [
        "https://www.coinmarketcap.com",
        "https://www.coingecko.com",
    ],
    "crypto_twitter": [
        "https://www.twitter.com/search?q=bitcoin",
        "https://www.twitter.com/search?q=crypto",
    ],
    "trading_charts": [
        "https://www.tradingview.com",
        "https://www.binance.com",
    ],
    "lambo_dealerships": [
        "https://www.lamborghini.com",
        "https://www.ferrari.com",  # Diversified portfolio
    ],
    "copium_reddit": [
        "https://www.reddit.com/r/cryptocurrency",
        "https://www.reddit.com/r/wallstreetbets",
    ],
    "bankruptcy_lawyers": [
        "https://www.google.com/search?q=bankruptcy+lawyer+near+me",
    ],

    # 3am You
    "youtube_weird": [
        "https://www.youtube.com",
        "https://www.youtube.com/results?search_query=oddly+satisfying",
    ],
    "wikipedia_rabbit_holes": [
        "https://en.wikipedia.org/wiki/Special:Random",
        "https://en.wikipedia.org/wiki/List_of_unusual_deaths",
    ],
    "weird_questions": [
        "https://www.google.com/search?q=why+do+we+yawn",
        "https://www.google.com/search?q=how+many+ants+are+there",
        "https://www.google.com/search?q=can+fish+feel+pain",
    ],
    "snacks_delivery": [
        "https://www.doordash.com",
        "https://www.instacart.com",
    ],
    "existential_searches": [
        "https://www.google.com/search?q=am+i+happy",
        "https://www.google.com/search?q=what+should+i+do+with+my+life",
    ],
}


class PersonalityMode:
    """
    Run traffic generation as a specific personality.

    "Method acting, but for HTTP requests."
    """

    def __init__(
        self,
        personality: str = "paranoid",
        fetch_callback: Optional[Callable] = None,
    ):
        if personality not in PERSONALITIES:
            available = ", ".join(PERSONALITIES.keys())
            raise ValueError(f"Unknown personality: {personality}. Available: {available}")

        self.profile = PERSONALITIES[personality]
        self.fetch_callback = fetch_callback
        self.running = False
        self.stats = {
            "requests": 0,
            "start_time": None,
        }

    def _get_delay(self) -> float:
        """Get delay based on attention span."""
        delays = {
            "goldfish": (1, 10),      # Quick switching
            "normal": (10, 60),       # Normal human
            "hyperfocus": (60, 300),  # Deep dives
            "adhd": (5, 120),         # Wildly variable
        }
        min_delay, max_delay = delays.get(self.profile.attention_span, (10, 60))

        # Add chaos factor
        if random.random() < self.profile.chaos_level:
            max_delay *= 2

        return random.uniform(min_delay, max_delay)

    def _is_active_hour(self) -> bool:
        """Check if current hour is within active hours."""
        current_hour = datetime.now().hour
        start, end = self.profile.active_hours

        if start < end:
            return start <= current_hour < end
        else:  # Crosses midnight
            return current_hour >= start or current_hour < end

    def _select_site(self) -> str:
        """Select a site based on personality preferences."""
        # Weight categories
        categories = list(self.profile.site_categories.keys())
        weights = list(self.profile.site_categories.values())

        selected_category = random.choices(categories, weights=weights, k=1)[0]

        # Get sites for category
        sites = PERSONALITY_SITES.get(selected_category, ["https://www.google.com"])

        return random.choice(sites)

    async def run(self, duration_minutes: int = 60) -> None:
        """Run the personality mode."""
        self.running = True
        self.stats["start_time"] = datetime.now()

        print(f"\n{'=' * 60}")
        print(f"🎭 PERSONALITY MODE: {self.profile.name}")
        print(f"   {self.profile.description}")
        print(f"   Catchphrase: \"{self.profile.catchphrase}\"")
        print(f"{'=' * 60}\n")

        end_time = datetime.now().timestamp() + (duration_minutes * 60)

        while self.running and datetime.now().timestamp() < end_time:
            try:
                # Check if we should be active
                if not self._is_active_hour():
                    print(f"[{self.profile.name}] Not active hours. Waiting...")
                    await asyncio.sleep(300)  # Check again in 5 min
                    continue

                # Select and visit site
                site = self._select_site()
                print(f"[{self.profile.name}] {self.profile.catchphrase}")
                print(f"[{self.profile.name}] Visiting: {site}")

                if self.fetch_callback:
                    await self.fetch_callback(site)

                self.stats["requests"] += 1

                # Delay based on personality
                delay = self._get_delay()
                print(f"[{self.profile.name}] Next request in {delay:.0f}s")
                await asyncio.sleep(delay)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[{self.profile.name}] Error: {e}")
                await asyncio.sleep(30)

        self.running = False
        self._print_stats()

    def _print_stats(self) -> None:
        """Print session statistics."""
        print(f"\n{'=' * 60}")
        print(f"🎭 {self.profile.name} Session Complete")
        print(f"   Requests: {self.stats['requests']}")
        print(f"   Final words: \"{self.profile.catchphrase}\"")
        print(f"{'=' * 60}")

    def stop(self) -> None:
        """Stop the personality mode."""
        self.running = False


def list_personalities() -> None:
    """Print all available personalities."""
    print("\n🎭 AVAILABLE PERSONALITIES 🎭\n")
    print("=" * 70)

    for name, profile in PERSONALITIES.items():
        print(f"\n  --personality {name}")
        print(f"  Name: {profile.name}")
        print(f"  Description: {profile.description}")
        print(f"  Active hours: {profile.active_hours[0]}:00 - {profile.active_hours[1]}:00")
        print(f"  Chaos level: {'🔥' * int(profile.chaos_level * 5)}")
        print(f"  Catchphrase: \"{profile.catchphrase}\"")

    print("\n" + "=" * 70)
    print("\nUsage: python coconuts.py --personality paranoid")
    print("       python coconuts.py --personality drunk")
    print("       python coconuts.py --personality 3am_you\n")


# For testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_personalities()
    else:
        async def test():
            mode = PersonalityMode("paranoid")
            await mode.run(duration_minutes=2)

        asyncio.run(test())
