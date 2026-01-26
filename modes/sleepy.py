#!/usr/bin/env python3
"""
Sleepy Mode - Realistic overnight traffic generation.

"I'm not sleeping, I'm just browsing with my eyes closed."
    - Your computer at 3am

This module generates human-like browsing patterns while you sleep,
making it appear as if you're a real person with a terrible sleep schedule.

Features:
- Time-aware browsing patterns (slows down at night)
- Markov chain learning from your actual habits (optional)
- Realistic session lengths and breaks
- "Can't sleep" random 3am bursts
"""

import asyncio
import random
import json
import os
from datetime import datetime, time, timedelta
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Callable, Any
from collections import defaultdict
from pathlib import Path


@dataclass
class SleepSchedule:
    """
    Defines sleeping patterns for realistic traffic generation.

    Because even fake browsing needs beauty sleep.
    """
    # When the fake person "goes to bed" (slows down)
    bedtime_start: time = field(default_factory=lambda: time(23, 0))  # 11 PM
    # When they're "deep asleep" (very minimal activity)
    deep_sleep_start: time = field(default_factory=lambda: time(1, 0))  # 1 AM
    # When they might "toss and turn" (occasional activity)
    restless_start: time = field(default_factory=lambda: time(3, 0))  # 3 AM
    # When they "wake up" (activity increases)
    wake_start: time = field(default_factory=lambda: time(6, 0))  # 6 AM
    # When they're "fully awake" (normal activity)
    fully_awake: time = field(default_factory=lambda: time(8, 0))  # 8 AM


@dataclass
class ActivityWindow:
    """Defines activity levels for different time periods."""
    name: str
    requests_per_hour: tuple  # (min, max) requests per hour
    delay_range: tuple  # (min_seconds, max_seconds) between requests
    burst_chance: float  # Probability of a burst of activity
    category_weights: Dict[str, float] = field(default_factory=dict)


