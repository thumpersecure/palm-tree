#!/usr/bin/env python3
"""
Traffic Noise Generator v3.3 - Python Version with Dynamic Terminal UI

"I'm not paranoid, I'm just really popular with advertisers."
    - Every user of this tool

Generates randomized network traffic to obscure browsing patterns.
Features live headline display, Markov chains, chaos mathematics,
stealth mode, scheduled profiles, and decoy data injection.

Side effects may include:
- Confused ad algorithms
- Data brokers questioning their career choices
- A sudden increase in ads for PlayStation 5s and Samsung Smart Fridges
- The warm fuzzy feeling of digital privacy

Not responsible for any existential crises caused to tracking scripts.
"""

__version__ = "3.3"
__author__ = "palm-tree"

import asyncio
import argparse
import random
import string
import hashlib
import socket
import signal
import sys
import re
import json
import os
import math
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, List, Deque, Dict, Any, Callable
from collections import deque
from contextlib import suppress
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.style import Style
from rich.prompt import Prompt, Confirm, IntPrompt
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
# TAXI CAB DRIVER JOKES (for --help)
# ============================================================================

TAXI_JOKES = [
    "Why did the taxi driver get fired? He kept driving his customers away!",
    "What's a taxi driver's favorite music? Car-tunes!",
    "Why don't taxi drivers ever get lost? They always take the scenic route on purpose!",
    "What did the taxi say to the fare? 'You're my type - the paying kind!'",
    "Why did the taxi driver bring a ladder? He heard the fares were going up!",
    "How do taxi drivers stay cool? They roll with the windows down and the meter up!",
    "What's a taxi driver's least favorite game? Hide and seek - nobody wants to be found!",
    "Why did the passenger tip the taxi driver? Because he couldn't meter expectations!",
    "What do you call a taxi driver who loves math? A fare calculator!",
    "Why did the taxi break up with the bus? It needed more personal space!",
    "What's a taxi driver's favorite exercise? Running the meter!",
    "Why don't taxis ever get lonely? They're always picking people up!",
]

# ============================================================================
# MARKOV CHAIN & CHAOS MATHEMATICS
# ============================================================================

class MarkovChain:
    """Markov chain for human-like browsing pattern transitions."""

    def __init__(self):
        self.category_transitions = {
            "Lifestyle": {"Lifestyle": 0.3, "World": 0.15, "Technology": 0.15, "Health": 0.15, "Trending": 0.15, "SocialMedia": 0.1},
            "World": {"Lifestyle": 0.1, "World": 0.35, "Technology": 0.15, "Health": 0.1, "Trending": 0.2, "SocialMedia": 0.1},
            "Technology": {"Lifestyle": 0.1, "World": 0.15, "Technology": 0.35, "Health": 0.1, "Trending": 0.15, "SocialMedia": 0.15},
            "Health": {"Lifestyle": 0.2, "World": 0.15, "Technology": 0.1, "Health": 0.35, "Trending": 0.1, "SocialMedia": 0.1},
            "Trending": {"Lifestyle": 0.15, "World": 0.2, "Technology": 0.15, "Health": 0.1, "Trending": 0.25, "SocialMedia": 0.15},
            "SocialMedia": {"Lifestyle": 0.15, "World": 0.15, "Technology": 0.2, "Health": 0.1, "Trending": 0.15, "SocialMedia": 0.25},
        }
        self.pattern_transitions = {
            "normal": {"normal": 0.6, "bursty": 0.15, "slow": 0.15, "erratic": 0.1},
            "bursty": {"normal": 0.2, "bursty": 0.5, "slow": 0.1, "erratic": 0.2},
            "slow": {"normal": 0.3, "bursty": 0.1, "slow": 0.5, "erratic": 0.1},
            "erratic": {"normal": 0.15, "bursty": 0.25, "slow": 0.1, "erratic": 0.5},
        }
        self.current_category = random.choice(list(self.category_transitions.keys()))
        self.current_pattern = random.choice(list(self.pattern_transitions.keys()))

    def next_category(self) -> str:
        transitions = self.category_transitions.get(self.current_category, {})
        if not transitions:
            self.current_category = random.choice(list(self.category_transitions.keys()))
            return self.current_category
        categories = list(transitions.keys())
        probabilities = list(transitions.values())
        self.current_category = random.choices(categories, weights=probabilities, k=1)[0]
        return self.current_category

    def next_pattern(self) -> str:
        transitions = self.pattern_transitions.get(self.current_pattern, {})
        if not transitions:
            self.current_pattern = random.choice(list(self.pattern_transitions.keys()))
            return self.current_pattern
        patterns = list(transitions.keys())
        probabilities = list(transitions.values())
        self.current_pattern = random.choices(patterns, weights=probabilities, k=1)[0]
        return self.current_pattern


class ChaosGenerator:
    """Chaos mathematics for unpredictable but deterministic timing."""

    def __init__(self, r: float = 3.9, seed: float = None):
        self.r = r
        self.x = seed if seed else random.random() * 0.5 + 0.25
        self.iteration = 0

    def logistic_map(self) -> float:
        self.x = self.r * self.x * (1 - self.x)
        self.iteration += 1
        return self.x

    def get_chaos_delay(self, min_delay: float, max_delay: float) -> float:
        chaos_value = self.logistic_map()
        time_factor = math.sin(self.iteration * 0.1) * 0.3 + 1.0
        normalized = max(0.1, min(1.0, chaos_value * time_factor))
        return min_delay + (max_delay - min_delay) * normalized

    def should_switch_behavior(self, base_probability: float = 0.1) -> bool:
        return self.logistic_map() < base_probability


