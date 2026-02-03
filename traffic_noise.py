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
import math

# ============================================================================
# MARKOV CHAIN & CHAOS MATHEMATICS
# ============================================================================

class MarkovChain:
    """
    Markov chain for human-like browsing pattern transitions.

    "Because even chaos should have some method to its madness."
    """

    def __init__(self):
        # State transition probabilities for browsing categories
        # Rows: current state, Columns: next state probability
        self.category_transitions = {
            "Lifestyle": {"Lifestyle": 0.3, "World": 0.15, "Technology": 0.15, "Health": 0.15, "Trending": 0.15, "SocialMedia": 0.1},
            "World": {"Lifestyle": 0.1, "World": 0.35, "Technology": 0.15, "Health": 0.1, "Trending": 0.2, "SocialMedia": 0.1},
            "Technology": {"Lifestyle": 0.1, "World": 0.15, "Technology": 0.35, "Health": 0.1, "Trending": 0.15, "SocialMedia": 0.15},
            "Health": {"Lifestyle": 0.2, "World": 0.15, "Technology": 0.1, "Health": 0.35, "Trending": 0.1, "SocialMedia": 0.1},
            "Trending": {"Lifestyle": 0.15, "World": 0.2, "Technology": 0.15, "Health": 0.1, "Trending": 0.25, "SocialMedia": 0.15},
            "SocialMedia": {"Lifestyle": 0.15, "World": 0.15, "Technology": 0.2, "Health": 0.1, "Trending": 0.15, "SocialMedia": 0.25},
        }

        # Browsing pattern transitions
        self.pattern_transitions = {
            "normal": {"normal": 0.6, "bursty": 0.15, "slow": 0.15, "erratic": 0.1},
            "bursty": {"normal": 0.2, "bursty": 0.5, "slow": 0.1, "erratic": 0.2},
            "slow": {"normal": 0.3, "bursty": 0.1, "slow": 0.5, "erratic": 0.1},
            "erratic": {"normal": 0.15, "bursty": 0.25, "slow": 0.1, "erratic": 0.5},
        }

        self.current_category = random.choice(list(self.category_transitions.keys()))
        self.current_pattern = random.choice(list(self.pattern_transitions.keys()))

    def next_category(self) -> str:
        """Get next category based on Markov chain transition."""
        transitions = self.category_transitions.get(self.current_category, {})
        if not transitions:
            self.current_category = random.choice(list(self.category_transitions.keys()))
            return self.current_category

        categories = list(transitions.keys())
        probabilities = list(transitions.values())
        self.current_category = random.choices(categories, weights=probabilities, k=1)[0]
        return self.current_category

    def next_pattern(self) -> str:
        """Get next browsing pattern based on Markov chain transition."""
        transitions = self.pattern_transitions.get(self.current_pattern, {})
        if not transitions:
            self.current_pattern = random.choice(list(self.pattern_transitions.keys()))
            return self.current_pattern

        patterns = list(transitions.keys())
        probabilities = list(transitions.values())
        self.current_pattern = random.choices(patterns, weights=probabilities, k=1)[0]
        return self.current_pattern