class BehaviorModel:
    """
    Markov chain model for learning and predicting browsing behavior.

    "It's not AI, it's just fancy counting."
        - Every data scientist, ever

    This learns transition probabilities from browsing patterns:
    - What category follows what category?
    - How long between requests at different times?
    - What's the typical session length?

    No neural networks, no GPU required, fits in memory smaller
    than the cookie file it's trying to obscure.
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the behavior model.

        Args:
            model_path: Path to save/load the learned model
        """
        self.model_path = model_path or os.path.expanduser("~/.palm-tree-behavior.json")

        # Transition probabilities: category -> {next_category: probability}
        self.transitions: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))

        # Time-based delay patterns: hour -> [delays]
        self.delay_patterns: Dict[int, List[float]] = defaultdict(list)

        # Session lengths: [durations in minutes]
        self.session_lengths: List[float] = []

        # Current state
        self.current_category: Optional[str] = None
        self.history: List[str] = []

        # Default categories (news site categories)
        self.categories = ["Lifestyle", "World", "Technology", "Health", "Trending", "Social", "Shopping", "Entertainment"]

        # Try to load existing model
        self._load_model()

    def train_from_history(self, browsing_history: List[Dict[str, Any]]) -> None:
        """
        Train the model from browsing history.

        Args:
            browsing_history: List of {category: str, timestamp: datetime, url: str}
        """
        if len(browsing_history) < 2:
            return

        # Sort by timestamp
        sorted_history = sorted(browsing_history, key=lambda x: x.get('timestamp', datetime.now()))

        prev_category = None
        prev_time = None

        for entry in sorted_history:
            category = entry.get('category', 'Unknown')
            timestamp = entry.get('timestamp', datetime.now())

            # Learn transitions
            if prev_category:
                self.transitions[prev_category][category] += 1

            # Learn delays
            if prev_time:
                delay = (timestamp - prev_time).total_seconds()
                if 0 < delay < 3600:  # Ignore gaps > 1 hour (sessions)
                    hour = timestamp.hour
                    self.delay_patterns[hour].append(delay)

            prev_category = category
            prev_time = timestamp

        # Normalize transition probabilities
        self._normalize_transitions()

        # Save model
        self._save_model()

    def train_from_bash_history(self, history_path: str = "~/.bash_history") -> None:
        """
        Train from bash history by looking for curl/wget/browser commands.

        This is a fun approximation - if you curl a lot of tech sites,
        we'll assume you like tech news.
        """
        history_path = os.path.expanduser(history_path)
        if not os.path.exists(history_path):
            return

        # Keywords to category mapping
        keyword_categories = {
            "github": "Technology",
            "stackoverflow": "Technology",
            "reddit": "Trending",
            "twitter": "Social",
            "facebook": "Social",
            "instagram": "Social",
            "youtube": "Entertainment",
            "netflix": "Entertainment",
            "amazon": "Shopping",
            "news": "World",
            "bbc": "World",
            "cnn": "World",
            "health": "Health",
            "recipe": "Lifestyle",
            "food": "Lifestyle",
        }

        categories_found = []

        try:
            with open(history_path, 'r', errors='ignore') as f:
                for line in f:
                    line_lower = line.lower()
                    for keyword, category in keyword_categories.items():
                        if keyword in line_lower:
                            categories_found.append(category)
                            break
        except Exception:
            pass

        # Learn transitions from found categories
        if len(categories_found) >= 2:
            for i in range(len(categories_found) - 1):
                self.transitions[categories_found[i]][categories_found[i + 1]] += 1

            self._normalize_transitions()
            self._save_model()

    def _normalize_transitions(self) -> None:
        """Normalize transition probabilities to sum to 1."""
        for from_cat in self.transitions:
            total = sum(self.transitions[from_cat].values())
            if total > 0:
                for to_cat in self.transitions[from_cat]:
                    self.transitions[from_cat][to_cat] /= total

    def predict_next_category(self, current_category: Optional[str] = None) -> str:
        """
        Predict the next category based on current state.

        Returns a category weighted by learned probabilities,
        or a random one if we haven't learned anything yet.
        """
        current = current_category or self.current_category

        if current and current in self.transitions:
            probs = self.transitions[current]
            if probs:
                categories = list(probs.keys())
                weights = list(probs.values())
                chosen = random.choices(categories, weights=weights, k=1)[0]
                self.current_category = chosen
                return chosen

        # Fallback to random
        chosen = random.choice(self.categories)
        self.current_category = chosen
        return chosen

    def predict_delay(self, hour: Optional[int] = None) -> float:
        """
        Predict the delay before the next request.

        Uses learned patterns for the current hour, or reasonable defaults.
        """
        hour = hour or datetime.now().hour

        if hour in self.delay_patterns and self.delay_patterns[hour]:
            delays = self.delay_patterns[hour]
            # Return something near the median with some randomness
            median_delay = sorted(delays)[len(delays) // 2]
            return max(1, median_delay * random.uniform(0.5, 1.5))

        # Default delays based on time of day
        if 0 <= hour < 6:  # Night
            return random.uniform(300, 1800)  # 5-30 minutes
        elif 6 <= hour < 9:  # Morning
            return random.uniform(30, 180)  # 30s - 3 min
        elif 9 <= hour < 17:  # Work hours
            return random.uniform(60, 300)  # 1-5 min
        elif 17 <= hour < 23:  # Evening
            return random.uniform(15, 120)  # 15s - 2 min
        else:  # Late night
            return random.uniform(120, 600)  # 2-10 min

    def _save_model(self) -> None:
        """Save the learned model to disk."""
        try:
            model_data = {
                "transitions": {k: dict(v) for k, v in self.transitions.items()},
                "delay_patterns": {str(k): v for k, v in self.delay_patterns.items()},
                "session_lengths": self.session_lengths,
            }
            with open(self.model_path, 'w') as f:
                json.dump(model_data, f, indent=2)
        except Exception:
            pass  # Silent fail - model saving is optional

    def _load_model(self) -> None:
        """Load the learned model from disk."""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'r') as f:
                    model_data = json.load(f)
                    self.transitions = defaultdict(
                        lambda: defaultdict(float),
                        {k: defaultdict(float, v) for k, v in model_data.get("transitions", {}).items()}
                    )
                    self.delay_patterns = defaultdict(
                        list,
                        {int(k): v for k, v in model_data.get("delay_patterns", {}).items()}
                    )
                    self.session_lengths = model_data.get("session_lengths", [])
        except Exception:
            pass  # Silent fail - start fresh