# ============================================================================
# STEALTH MODE - TLS/HTTP FINGERPRINT RANDOMIZATION
# ============================================================================

class StealthMode:
    """Randomize request fingerprints to evade advanced tracking."""

    # TLS cipher suites to randomize (simulated via headers)
    CIPHER_HINTS = [
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
    ]

    # HTTP/2 settings variations
    HTTP2_SETTINGS = [
        {"HEADER_TABLE_SIZE": 4096, "MAX_CONCURRENT_STREAMS": 100},
        {"HEADER_TABLE_SIZE": 65536, "MAX_CONCURRENT_STREAMS": 250},
        {"HEADER_TABLE_SIZE": 16384, "MAX_CONCURRENT_STREAMS": 128},
    ]

    # Header ordering patterns (different browsers order headers differently)
    HEADER_ORDERS = [
        ["Host", "User-Agent", "Accept", "Accept-Language", "Accept-Encoding"],
        ["User-Agent", "Accept", "Accept-Language", "Accept-Encoding", "Host"],
        ["Accept", "User-Agent", "Host", "Accept-Encoding", "Accept-Language"],
    ]

    @classmethod
    def randomize_headers(cls, headers: dict) -> dict:
        """Randomize header ordering and add fingerprint variations."""
        order = random.choice(cls.HEADER_ORDERS)
        ordered = {}
        for key in order:
            if key in headers:
                ordered[key] = headers[key]
        for key, value in headers.items():
            if key not in ordered:
                ordered[key] = value

        # Add random Sec-CH-UA variations
        if random.random() > 0.5:
            brands = [
                '"Chromium";v="120", "Google Chrome";v="120"',
                '"Firefox";v="121"',
                '"Safari";v="17"',
                '"Microsoft Edge";v="120"',
            ]
            ordered["Sec-CH-UA"] = random.choice(brands)

        return ordered


# ============================================================================
# SCHEDULED PROFILES
# ============================================================================

class ScheduledProfile:
    """Time-based browsing behavior profiles."""

    PROFILES = {
        "work_hours": {
            "hours": (9, 17),
            "categories": ["Technology", "World", "Trending"],
            "patterns": ["normal", "bursty"],
            "intensity": 0.8,
        },
        "evening": {
            "hours": (17, 22),
            "categories": ["Lifestyle", "SocialMedia", "Tabloids", "Hobbies"],
            "patterns": ["slow", "normal"],
            "intensity": 0.6,
        },
        "night": {
            "hours": (22, 6),
            "categories": ["Technology", "Privacy"],
            "patterns": ["slow", "erratic"],
            "intensity": 0.3,
        },
        "weekend": {
            "hours": (0, 24),
            "categories": ["Hobbies", "SocialMedia", "Lifestyle", "Tabloids"],
            "patterns": ["erratic", "slow"],
            "intensity": 0.5,
        },
    }

    @classmethod
    def get_current_profile(cls) -> dict:
        """Get profile based on current time."""
        hour = datetime.now().hour
        day = datetime.now().weekday()

        if day >= 5:  # Weekend
            return cls.PROFILES["weekend"]

        for name, profile in cls.PROFILES.items():
            if name == "weekend":
                continue
            start, end = profile["hours"]
            if start <= hour < end or (start > end and (hour >= start or hour < end)):
                return profile

        return cls.PROFILES["evening"]


# ============================================================================
# PRIVACY SCORE / METRICS
# ============================================================================

class PrivacyMetrics:
    """Track and calculate privacy/confusion metrics."""

    def __init__(self):
        self.unique_user_agents = set()
        self.unique_categories = set()
        self.timing_samples = []
        self.request_count = 0
        self.identity_changes = 0

    def record_request(self, user_agent: str, category: str, delay: float):
        self.unique_user_agents.add(user_agent)
        self.unique_categories.add(category)
        self.timing_samples.append(delay)
        self.request_count += 1
        if len(self.timing_samples) > 100:
            self.timing_samples = self.timing_samples[-100:]

    def record_identity_change(self):
        self.identity_changes += 1

    def calculate_entropy(self, values: list) -> float:
        """Calculate Shannon entropy."""
        if not values:
            return 0.0
        from collections import Counter
        counts = Counter(values)
        total = len(values)
        entropy = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return entropy

    def get_confusion_score(self) -> int:
        """Calculate overall confusion score (0-100)."""
        ua_score = min(len(self.unique_user_agents) * 5, 30)
        cat_score = min(len(self.unique_categories) * 3, 20)
        timing_entropy = self.calculate_entropy([int(t) for t in self.timing_samples])
        timing_score = min(timing_entropy * 10, 25)
        identity_score = min(self.identity_changes * 2, 25)
        return int(ua_score + cat_score + timing_score + identity_score)

    def get_report(self) -> dict:
        return {
            "confusion_score": self.get_confusion_score(),
            "unique_fingerprints": len(self.unique_user_agents),
            "categories_visited": len(self.unique_categories),
            "identity_changes": self.identity_changes,
            "requests": self.request_count,
        }


# ============================================================================
# DECOY DATA INJECTION
# ============================================================================