class ChaosGenerator:
    """
    Chaos mathematics for generating unpredictable but deterministic timing.

    Uses the logistic map and other chaotic systems to create
    human-like irregular timing that still follows natural patterns.

    "Order within chaos, chaos within order."
    """

    def __init__(self, r: float = 3.9, seed: float = None):
        """
        Initialize chaos generator.

        Args:
            r: Control parameter for logistic map (3.57 < r <= 4.0 for chaos)
            seed: Initial value (0 < seed < 1)
        """
        self.r = r  # 3.9 gives good chaotic behavior
        self.x = seed if seed else random.random() * 0.5 + 0.25  # Start near middle
        self.iteration = 0

    def logistic_map(self) -> float:
        """
        Generate next value using the logistic map.

        x_{n+1} = r * x_n * (1 - x_n)

        This creates deterministic chaos - appears random but follows rules.
        """
        self.x = self.r * self.x * (1 - self.x)
        self.iteration += 1
        return self.x

    def henon_map(self, a: float = 1.4, b: float = 0.3) -> tuple:
        """
        Generate next point using the Hénon map for 2D chaos.

        Creates more complex chaotic patterns for multi-dimensional variation.
        """
        if not hasattr(self, 'y'):
            self.y = random.random() * 0.5 + 0.25

        new_x = 1 - a * self.x ** 2 + self.y
        new_y = b * self.x
        self.x = new_x
        self.y = new_y
        return (self.x, self.y)

    def get_chaos_delay(self, min_delay: float, max_delay: float) -> float:
        """
        Get a chaotic delay value that looks human-like.

        Uses logistic map combined with sinusoidal modulation for
        realistic browsing patterns.
        """
        # Base chaos value
        chaos_value = self.logistic_map()

        # Add sinusoidal "time of day" effect
        time_factor = math.sin(self.iteration * 0.1) * 0.3 + 1.0

        # Combine for final delay
        normalized = chaos_value * time_factor
        normalized = max(0.1, min(1.0, normalized))  # Clamp to [0.1, 1.0]

        delay = min_delay + (max_delay - min_delay) * normalized
        return delay

    def get_burst_count(self, min_burst: int = 1, max_burst: int = 8) -> int:
        """Get number of requests in a burst using chaos."""
        chaos_value = self.logistic_map()
        return int(min_burst + (max_burst - min_burst) * chaos_value)

    def should_switch_behavior(self, base_probability: float = 0.1) -> bool:
        """Determine if behavior should switch using chaos."""
        return self.logistic_map() < base_probability