class SleepyMode:
    """
    Sleepy Mode - Generate realistic overnight traffic.

    "Simulating insomnia so you don't have to experience it."

    This mode generates traffic patterns that look like a real person
    who can't sleep, gradually winding down at night and occasionally
    waking up to scroll through their phone.

    Time periods:
    - 11pm-1am: Active browsing, slowing down (pre-sleep scrolling)
    - 1am-3am: Very slow, occasional requests (light sleep)
    - 3am-6am: Rare bursts (restless sleep, can't sleep moments)
    - 6am-8am: Gradually increasing (morning routine)
    """

    # Activity windows define behavior for different times
    ACTIVITY_WINDOWS = {
        "pre_sleep": ActivityWindow(
            name="Pre-Sleep Scrolling",
            requests_per_hour=(6, 15),
            delay_range=(120, 600),  # 2-10 minutes
            burst_chance=0.3,
            category_weights={"Social": 0.3, "Entertainment": 0.3, "Trending": 0.2, "Lifestyle": 0.2}
        ),
        "winding_down": ActivityWindow(
            name="Winding Down",
            requests_per_hour=(2, 6),
            delay_range=(300, 1200),  # 5-20 minutes
            burst_chance=0.1,
            category_weights={"Entertainment": 0.4, "Lifestyle": 0.3, "Trending": 0.3}
        ),
        "light_sleep": ActivityWindow(
            name="Light Sleep",
            requests_per_hour=(0, 2),
            delay_range=(1200, 3600),  # 20-60 minutes
            burst_chance=0.05,
            category_weights={"Social": 0.5, "Trending": 0.3, "Entertainment": 0.2}
        ),
        "deep_sleep": ActivityWindow(
            name="Deep Sleep",
            requests_per_hour=(0, 1),
            delay_range=(1800, 7200),  # 30 min - 2 hours
            burst_chance=0.02,
            category_weights={"Social": 0.6, "Trending": 0.4}
        ),
        "cant_sleep": ActivityWindow(
            name="Can't Sleep",
            requests_per_hour=(3, 8),
            delay_range=(60, 300),  # 1-5 minutes
            burst_chance=0.4,
            category_weights={"Social": 0.3, "Trending": 0.3, "Entertainment": 0.2, "Technology": 0.2}
        ),
        "waking_up": ActivityWindow(
            name="Waking Up",
            requests_per_hour=(4, 10),
            delay_range=(180, 600),  # 3-10 minutes
            burst_chance=0.2,
            category_weights={"Trending": 0.4, "World": 0.3, "Lifestyle": 0.3}
        ),
        "morning_routine": ActivityWindow(
            name="Morning Routine",
            requests_per_hour=(8, 20),
            delay_range=(60, 300),  # 1-5 minutes
            burst_chance=0.3,
            category_weights={"World": 0.3, "Trending": 0.2, "Technology": 0.2, "Lifestyle": 0.2, "Health": 0.1}
        ),
        "daytime": ActivityWindow(
            name="Daytime",
            requests_per_hour=(5, 15),
            delay_range=(120, 480),  # 2-8 minutes
            burst_chance=0.25,
            category_weights={"Technology": 0.25, "World": 0.2, "Trending": 0.2, "Lifestyle": 0.2, "Health": 0.15}
        ),
    }

    # News sites by category (matches traffic_noise.py)
    NEWS_SITES = {
        "Lifestyle": [
            "https://www.buzzfeed.com",
            "https://www.huffpost.com/life",
            "https://www.refinery29.com",
            "https://www.goodhousekeeping.com",
            "https://www.allrecipes.com",
        ],
        "World": [
            "https://www.bbc.com/news/world",
            "https://www.reuters.com/world",
            "https://www.theguardian.com/world",
            "https://apnews.com/world-news",
        ],
        "Technology": [
            "https://www.theverge.com",
            "https://techcrunch.com",
            "https://arstechnica.com",
            "https://www.wired.com",
        ],
        "Health": [
            "https://www.webmd.com",
            "https://www.healthline.com",
            "https://www.health.com",
        ],
        "Trending": [
            "https://news.google.com",
            "https://www.reddit.com/r/news",
            "https://news.ycombinator.com",
        ],
        "Social": [
            "https://www.reddit.com",
            "https://twitter.com",
        ],
        "Entertainment": [
            "https://www.youtube.com",
            "https://www.netflix.com",
            "https://www.imdb.com",
        ],
        "Shopping": [
            "https://www.amazon.com",
            "https://www.ebay.com",
        ],
    }

    def __init__(
        self,
        schedule: Optional[SleepSchedule] = None,
        use_learning: bool = False,
        model_path: Optional[str] = None,
        fetch_callback: Optional[Callable] = None,
    ):
        """
        Initialize Sleepy Mode.

        Args:
            schedule: Custom sleep schedule (uses defaults if None)
            use_learning: Whether to use Markov chain learning
            model_path: Path to save/load the behavior model
            fetch_callback: Function to call for fetching URLs (for integration with traffic_noise.py)
        """
        self.schedule = schedule or SleepSchedule()
        self.use_learning = use_learning
        self.fetch_callback = fetch_callback

        if use_learning:
            self.behavior_model = BehaviorModel(model_path)
        else:
            self.behavior_model = None

        self.running = False
        self.stats = {
            "requests": 0,
            "categories": defaultdict(int),
            "start_time": None,
        }

    def get_current_activity_window(self, now: Optional[datetime] = None) -> ActivityWindow:
        """
        Determine the current activity window based on time.

        This is where the magic happens - different times get different
        browsing intensities.
        """
        now = now or datetime.now()
        current_time = now.time()
        hour = now.hour

        # Check for "can't sleep" random event (5% chance between 1am-5am)
        if 1 <= hour < 5 and random.random() < 0.05:
            return self.ACTIVITY_WINDOWS["cant_sleep"]

        # Determine window based on time
        if self._time_in_range(current_time, self.schedule.bedtime_start, self.schedule.deep_sleep_start):
            # 11pm - 1am: Winding down
            return self.ACTIVITY_WINDOWS["winding_down"]
        elif self._time_in_range(current_time, self.schedule.deep_sleep_start, self.schedule.restless_start):
            # 1am - 3am: Light sleep
            return self.ACTIVITY_WINDOWS["light_sleep"]
        elif self._time_in_range(current_time, self.schedule.restless_start, self.schedule.wake_start):
            # 3am - 6am: Deep sleep (very quiet)
            return self.ACTIVITY_WINDOWS["deep_sleep"]
        elif self._time_in_range(current_time, self.schedule.wake_start, self.schedule.fully_awake):
            # 6am - 8am: Waking up
            return self.ACTIVITY_WINDOWS["waking_up"]
        elif 8 <= hour < 22:
            # 8am - 10pm: Normal daytime
            return self.ACTIVITY_WINDOWS["daytime"]
        else:
            # 10pm - 11pm: Pre-sleep scrolling
            return self.ACTIVITY_WINDOWS["pre_sleep"]

    def _time_in_range(self, current: time, start: time, end: time) -> bool:
        """Check if current time is in range (handles midnight crossing)."""
        if start <= end:
            return start <= current < end
        else:  # Crosses midnight
            return current >= start or current < end

    def select_category(self, window: ActivityWindow) -> str:
        """
        Select a category to browse based on current window and learned behavior.
        """
        # If using learning, let the model decide (with some probability)
        if self.behavior_model and random.random() < 0.7:
            return self.behavior_model.predict_next_category()

        # Otherwise use window weights
        if window.category_weights:
            categories = list(window.category_weights.keys())
            weights = list(window.category_weights.values())
            return random.choices(categories, weights=weights, k=1)[0]

        # Fallback
        return random.choice(list(self.NEWS_SITES.keys()))

    def select_url(self, category: str) -> str:
        """Select a random URL from the given category."""
        sites = self.NEWS_SITES.get(category, self.NEWS_SITES["Trending"])
        return random.choice(sites)

    def calculate_delay(self, window: ActivityWindow) -> float:
        """
        Calculate the delay before the next request.

        Uses learned patterns if available, otherwise uses window defaults.
        """
        # If using learning, let the model decide (sometimes)
        if self.behavior_model and random.random() < 0.6:
            return self.behavior_model.predict_delay()

        # Check for burst
        if random.random() < window.burst_chance:
            # Burst: much shorter delay
            return random.uniform(3, 30)

        # Normal delay from window range
        return random.uniform(*window.delay_range)

    async def run(self, duration_hours: float = 8, max_bandwidth_kbps: int = 500) -> None:
        """
        Run Sleepy Mode for the specified duration.

        Args:
            duration_hours: How long to run (default 8 hours for a full night)
            max_bandwidth_kbps: Maximum bandwidth to use (for throttling)
        """
        self.running = True
        self.stats["start_time"] = datetime.now()
        end_time = self.stats["start_time"] + timedelta(hours=duration_hours)

        print(f"[Sleepy Mode] Starting at {self.stats['start_time'].strftime('%H:%M:%S')}")
        print(f"[Sleepy Mode] Will run until {end_time.strftime('%H:%M:%S')}")

        while self.running and datetime.now() < end_time:
            try:
                # Get current activity window
                window = self.get_current_activity_window()

                # Select category and URL
                category = self.select_category(window)
                url = self.select_url(category)

                # Log the activity
                now = datetime.now()
                print(f"[{now.strftime('%H:%M:%S')}] [{window.name}] {category}: {url}")

                # Make the request (if callback is set)
                if self.fetch_callback:
                    try:
                        await self.fetch_callback(url, category)
                    except Exception as e:
                        print(f"[Sleepy Mode] Request failed: {e}")

                # Update stats
                self.stats["requests"] += 1
                self.stats["categories"][category] += 1

                # Calculate and apply delay
                delay = self.calculate_delay(window)
                print(f"[Sleepy Mode] Next request in {delay:.0f}s ({window.name})")

                await asyncio.sleep(delay)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Sleepy Mode] Error: {e}")
                await asyncio.sleep(60)  # Wait a minute on error

        self.running = False
        self._print_stats()

    def _print_stats(self) -> None:
        """Print session statistics."""
        if self.stats["start_time"]:
            duration = datetime.now() - self.stats["start_time"]
            print("\n" + "=" * 50)
            print("Sleepy Mode Session Complete")
            print("=" * 50)
            print(f"Duration: {duration}")
            print(f"Total Requests: {self.stats['requests']}")
            print("\nRequests by Category:")
            for cat, count in sorted(self.stats["categories"].items(), key=lambda x: -x[1]):
                print(f"  {cat}: {count}")

    def stop(self) -> None:
        """Stop the sleepy mode."""
        self.running = False


# For testing
if __name__ == "__main__":
    async def test():
        print("Testing Sleepy Mode...")
        print("=" * 50)

        mode = SleepyMode(use_learning=False)

        # Test activity windows at different times
        test_times = [
            datetime(2024, 1, 1, 22, 0),   # 10pm - Pre-sleep
            datetime(2024, 1, 1, 23, 30),  # 11:30pm - Winding down
            datetime(2024, 1, 2, 1, 30),   # 1:30am - Light sleep
            datetime(2024, 1, 2, 4, 0),    # 4am - Deep sleep
            datetime(2024, 1, 2, 7, 0),    # 7am - Waking up
            datetime(2024, 1, 2, 12, 0),   # 12pm - Daytime
        ]

        for test_time in test_times:
            window = mode.get_current_activity_window(test_time)
            category = mode.select_category(window)
            delay = mode.calculate_delay(window)
            print(f"\nTime: {test_time.strftime('%H:%M')}")
            print(f"  Window: {window.name}")
            print(f"  Category: {category}")
            print(f"  Delay: {delay:.0f}s")
            print(f"  URL: {mode.select_url(category)}")

    asyncio.run(test())