class DecoyInjector:
    """Generate fake data to mislead tracking profiles."""

    FAKE_INTERESTS = [
        "luxury watches", "yacht maintenance", "private jets",
        "cryptocurrency trading", "stock market analysis",
        "organic farming", "beekeeping", "pottery classes",
        "skydiving lessons", "scuba certification",
        "wedding planning", "baby products", "retirement homes",
        "veterinary care", "pet insurance", "exotic pets",
    ]

    FAKE_LOCATIONS = [
        "New York, NY", "Los Angeles, CA", "London, UK",
        "Tokyo, Japan", "Sydney, Australia", "Paris, France",
        "Berlin, Germany", "Toronto, Canada", "Mumbai, India",
    ]

    FAKE_DEMOGRAPHICS = [
        {"age": "18-24", "gender": "male", "income": "high"},
        {"age": "25-34", "gender": "female", "income": "medium"},
        {"age": "35-44", "gender": "other", "income": "low"},
        {"age": "45-54", "gender": "male", "income": "very_high"},
        {"age": "55-64", "gender": "female", "income": "medium"},
        {"age": "65+", "gender": "male", "income": "retired"},
    ]

    @classmethod
    def generate_decoy_cookies(cls) -> str:
        """Generate misleading tracking cookies."""
        interest = random.choice(cls.FAKE_INTERESTS).replace(" ", "_")
        demo = random.choice(cls.FAKE_DEMOGRAPHICS)
        location = random.choice(cls.FAKE_LOCATIONS).replace(", ", "_").replace(" ", "")

        cookies = [
            f"_interest={interest}",
            f"_demo_age={demo['age']}",
            f"_demo_gender={demo['gender']}",
            f"_geo={location}",
            f"_segment={random.randint(1, 50)}",
            f"_cohort={random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 99)}",
        ]
        return "; ".join(random.sample(cookies, k=random.randint(2, 5)))

    @classmethod
    def generate_decoy_search(cls) -> str:
        """Generate a decoy search query URL."""
        interest = random.choice(cls.FAKE_INTERESTS)
        search_terms = [
            f"best {interest} 2024",
            f"cheap {interest} near me",
            f"{interest} reviews",
            f"how to {interest}",
            f"{interest} for beginners",
        ]
        query = random.choice(search_terms).replace(" ", "+")
        return f"https://www.google.com/search?q={query}"


# ============================================================================
# PLUGIN SYSTEM
# ============================================================================

class PluginManager:
    """Simple plugin system for custom site lists and behaviors."""

    def __init__(self, plugin_dir: str = "~/.traffic_noise/plugins"):
        self.plugin_dir = Path(plugin_dir).expanduser()
        self.custom_sites = {}
        self.custom_personas = {}

    def load_plugins(self):
        """Load custom configurations from plugin directory."""
        if not self.plugin_dir.exists():
            return

        # Load custom sites
        sites_file = self.plugin_dir / "sites.json"
        if sites_file.exists():
            try:
                with open(sites_file) as f:
                    self.custom_sites = json.load(f)
            except Exception:
                pass

        # Load custom personas
        personas_file = self.plugin_dir / "personas.json"
        if personas_file.exists():
            try:
                with open(personas_file) as f:
                    self.custom_personas = json.load(f)
            except Exception:
                pass

    def get_sites(self, category: str) -> list:
        """Get sites for a category, including custom ones."""
        return self.custom_sites.get(category, [])

    def get_persona(self, name: str) -> list:
        """Get persona categories, including custom ones."""
        return self.custom_personas.get(name, [])


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

markov_chain = MarkovChain()
chaos_generator = ChaosGenerator()
privacy_metrics = PrivacyMetrics()
plugin_manager = PluginManager()

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
    duration: int = 0
    interface: str = "eth0"
    quiet: bool = False
    max_headlines: int = 10
    simulate_issues: Optional[str] = None
    use_markov: bool = True
    include_political: bool = False
    include_tabloids: bool = False
    include_social: bool = False
    include_privacy: bool = False
    include_hobbies: bool = False
    persona: Optional[str] = None
    # New v3.3 features
    stealth_mode: bool = False
    scheduled_profile: bool = False
    show_privacy_score: bool = True
    inject_decoys: bool = False
    interactive: bool = False

# Timing
MIN_DELAY, MAX_DELAY = 3, 45
MIN_SESSION, MAX_SESSION = 60, 300
CHAOS_MIN_DELAY, CHAOS_MAX_DELAY = 1, 120

# ============================================================================
# USER AGENTS
# ============================================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "Mozilla/5.0 (PlayStation; PlayStation 5/1.0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/609.4 (KHTML, like Gecko) NF/6.0.2.21.3 NintendoBrowser/5.1.0.22474",
    "Mozilla/5.0 (SMART-TV; Linux; Tizen 6.5) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/85.0.4183.93 TV Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Tesla/2021.44.25.2",
    "Mozilla/5.0 (SmartFridge; Linux) AppleWebKit/537.36 LG/1.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
]

DNS_SERVERS = [
    "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
    "9.9.9.9", "149.112.112.112", "208.67.222.222", "208.67.220.220",
    "64.6.64.6", "64.6.65.6", "185.228.168.9", "94.140.14.14",
]

# ============================================================================
# NEWS SITES BY CATEGORY
# ============================================================================