# Global instances for chaos mode
markov_chain = MarkovChain()
chaos_generator = ChaosGenerator()


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
    max_headlines: int = 10  # Changed from 3 to show up to 10 headlines
    # Issue simulation modes
    simulate_issues: Optional[str] = None  # networking, hardware, software, malware, misconfigured, mixed
    use_markov: bool = True  # Use Markov chains for human-like browsing
    # Content filtering
    include_political: bool = False  # Include politically diverse sites
    include_tabloids: bool = False
    include_social: bool = False
    include_privacy: bool = False
    include_hobbies: bool = False
    # Custom feature: Persona mode
    persona: Optional[str] = None  # tech_enthusiast, news_junkie, privacy_advocate, etc.

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
    "SocialNetworkAds": [
        "https://www.dailymail.co.uk",
        "https://www.tmz.com",
        "https://www.unilad.com",
        "https://www.ladbible.com",
        "https://www.foxnews.com",
        "https://www.independent.co.uk",
        "https://www.politico.com",
        "https://www.mirror.co.uk",
        "https://www.euronews.com",
        "https://www.businessinsider.com",
        "https://www.msn.com",
        "https://www.windowscentral.com",
        "https://www.techradar.com",
        "https://www.bgr.com",
        "https://www.marketwatch.com",
        "https://www.bleacherreport.com",
        "https://www.eater.com",
    ],
    # ========================================================================
    # POLITICALLY DIVERSE NEWS SITES (50 Left-Leaning, 50 Right-Leaning)
    # ========================================================================
    "LeftLeaning": [
        "https://www.msnbc.com",
        "https://www.huffpost.com",
        "https://www.vox.com",
        "https://www.slate.com",
        "https://www.motherjones.com",
        "https://www.thenation.com",
        "https://www.theatlantic.com",
        "https://www.newyorker.com",
        "https://www.salon.com",
        "https://www.dailykos.com",
        "https://www.thinkprogress.org",
        "https://www.democracynow.org",
        "https://www.commondreams.org",
        "https://www.truthout.org",
        "https://www.alternet.org",
        "https://www.jacobinmag.com",
        "https://www.currentaffairs.org",
        "https://www.thedailybeast.com",
        "https://www.mediamatters.org",
        "https://www.rawstory.com",
        "https://www.crooksandliars.com",
        "https://www.washingtonmonthly.com",
        "https://www.prospect.org",
        "https://www.inthesetimes.com",
        "https://www.theintercept.com",
        "https://www.propublica.org",
        "https://www.rollingstone.com",
        "https://www.vanityfair.com",
        "https://www.esquire.com",
        "https://www.gq.com",
        "https://www.buzzfeednews.com",
        "https://www.vice.com",
        "https://www.vox.com/the-goods",
        "https://www.eater.com",
        "https://www.curbed.com",
        "https://www.theroot.com",
        "https://www.jezebel.com",
        "https://www.splinter.com",
        "https://www.talking pointsmemo.com",
        "https://www.palmerreport.com",
        "https://www.politicususa.com",
        "https://www.occupydemocrats.com",
        "https://www.bluedotdaily.com",
        "https://www.progressivetimes.com",
        "https://www.liberalamerica.org",
        "https://www.forwardprogressives.com",
        "https://www.bipartisanreport.com",
        "https://www.americannewsx.com",
        "https://www.newcenturytimes.com",
        "https://www.wonkette.com",
    ],
    "RightLeaning": [
        "https://www.foxnews.com",
        "https://www.breitbart.com",
        "https://www.dailywire.com",
        "https://www.theblaze.com",
        "https://www.newsmax.com",
        "https://www.oann.com",
        "https://www.washingtonexaminer.com",
        "https://www.nationalreview.com",
        "https://www.townhall.com",
        "https://www.redstate.com",
        "https://www.hotair.com",
        "https://www.pjmedia.com",
        "https://www.americanthinker.com",
        "https://www.thefederalist.com",
        "https://www.dailycaller.com",
        "https://www.freebeacon.com",
        "https://www.washingtonexaminer.com",
        "https://www.spectator.org",
        "https://www.weeklystandard.com",
        "https://www.commentary.org",
        "https://www.reason.com",
        "https://www.cato.org",
        "https://www.heritage.org",
        "https://www.aei.org",
        "https://www.manhattan-institute.org",
        "https://www.powerlineblog.com",
        "https://www.instapundit.com",
        "https://www.legalinsurrection.com",
        "https://www.twitchy.com",
        "https://www.ijr.com",
        "https://www.westernjournal.com",
        "https://www.lifezette.com",
        "https://www.lifenews.com",
        "https://www.cnsnews.com",
        "https://www.wnd.com",
        "https://www.thepostmillennial.com",
        "https://www.justthenews.com",
        "https://www.realclearpolitics.com",
        "https://www.theepochtimes.com",
        "https://www.zerohedge.com",
        "https://www.drudgereport.com",
        "https://www.lucianne.com",
        "https://www.frontpagemag.com",
        "https://www.americangreatness.com",
        "https://www.amren.com",
        "https://www.bizpacreview.com",
        "https://www.bongino.com",
        "https://www.chicksonright.com",
        "https://www.conservativereview.com",
        "https://www.rushlimbaugh.com",
    ],
    # ========================================================================
    # TABLOID SITES
    # ========================================================================
    "Tabloids": [
        "https://www.tmz.com",
        "https://www.dailymail.co.uk",
        "https://www.pagesix.com",
        "https://www.eonline.com",
        "https://www.usmagazine.com",
        "https://www.people.com",
        "https://www.etonline.com",
        "https://www.justjared.com",
        "https://www.perezhilton.com",
        "https://www.thesun.co.uk",
        "https://www.mirror.co.uk",
        "https://www.express.co.uk",
        "https://www.star-magazine.com",
        "https://www.intouchweekly.com",
        "https://www.lifeandstylemag.com",
        "https://www.okmagazine.com",
        "https://www.radaronline.com",
        "https://www.nationalenquirer.com",
        "https://www.globemagazine.com",
        "https://www.nydailynews.com",
    ],
    # ========================================================================
    # HOBBY & INTEREST SITES
    # ========================================================================
    "Hobbies": [
        "https://www.instructables.com",
        "https://www.craftsy.com",
        "https://www.ravelry.com",
        "https://www.allrecipes.com",
        "https://www.epicurious.com",
        "https://www.seriouseats.com",
        "https://www.bonappetit.com",
        "https://www.foodnetwork.com",
        "https://www.diynetwork.com",
        "https://www.hgtv.com",
        "https://www.gardeningknowhow.com",
        "https://www.finegardening.com",
        "https://www.bhg.com",
        "https://www.thespruce.com",
        "https://www.popularmechanics.com",
        "https://www.makeuseof.com",
        "https://www.hackaday.com",
        "https://www.adafruit.com",
        "https://www.sparkfun.com",
        "https://www.arduino.cc",
        "https://www.model-railroad-hobbyist.com",
        "https://www.rcgroups.com",
        "https://www.flitetest.com",
        "https://www.photographylife.com",
        "https://www.petapixel.com",
        "https://www.dpreview.com",
        "https://www.thepioneerwoman.com",
        "https://www.cookinglight.com",
        "https://www.delish.com",
        "https://www.tasty.co",
    ],
    # ========================================================================
    # SOCIAL MEDIA PLATFORMS (30 sites)
    # ========================================================================
    "SocialMedia": [
        "https://www.facebook.com",
        "https://www.twitter.com",
        "https://www.instagram.com",
        "https://www.tiktok.com",
        "https://www.snapchat.com",
        "https://www.pinterest.com",
        "https://www.linkedin.com",
        "https://www.reddit.com",
        "https://www.tumblr.com",
        "https://www.discord.com",
        "https://www.twitch.tv",
        "https://www.youtube.com",
        "https://www.vimeo.com",
        "https://www.dailymotion.com",
        "https://www.flickr.com",
        "https://www.500px.com",
        "https://www.deviantart.com",
        "https://www.behance.net",
        "https://www.dribbble.com",
        "https://www.medium.com",
        "https://www.quora.com",
        "https://www.clubhouse.com",
        "https://www.mastodon.social",
        "https://www.threads.net",
        "https://www.bluesky.social",
        "https://www.truth social.com",
        "https://www.parler.com",
        "https://www.gab.com",
        "https://www.minds.com",
        "https://www.mewe.com",
    ],
    # ========================================================================
    # ONLINE PRIVACY SITES
    # ========================================================================
    "Privacy": [
        "https://www.eff.org",
        "https://www.privacytools.io",
        "https://www.torproject.org",
        "https://www.privacyguides.org",
        "https://www.spreadprivacy.com",
        "https://www.epic.org",
        "https://www.accessnow.org",
        "https://www.fightforthefuture.org",
        "https://www.aclu.org",
        "https://www.cdt.org",
        "https://www.digitalrights.ie",
        "https://www.noyb.eu",
        "https://www.edri.org",
        "https://www.openrightsgroup.org",
        "https://www.techdirt.com",
        "https://www.schneier.com",
        "https://www.krebsonsecurity.com",
        "https://www.bleepingcomputer.com",
        "https://www.thehackernews.com",
        "https://www.darkreading.com",
    ],
    # ========================================================================
    # TECHNICAL ISSUE SEARCH PATTERNS
    # ========================================================================
    "NetworkingIssues": [
        "https://www.google.com/search?q=wifi+not+connecting",
        "https://www.google.com/search?q=dns+server+not+responding",
        "https://www.google.com/search?q=ethernet+no+internet",
        "https://www.google.com/search?q=slow+internet+connection+fix",
        "https://www.google.com/search?q=router+keeps+disconnecting",
        "https://www.google.com/search?q=ip+address+conflict",
        "https://www.google.com/search?q=port+forwarding+not+working",
        "https://www.google.com/search?q=vpn+connection+failed",
        "https://www.google.com/search?q=firewall+blocking+connection",
        "https://www.google.com/search?q=network+adapter+missing",
        "https://www.reddit.com/r/techsupport/search?q=wifi+issues",
        "https://www.reddit.com/r/HomeNetworking",
        "https://superuser.com/questions/tagged/networking",
        "https://networkengineering.stackexchange.com",
        "https://www.speedtest.net",
    ],
    "HardwareIssues": [
        "https://www.google.com/search?q=computer+won't+turn+on",
        "https://www.google.com/search?q=blue+screen+of+death+fix",
        "https://www.google.com/search?q=cpu+overheating+solutions",
        "https://www.google.com/search?q=ram+not+detected",
        "https://www.google.com/search?q=hard+drive+not+showing+up",
        "https://www.google.com/search?q=graphics+card+not+working",
        "https://www.google.com/search?q=monitor+no+signal",
        "https://www.google.com/search?q=keyboard+not+typing",
        "https://www.google.com/search?q=mouse+cursor+freezing",
        "https://www.google.com/search?q=usb+device+not+recognized",
        "https://www.reddit.com/r/buildapc",
        "https://www.reddit.com/r/techsupport",
        "https://www.tomshardware.com/forums",
        "https://forums.anandtech.com",
        "https://www.pcpartpicker.com",
    ],
    "SoftwareIssues": [
        "https://www.google.com/search?q=windows+update+stuck",
        "https://www.google.com/search?q=application+won't+open",
        "https://www.google.com/search?q=dll+file+missing+error",
        "https://www.google.com/search?q=program+keeps+crashing",
        "https://www.google.com/search?q=driver+installation+failed",
        "https://www.google.com/search?q=windows+won't+boot",
        "https://www.google.com/search?q=mac+spinning+wheel",
        "https://www.google.com/search?q=linux+kernel+panic",
        "https://www.google.com/search?q=browser+keeps+crashing",
        "https://www.google.com/search?q=software+compatibility+issues",
        "https://answers.microsoft.com",
        "https://support.apple.com",
        "https://askubuntu.com",
        "https://stackoverflow.com",
        "https://superuser.com",
    ],
    "MalwareIssues": [
        "https://www.google.com/search?q=remove+malware+from+computer",
        "https://www.google.com/search?q=computer+running+slow+virus",
        "https://www.google.com/search?q=popup+ads+won't+stop",
        "https://www.google.com/search?q=browser+hijacked+fix",
        "https://www.google.com/search?q=ransomware+recovery",
        "https://www.google.com/search?q=adware+removal+tool",
        "https://www.google.com/search?q=spyware+scan+free",
        "https://www.google.com/search?q=trojan+virus+removal",
        "https://www.google.com/search?q=computer+infected+signs",
        "https://www.google.com/search?q=antivirus+not+working",
        "https://www.malwarebytes.com",
        "https://www.avg.com",
        "https://www.avast.com",
        "https://www.kaspersky.com",
        "https://www.bleepingcomputer.com/virus-removal",
    ],
    "MisconfiguredSettings": [
        "https://www.google.com/search?q=windows+proxy+settings+wrong",
        "https://www.google.com/search?q=dns+settings+incorrect",
        "https://www.google.com/search?q=firewall+settings+blocking",
        "https://www.google.com/search?q=time+zone+sync+issues",
        "https://www.google.com/search?q=display+resolution+problems",
        "https://www.google.com/search?q=sound+output+wrong+device",
        "https://www.google.com/search?q=default+browser+change",
        "https://www.google.com/search?q=startup+programs+too+many",
        "https://www.google.com/search?q=power+settings+wrong",
        "https://www.google.com/search?q=privacy+settings+reset",
        "https://www.google.com/search?q=registry+settings+fix",
        "https://www.google.com/search?q=bios+settings+wrong",
        "https://www.howtogeek.com",
        "https://www.lifehacker.com",
        "https://www.pcworld.com",
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
    "https://meta.com/",
    "https://business.facebook.com/",
    "https://twitter.com/",
    "https://www.reddit.com/",
    "https://www.microsoft.com/",
    "https://instagram.com/",
    "https://www.instagram.com/",
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

def get_random_news_url(config: Config = None, use_markov: bool = False) -> tuple[str, str]:
    """
    Get a random news URL, optionally using Markov chain for human-like browsing.

    Args:
        config: Configuration object for filtering categories
        use_markov: Whether to use Markov chain for category selection
    """
    # Build list of available categories based on config
    available_categories = ["Lifestyle", "World", "Technology", "Health", "Trending", "SocialNetworkAds"]

    if config:
        # Add optional categories if enabled
        if config.include_political:
            available_categories.extend(["LeftLeaning", "RightLeaning"])
        if config.include_tabloids:
            available_categories.append("Tabloids")
        if config.include_social:
            available_categories.append("SocialMedia")
        if config.include_privacy:
            available_categories.append("Privacy")
        if config.include_hobbies:
            available_categories.append("Hobbies")

        # Handle issue simulation mode
        if config.simulate_issues:
            issue_categories = {
                "networking": ["NetworkingIssues"],
                "hardware": ["HardwareIssues"],
                "software": ["SoftwareIssues"],
                "malware": ["MalwareIssues"],
                "misconfigured": ["MisconfiguredSettings"],
                "mixed": ["NetworkingIssues", "HardwareIssues", "SoftwareIssues",
                         "MalwareIssues", "MisconfiguredSettings"],
            }
            if config.simulate_issues in issue_categories:
                # Mix issue searches with regular browsing (30% issues, 70% regular)
                if random.random() < 0.3:
                    issue_cats = issue_categories[config.simulate_issues]
                    category = random.choice(issue_cats)
                    if category in NEWS_SITES:
                        url = random.choice(NEWS_SITES[category])
                        return category, url

        # Handle persona mode
        if config.persona:
            persona_categories = get_persona_categories(config.persona)
            if persona_categories:
                available_categories = persona_categories

    # Filter to categories that exist in NEWS_SITES
    available_categories = [c for c in available_categories if c in NEWS_SITES]

    if not available_categories:
        available_categories = list(NEWS_SITES.keys())

    # Select category using Markov chain or random
    if use_markov and config and config.chaos_mode:
        # Update Markov chain with available categories
        category = markov_chain.next_category()
        if category not in available_categories:
            category = random.choice(available_categories)
    else:
        category = random.choice(available_categories)

    url = random.choice(NEWS_SITES[category])
    return category, url


def get_persona_categories(persona: str) -> List[str]:
    """Get preferred categories for a persona type."""
    personas = {
        "tech_enthusiast": ["Technology", "Privacy", "Hobbies"],
        "news_junkie": ["World", "Trending", "LeftLeaning", "RightLeaning"],
        "privacy_advocate": ["Privacy", "Technology"],
        "social_butterfly": ["SocialMedia", "Lifestyle", "Trending"],
        "entertainment_seeker": ["Tabloids", "SocialMedia", "Lifestyle"],
        "health_conscious": ["Health", "Lifestyle", "Hobbies"],
        "political_observer": ["LeftLeaning", "RightLeaning", "World", "Trending"],
        "hobbyist": ["Hobbies", "Technology", "Lifestyle"],
        "troubleshooter": ["NetworkingIssues", "HardwareIssues", "SoftwareIssues",
                          "MalwareIssues", "Technology"],
    }
    return personas.get(persona, [])


def get_pattern_delay(pattern: str, chaos: bool = False, use_chaos_math: bool = False) -> float:
    """
    Get delay based on browsing pattern.

    Args:
        pattern: Browsing pattern type
        chaos: Whether chaos mode is enabled
        use_chaos_math: Whether to use chaos mathematics for timing
    """
    if chaos and use_chaos_math:
        # Use chaos generator for more human-like timing
        return chaos_generator.get_chaos_delay(CHAOS_MIN_DELAY, CHAOS_MAX_DELAY)
    elif chaos:
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

    # Initialize per-worker chaos generator for variety
    worker_chaos = ChaosGenerator(r=3.85 + worker_id * 0.01)

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
                    # Use Markov chain for human-like category selection in chaos mode
                    category, url = get_random_news_url(
                        config=config,
                        use_markov=(config.chaos_mode and config.use_markov)
                    )
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

                # Delay based on pattern - use chaos mathematics in chaos mode
                delay = get_pattern_delay(
                    pattern,
                    config.chaos_mode,
                    use_chaos_math=(config.chaos_mode and config.use_markov)
                )

                # Chaos mode: use Markov chain to decide pattern transitions
                if config.chaos_mode:
                    if config.use_markov:
                        # Use Markov chain for pattern transitions
                        if worker_chaos.should_switch_behavior(0.15):
                            pattern = markov_chain.next_pattern()
                    elif random.random() < 0.1:
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
                        help="Chaos mode - erratic multi-bot simulation with Markov chains")
    parser.add_argument("-w", "--workers", type=int, default=3, metavar="NUM",
                        help="Number of parallel workers (default: 3, max: 30)")
    parser.add_argument("-d", "--duration", type=int, default=0, metavar="MINS",
                        help="Run duration in minutes (default: continuous)")
    parser.add_argument("-i", "--interface", type=str, default="eth0",
                        help="Network interface (default: eth0)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Minimal output")
    parser.add_argument("--max-headlines", type=int, default=10,
                        help="Max headlines to display (default: 10)")

    # Chaos mode enhancements
    parser.add_argument("--no-markov", action="store_true",
                        help="Disable Markov chains in chaos mode (use pure random)")

    # Issue simulation options
    issue_group = parser.add_argument_group("Issue Simulation",
                        "Generate traffic that simulates various technical issues")
    issue_group.add_argument("--simulate-issues", type=str, metavar="TYPE",
                        choices=["networking", "hardware", "software", "malware",
                                "misconfigured", "mixed"],
                        help="Simulate traffic for technical issues")

    # Content category options
    content_group = parser.add_argument_group("Content Categories",
                        "Include additional content categories")
    content_group.add_argument("--include-political", action="store_true",
                        help="Include politically diverse sites (50 left, 50 right)")
    content_group.add_argument("--include-tabloids", action="store_true",
                        help="Include tabloid/entertainment sites")
    content_group.add_argument("--include-social", action="store_true",
                        help="Include social media platforms")
    content_group.add_argument("--include-privacy", action="store_true",
                        help="Include privacy-focused sites")
    content_group.add_argument("--include-hobbies", action="store_true",
                        help="Include hobby and interest sites")
    content_group.add_argument("--include-all", action="store_true",
                        help="Include all content categories")

    # Persona mode (custom feature)
    persona_group = parser.add_argument_group("Persona Mode",
                        "Simulate browsing as a specific user type")
    persona_group.add_argument("--persona", type=str, metavar="TYPE",
                        choices=["tech_enthusiast", "news_junkie", "privacy_advocate",
                                "social_butterfly", "entertainment_seeker",
                                "health_conscious", "political_observer",
                                "hobbyist", "troubleshooter"],
                        help="Browse as a specific persona type")
    persona_group.add_argument("--list-personas", action="store_true",
                        help="List available persona types")

    args = parser.parse_args()

    # Handle --list-personas
    if args.list_personas:
        print("\n🎭 Available Personas:\n")
        personas = {
            "tech_enthusiast": "Browses technology, privacy, and hobby sites",
            "news_junkie": "Follows world news and trending topics across political spectrum",
            "privacy_advocate": "Focuses on privacy tools and security resources",
            "social_butterfly": "Active on social media, lifestyle, and trending content",
            "entertainment_seeker": "Tabloids, social media, and entertainment sites",
            "health_conscious": "Health, wellness, lifestyle, and hobby content",
            "political_observer": "Political news from multiple perspectives",
            "hobbyist": "DIY, crafts, cooking, and technology projects",
            "troubleshooter": "Technical support searches and problem-solving",
        }
        for name, desc in personas.items():
            print(f"  {name:22} - {desc}")
        print("\nUsage: python traffic_noise.py --persona tech_enthusiast -c\n")
        return

    # Handle --include-all
    if args.include_all:
        args.include_political = True
        args.include_tabloids = True
        args.include_social = True
        args.include_privacy = True
        args.include_hobbies = True

    # Build config
    config = Config(
        mode="vps" if args.vps else "news",
        vps_target=args.vps,
        show_headlines=not args.no_headlines,
        randomize_identity=args.randomize_id,
        chaos_mode=args.chaos,
        parallel_workers=min(max(args.workers, 1), 30),
        duration=args.duration,
        interface=args.interface,
        quiet=args.quiet,
        max_headlines=args.max_headlines,
        simulate_issues=args.simulate_issues,
        use_markov=not args.no_markov,
        include_political=args.include_political,
        include_tabloids=args.include_tabloids,
        include_social=args.include_social,
        include_privacy=args.include_privacy,
        include_hobbies=args.include_hobbies,
        persona=args.persona,
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