NEWS_SITES = {
    "Lifestyle": [
        "https://www.buzzfeed.com", "https://www.huffpost.com/life",
        "https://www.refinery29.com", "https://www.goodhousekeeping.com",
        "https://www.allrecipes.com", "https://www.foodnetwork.com",
    ],
    "World": [
        "https://www.bbc.com/news/world", "https://www.reuters.com/world",
        "https://www.aljazeera.com", "https://www.theguardian.com/world",
        "https://apnews.com/world-news", "https://www.france24.com/en",
        "https://www.dw.com/en", "https://www.npr.org/sections/world",
    ],
    "Technology": [
        "https://www.theverge.com", "https://techcrunch.com",
        "https://arstechnica.com", "https://www.wired.com",
        "https://www.cnet.com", "https://www.engadget.com", "https://www.zdnet.com",
    ],
    "Health": [
        "https://www.webmd.com", "https://www.healthline.com",
        "https://www.medicalnewstoday.com", "https://www.health.com",
        "https://www.prevention.com",
    ],
    "Trending": [
        "https://news.google.com", "https://www.reddit.com/r/news",
        "https://news.ycombinator.com", "https://www.usatoday.com",
        "https://www.nbcnews.com", "https://www.cnn.com",
    ],
    "SocialNetworkAds": [
        "https://www.dailymail.co.uk", "https://www.tmz.com",
        "https://www.unilad.com", "https://www.ladbible.com",
        "https://www.foxnews.com", "https://www.independent.co.uk",
        "https://www.politico.com", "https://www.mirror.co.uk",
        "https://www.euronews.com", "https://www.businessinsider.com",
        "https://www.msn.com", "https://www.windowscentral.com",
        "https://www.techradar.com", "https://www.bgr.com",
        "https://www.marketwatch.com", "https://www.bleacherreport.com",
    ],
    "LeftLeaning": [
        "https://www.msnbc.com", "https://www.huffpost.com", "https://www.vox.com",
        "https://www.slate.com", "https://www.motherjones.com", "https://www.thenation.com",
        "https://www.theatlantic.com", "https://www.newyorker.com", "https://www.salon.com",
        "https://www.dailykos.com", "https://www.democracynow.org", "https://www.commondreams.org",
        "https://www.truthout.org", "https://www.alternet.org", "https://www.jacobinmag.com",
        "https://www.currentaffairs.org", "https://www.thedailybeast.com",
        "https://www.mediamatters.org", "https://www.rawstory.com", "https://www.theintercept.com",
        "https://www.propublica.org", "https://www.rollingstone.com", "https://www.vanityfair.com",
        "https://www.esquire.com", "https://www.vice.com", "https://www.theroot.com",
    ],
    "RightLeaning": [
        "https://www.foxnews.com", "https://www.breitbart.com", "https://www.dailywire.com",
        "https://www.theblaze.com", "https://www.newsmax.com", "https://www.oann.com",
        "https://www.washingtonexaminer.com", "https://www.nationalreview.com",
        "https://www.townhall.com", "https://www.redstate.com", "https://www.hotair.com",
        "https://www.pjmedia.com", "https://www.americanthinker.com", "https://www.thefederalist.com",
        "https://www.dailycaller.com", "https://www.freebeacon.com", "https://www.spectator.org",
        "https://www.reason.com", "https://www.cato.org", "https://www.heritage.org",
        "https://www.aei.org", "https://www.realclearpolitics.com", "https://www.theepochtimes.com",
        "https://www.zerohedge.com", "https://www.justthenews.com", "https://www.thepostmillennial.com",
    ],
    "Tabloids": [
        "https://www.tmz.com", "https://www.dailymail.co.uk", "https://www.pagesix.com",
        "https://www.eonline.com", "https://www.usmagazine.com", "https://www.people.com",
        "https://www.etonline.com", "https://www.justjared.com", "https://www.thesun.co.uk",
        "https://www.mirror.co.uk", "https://www.express.co.uk", "https://www.radaronline.com",
        "https://www.nationalenquirer.com", "https://www.nydailynews.com",
    ],
    "Hobbies": [
        "https://www.instructables.com", "https://www.allrecipes.com",
        "https://www.epicurious.com", "https://www.seriouseats.com",
        "https://www.bonappetit.com", "https://www.foodnetwork.com",
        "https://www.hgtv.com", "https://www.thespruce.com",
        "https://www.popularmechanics.com", "https://www.makeuseof.com",
        "https://www.hackaday.com", "https://www.arduino.cc",
        "https://www.photographylife.com", "https://www.petapixel.com",
        "https://www.delish.com", "https://www.tasty.co",
    ],
    "SocialMedia": [
        "https://www.facebook.com", "https://www.twitter.com", "https://www.instagram.com",
        "https://www.tiktok.com", "https://www.snapchat.com", "https://www.pinterest.com",
        "https://www.linkedin.com", "https://www.reddit.com", "https://www.tumblr.com",
        "https://www.discord.com", "https://www.twitch.tv", "https://www.youtube.com",
        "https://www.vimeo.com", "https://www.dailymotion.com", "https://www.flickr.com",
        "https://www.deviantart.com", "https://www.behance.net", "https://www.dribbble.com",
        "https://www.medium.com", "https://www.quora.com", "https://www.mastodon.social",
        "https://www.threads.net", "https://www.bluesky.social", "https://www.minds.com",
    ],
    "Privacy": [
        "https://www.eff.org", "https://www.privacytools.io", "https://www.torproject.org",
        "https://www.privacyguides.org", "https://www.spreadprivacy.com",
        "https://www.epic.org", "https://www.accessnow.org", "https://www.fightforthefuture.org",
        "https://www.aclu.org", "https://www.cdt.org", "https://www.noyb.eu",
        "https://www.openrightsgroup.org", "https://www.techdirt.com",
        "https://www.schneier.com", "https://www.krebsonsecurity.com",
        "https://www.bleepingcomputer.com", "https://www.thehackernews.com",
    ],
    "NetworkingIssues": [
        "https://www.google.com/search?q=wifi+not+connecting",
        "https://www.google.com/search?q=dns+server+not+responding",
        "https://www.google.com/search?q=ethernet+no+internet",
        "https://www.google.com/search?q=slow+internet+connection+fix",
        "https://www.google.com/search?q=router+keeps+disconnecting",
        "https://www.google.com/search?q=vpn+connection+failed",
        "https://www.reddit.com/r/techsupport/search?q=wifi+issues",
        "https://www.reddit.com/r/HomeNetworking",
        "https://superuser.com/questions/tagged/networking",
        "https://www.speedtest.net",
    ],
    "HardwareIssues": [
        "https://www.google.com/search?q=computer+won't+turn+on",
        "https://www.google.com/search?q=blue+screen+of+death+fix",
        "https://www.google.com/search?q=cpu+overheating+solutions",
        "https://www.google.com/search?q=ram+not+detected",
        "https://www.google.com/search?q=graphics+card+not+working",
        "https://www.google.com/search?q=usb+device+not+recognized",
        "https://www.reddit.com/r/buildapc",
        "https://www.reddit.com/r/techsupport",
        "https://www.tomshardware.com/forums",
    ],
    "SoftwareIssues": [
        "https://www.google.com/search?q=windows+update+stuck",
        "https://www.google.com/search?q=application+won't+open",
        "https://www.google.com/search?q=dll+file+missing+error",
        "https://www.google.com/search?q=program+keeps+crashing",
        "https://www.google.com/search?q=driver+installation+failed",
        "https://answers.microsoft.com",
        "https://support.apple.com",
        "https://askubuntu.com",
        "https://stackoverflow.com",
    ],
    "MalwareIssues": [
        "https://www.google.com/search?q=remove+malware+from+computer",
        "https://www.google.com/search?q=computer+running+slow+virus",
        "https://www.google.com/search?q=popup+ads+won't+stop",
        "https://www.google.com/search?q=browser+hijacked+fix",
        "https://www.google.com/search?q=ransomware+recovery",
        "https://www.google.com/search?q=adware+removal+tool",
        "https://www.malwarebytes.com",
        "https://www.avg.com",
        "https://www.bleepingcomputer.com/virus-removal",
    ],
    "MisconfiguredSettings": [
        "https://www.google.com/search?q=windows+proxy+settings+wrong",
        "https://www.google.com/search?q=dns+settings+incorrect",
        "https://www.google.com/search?q=firewall+settings+blocking",
        "https://www.google.com/search?q=display+resolution+problems",
        "https://www.google.com/search?q=sound+output+wrong+device",
        "https://www.howtogeek.com",
        "https://www.lifehacker.com",
    ],
}

LANGUAGES = [
    "en-US,en;q=0.9", "en-GB,en;q=0.9", "en-US,en;q=0.9,es;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8", "ja-JP,ja;q=0.9,en;q=0.8",
]

REFERERS = [
    "https://www.google.com/", "https://www.bing.com/",
    "https://duckduckgo.com/", "https://www.facebook.com/",
    "https://twitter.com/", "https://www.reddit.com/",
    "https://www.instagram.com/", "",
]

ACCEPT_HEADERS = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
]

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
    return ''.join(random.choices(string.hexdigits.lower(), k=32))

def get_random_news_url(config: Config = None, use_markov: bool = False) -> tuple:
    available = ["Lifestyle", "World", "Technology", "Health", "Trending", "SocialNetworkAds"]

    if config:
        if config.include_political:
            available.extend(["LeftLeaning", "RightLeaning"])
        if config.include_tabloids:
            available.append("Tabloids")
        if config.include_social:
            available.append("SocialMedia")
        if config.include_privacy:
            available.append("Privacy")
        if config.include_hobbies:
            available.append("Hobbies")

        if config.simulate_issues:
            issue_map = {
                "networking": ["NetworkingIssues"],
                "hardware": ["HardwareIssues"],
                "software": ["SoftwareIssues"],
                "malware": ["MalwareIssues"],
                "misconfigured": ["MisconfiguredSettings"],
                "mixed": ["NetworkingIssues", "HardwareIssues", "SoftwareIssues", "MalwareIssues", "MisconfiguredSettings"],
            }
            if config.simulate_issues in issue_map and random.random() < 0.3:
                cat = random.choice(issue_map[config.simulate_issues])
                if cat in NEWS_SITES:
                    return cat, random.choice(NEWS_SITES[cat])

        if config.persona:
            persona_map = {
                "tech_enthusiast": ["Technology", "Privacy", "Hobbies"],
                "news_junkie": ["World", "Trending", "LeftLeaning", "RightLeaning"],
                "privacy_advocate": ["Privacy", "Technology"],
                "social_butterfly": ["SocialMedia", "Lifestyle", "Trending"],
                "entertainment_seeker": ["Tabloids", "SocialMedia", "Lifestyle"],
                "health_conscious": ["Health", "Lifestyle", "Hobbies"],
                "political_observer": ["LeftLeaning", "RightLeaning", "World"],
                "hobbyist": ["Hobbies", "Technology", "Lifestyle"],
                "troubleshooter": ["NetworkingIssues", "HardwareIssues", "SoftwareIssues", "MalwareIssues"],
            }
            if config.persona in persona_map:
                available = persona_map[config.persona]

        if config.scheduled_profile:
            profile = ScheduledProfile.get_current_profile()
            available = [c for c in profile["categories"] if c in NEWS_SITES]

    available = [c for c in available if c in NEWS_SITES]
    if not available:
        available = list(NEWS_SITES.keys())

    if use_markov and config and config.chaos_mode:
        category = markov_chain.next_category()
        if category not in available:
            category = random.choice(available)
    else:
        category = random.choice(available)

    url = random.choice(NEWS_SITES[category])

    # Inject decoy searches occasionally
    if config and config.inject_decoys and random.random() < 0.1:
        url = DecoyInjector.generate_decoy_search()
        category = "Decoy"

    return category, url


def get_pattern_delay(pattern: str, chaos: bool = False, use_chaos_math: bool = False) -> float:
    if chaos and use_chaos_math:
        return chaos_generator.get_chaos_delay(CHAOS_MIN_DELAY, CHAOS_MAX_DELAY)
    elif chaos:
        return random.uniform(CHAOS_MIN_DELAY, CHAOS_MAX_DELAY)

    delays = {
        "normal": (5, 30), "bursty": (1, 3) if random.random() < 0.7 else (30, 90),
        "slow": (45, 180), "erratic": (1, 120), "scanner": (1, 5),
    }
    min_d, max_d = delays.get(pattern, (MIN_DELAY, MAX_DELAY))
    return random.uniform(min_d, max_d)


def build_headers(config: Config = None) -> dict:
    ua = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": ua,
        "Accept": random.choice(ACCEPT_HEADERS),
        "Accept-Language": random.choice(LANGUAGES),
        "Accept-Encoding": random.choice(["gzip, deflate, br", "gzip, deflate"]),
        "Connection": random.choice(["keep-alive", "close"]),
    }

    if random.random() > 0.3:
        headers["DNT"] = str(random.randint(0, 1))

    referer = random.choice(REFERERS)
    if referer:
        headers["Referer"] = referer

    # Add decoy cookies
    if config and config.inject_decoys:
        headers["Cookie"] = DecoyInjector.generate_decoy_cookies()
    elif random.random() > 0.3:
        ts = int(datetime.now().timestamp())
        headers["Cookie"] = f"_ga=GA1.2.{random.randint(1000000, 9999999)}.{ts}; session={generate_session_id()}"

    # Stealth mode randomization
    if config and config.stealth_mode:
        headers = StealthMode.randomize_headers(headers)

    privacy_metrics.record_request(ua, "", 0)
    return headers

# ============================================================================
# HEADLINE EXTRACTION
# ============================================================================

def extract_headlines(html: str, url: str, category: str) -> list:
    headlines = []
    try:
        soup = BeautifulSoup(html, 'lxml')
        selectors = ['h1', 'h2', 'h3', 'article h2', '.headline', '.title']
        seen = set()

        for selector in selectors:
            for elem in soup.select(selector)[:5]:
                text = re.sub(r'\s+', ' ', elem.get_text(strip=True))
                if 20 < len(text) < 200 and text not in seen:
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
    except Exception:
        pass
    return headlines

# ============================================================================
# NETWORK FUNCTIONS
# ============================================================================

async def fetch_url(client: httpx.AsyncClient, url: str, config: Config) -> Optional[str]:
    headers = build_headers(config)
    try:
        response = await client.get(url, headers=headers, timeout=30.0, follow_redirects=True)
        state.request_count += 1
        return response.text
    except Exception:
        state.errors += 1
        return None


async def connect_to_vps(client: httpx.AsyncClient, target: str, config: Config) -> bool:
    headers = build_headers(config)
    host, port = (target.rsplit(':', 1) + ["80"])[:2]

    for scheme in ["https", "http"]:
        try:
            response = await client.get(f"{scheme}://{host}:{port}", headers=headers, timeout=30.0)
            state.request_count += 1
            return True
        except Exception:
            continue
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
        Layout(name="stats", size=7 if config.show_privacy_score else 6),
        Layout(name="footer", size=3),
    )
    return layout


def update_display(layout: Layout, config: Config):
    elapsed = str(datetime.now() - state.start_time).split('.')[0]

    mode_text = "[bold cyan]CHAOS[/]" if config.chaos_mode else f"[cyan]{config.mode.upper()}[/]"
    header_text = Text()
    header_text.append(f"Traffic Noise v{__version__} ", style="bold green")
    header_text.append(f"| {mode_text} ", style="white")
    header_text.append(f"| Workers: [yellow]{config.parallel_workers}[/] ", style="white")
    header_text.append(f"| {elapsed}", style="magenta")

    layout["header"].update(Panel(header_text, box=box.ROUNDED))

    # Headlines table
    table = Table(show_header=True, header_style="bold blue", box=box.SIMPLE, expand=True)
    table.add_column("Time", width=10)
    table.add_column("Category", width=12)
    table.add_column("Headline", ratio=1)
    table.add_column("Source", width=20)

    recent = list(state.headlines)[-config.max_headlines:]
    for h in recent:
        table.add_row(h.get("time", ""), h.get("category", "")[:10], h.get("text", "")[:80], h.get("source", "")[:18])

    while len(recent) < config.max_headlines:
        table.add_row("", "", "[dim]Waiting...[/]", "")
        recent.append({})

    layout["headlines"].update(Panel(table, title="[bold]Live Headlines[/]", border_style="blue"))

    # Stats
    stats = Table(show_header=False, box=None, expand=True)
    stats.add_column("L1"); stats.add_column("V1"); stats.add_column("L2"); stats.add_column("V2")
    stats.add_row("Requests:", f"[green]{state.request_count}[/]", "Errors:", f"[red]{state.errors}[/]")
    stats.add_row("Category:", f"[cyan]{state.last_category or 'N/A'}[/]", "Workers:", f"[yellow]{state.workers_active}[/]")

    if config.show_privacy_score:
        score = privacy_metrics.get_confusion_score()
        score_color = "green" if score > 70 else "yellow" if score > 40 else "red"
        stats.add_row("Privacy Score:", f"[{score_color}]{score}/100[/]", "Fingerprints:", f"[cyan]{len(privacy_metrics.unique_user_agents)}[/]")

    layout["stats"].update(Panel(stats, title="[bold]Statistics[/]", border_style="green"))

    target = f"[yellow]VPS: {config.vps_target}[/]" if config.vps_target else "[dim]News mode[/]"
    layout["footer"].update(Panel(Text(f"Ctrl+C to stop | {target}"), box=box.ROUNDED))

# ============================================================================
# WORKER
# ============================================================================

async def worker(worker_id: int, config: Config, layout: Layout, live: Live):
    pattern = random.choice(BROWSING_PATTERNS)
    state.workers_active += 1
    worker_chaos = ChaosGenerator(r=3.85 + worker_id * 0.01)

    # Initialize per-worker chaos generator for variety
    worker_chaos = ChaosGenerator(r=3.85 + worker_id * 0.01)

    async with httpx.AsyncClient() as client:
        while state.running:
            try:
                if random.random() < 0.2:
                    send_local_udp(19999 + worker_id)

                if config.mode == "vps" and config.vps_target:
                    await connect_to_vps(client, config.vps_target, config)
                    state.last_url = config.vps_target
                    state.last_category = "VPS"
                else:
                    category, url = get_random_news_url(config, config.chaos_mode and config.use_markov)
                    state.last_category = category
                    state.last_url = url
                    html = await fetch_url(client, url, config)

                    if html and config.show_headlines:
                        for h in extract_headlines(html, url, category)[:2]:
                            state.headlines.append(h)

                    privacy_metrics.record_request(random.choice(USER_AGENTS), category, 0)

                update_display(layout, config)
                live.refresh()

                delay = get_pattern_delay(pattern, config.chaos_mode, config.chaos_mode and config.use_markov)
                privacy_metrics.timing_samples.append(delay)

                if config.chaos_mode:
                    if config.use_markov and worker_chaos.should_switch_behavior(0.15):
                        pattern = markov_chain.next_pattern()
                        privacy_metrics.record_identity_change()
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
# INTERACTIVE SETUP
# ============================================================================

def interactive_setup() -> Config:
    """Interactive configuration wizard."""
    console.print(Panel.fit(
        f"[bold green]Traffic Noise Generator v{__version__}[/]\n"
        "[dim]Interactive Setup Wizard[/]",
        border_style="green"
    ))

    chaos = Confirm.ask("Enable [bold cyan]Chaos Mode[/] (recommended)?", default=True)
    workers = IntPrompt.ask("Number of [yellow]parallel workers[/]", default=5)
    workers = min(max(workers, 1), 30)

    console.print("\n[bold]Content Categories:[/]")
    political = Confirm.ask("  Include [blue]politically diverse[/] sites?", default=False)
    tabloids = Confirm.ask("  Include [magenta]tabloid/entertainment[/] sites?", default=True)
    social = Confirm.ask("  Include [cyan]social media[/] platforms?", default=True)
    privacy = Confirm.ask("  Include [green]privacy-focused[/] sites?", default=True)

    console.print("\n[bold]Advanced Features:[/]")
    stealth = Confirm.ask("  Enable [red]Stealth Mode[/] (fingerprint randomization)?", default=True)
    decoys = Confirm.ask("  Enable [yellow]Decoy Injection[/] (misleading data)?", default=True)
    scheduled = Confirm.ask("  Enable [blue]Scheduled Profiles[/] (time-based)?", default=False)

    duration = IntPrompt.ask("\nRun for how many [magenta]minutes[/] (0 = continuous)?", default=0)

    return Config(
        chaos_mode=chaos,
        parallel_workers=workers,
        include_political=political,
        include_tabloids=tabloids,
        include_social=social,
        include_privacy=privacy,
        stealth_mode=stealth,
        inject_decoys=decoys,
        scheduled_profile=scheduled,
        duration=duration,
        include_hobbies=True,
        interactive=True,
    )

# ============================================================================
# MAIN
# ============================================================================

async def main_async(config: Config):
    layout = create_display(config)

    with Live(layout, console=console, refresh_per_second=2, screen=True) as live:
        update_display(layout, config)
        tasks = [asyncio.create_task(worker(i, config, layout, live)) for i in range(config.parallel_workers)]

        try:
            if config.duration > 0:
                await asyncio.sleep(config.duration * 60)
                state.running = False
            else:
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


def print_setup_help():
    """Print setup instructions and a joke."""
    console.print(Panel.fit(
        "[bold green]Setup Instructions[/]\n\n"
        "[yellow]1. Create virtual environment:[/]\n"
        "   [dim]python3 -m venv venv[/]\n\n"
        "[yellow]2. Activate it (use BASH, not zsh!):[/]\n"
        "   [dim]source venv/bin/activate[/]\n\n"
        "[yellow]3. Install dependencies:[/]\n"
        "   [dim]pip install -r requirements.txt[/]\n"
        "   [dim]# Or: pip install httpx beautifulsoup4 lxml rich[/]\n\n"
        "[bold magenta]Taxi Cab Driver Joke:[/]\n"
        f"   [italic]{random.choice(TAXI_JOKES)}[/]",
        title="[bold]Quick Start Guide[/]",
        border_style="blue"
    ))


def main():
    parser = argparse.ArgumentParser(
        description=f"Traffic Noise Generator v{__version__} - Network obfuscation with live headlines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --interactive         # Guided setup wizard
  %(prog)s -c -w 5               # Chaos mode, 5 workers
  %(prog)s -c --stealth          # Chaos + fingerprint randomization
  %(prog)s --simulate-issues mixed -c  # Simulate tech issues
  %(prog)s --include-all -c      # All content categories
        """
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--setup", action="store_true", help="Show setup instructions and a joke")
    parser.add_argument("--interactive", "-I", action="store_true", help="Interactive configuration wizard")

    parser.add_argument("-n", "--news-only", action="store_true", default=True)
    parser.add_argument("-v", "--vps", type=str, metavar="IP:PORT")
    parser.add_argument("-H", "--headlines", action="store_true", default=True)
    parser.add_argument("--no-headlines", action="store_true")
    parser.add_argument("-r", "--randomize-id", action="store_true")
    parser.add_argument("-c", "--chaos", action="store_true", help="Chaos mode with Markov chains")
    parser.add_argument("-w", "--workers", type=int, default=3, metavar="NUM")
    parser.add_argument("-d", "--duration", type=int, default=0, metavar="MINS")
    parser.add_argument("-i", "--interface", type=str, default="eth0")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--max-headlines", type=int, default=10)
    parser.add_argument("--no-markov", action="store_true")

    # v3.3 Features
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode (fingerprint randomization)")
    parser.add_argument("--scheduled", action="store_true", help="Use time-based browsing profiles")
    parser.add_argument("--decoys", action="store_true", help="Inject decoy/misleading data")
    parser.add_argument("--no-privacy-score", action="store_true", help="Hide privacy score")

    issue = parser.add_argument_group("Issue Simulation")
    issue.add_argument("--simulate-issues", choices=["networking", "hardware", "software", "malware", "misconfigured", "mixed"])

    content = parser.add_argument_group("Content Categories")
    content.add_argument("--include-political", action="store_true")
    content.add_argument("--include-tabloids", action="store_true")
    content.add_argument("--include-social", action="store_true")
    content.add_argument("--include-privacy", action="store_true")
    content.add_argument("--include-hobbies", action="store_true")
    content.add_argument("--include-all", action="store_true")

    persona = parser.add_argument_group("Persona Mode")
    persona.add_argument("--persona", choices=["tech_enthusiast", "news_junkie", "privacy_advocate", "social_butterfly", "entertainment_seeker", "health_conscious", "political_observer", "hobbyist", "troubleshooter"])
    persona.add_argument("--list-personas", action="store_true")

    args = parser.parse_args()

    if args.setup:
        print_setup_help()
        return

    if args.list_personas:
        personas = {
            "tech_enthusiast": "Technology, privacy, and hobby sites",
            "news_junkie": "World news across political spectrum",
            "privacy_advocate": "Privacy tools and security resources",
            "social_butterfly": "Social media and trending content",
            "entertainment_seeker": "Tabloids and entertainment",
            "health_conscious": "Health, wellness, and lifestyle",
            "political_observer": "Political news from all sides",
            "hobbyist": "DIY, crafts, and projects",
            "troubleshooter": "Tech support searches",
        }
        console.print("\n[bold]Available Personas:[/]\n")
        for name, desc in personas.items():
            console.print(f"  [cyan]{name:22}[/] - {desc}")
        console.print()
        return

    if args.interactive:
        config = interactive_setup()
    else:
        if args.include_all:
            args.include_political = args.include_tabloids = args.include_social = True
            args.include_privacy = args.include_hobbies = True

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
            stealth_mode=args.stealth,
            scheduled_profile=args.scheduled,
            inject_decoys=args.decoys,
            show_privacy_score=not args.no_privacy_score,
        )

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if not config.quiet:
        features = []
        if config.chaos_mode: features.append("Chaos")
        if config.stealth_mode: features.append("Stealth")
        if config.inject_decoys: features.append("Decoys")
        if config.scheduled_profile: features.append("Scheduled")

        console.print(Panel.fit(
            f"[bold green]Traffic Noise Generator v{__version__}[/]\n"
            f"[dim]Workers: {config.parallel_workers} | Features: {', '.join(features) or 'Standard'}[/]",
            border_style="green",
        ))
        console.print("[dim]Starting... Press Ctrl+C to stop[/]\n")

    try:
        asyncio.run(main_async(config))
    except KeyboardInterrupt:
        pass
    finally:
        if config.show_privacy_score:
            report = privacy_metrics.get_report()
            console.print(f"\n[bold]Session Report:[/] Score: {report['confusion_score']}/100 | "
                         f"Fingerprints: {report['unique_fingerprints']} | Requests: {report['requests']}")
        console.print("[green]Cleanup complete.[/]")


if __name__ == "__main__":
    main()
