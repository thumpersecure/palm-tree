#!/usr/bin/env python3
"""
Daily Routine Profiles - Browse like a real human (but faker).

"Because nobody browses news sites at 3am and shopping sites at 9am."

This module provides pre-built daily browsing routines that mimic
realistic human behavior patterns throughout the day. Each routine
defines what categories to browse, at what intensity, and with
what timing - making your traffic look like a genuine person's
browsing history.

Unlike scheduled profiles (which just change categories by time),
daily routines define complete behavioral arcs with transitions,
breaks, and natural pauses.
"""

__version__ = "1.0.0"

import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, time


@dataclass
class TimeSlot:
    """A time period within a daily routine."""
    start_hour: int
    end_hour: int
    categories: List[str]
    intensity: float
    description: str
    search_queries: List[str] = field(default_factory=list)
    break_probability: float = 0.0


@dataclass
class DailyRoutine:
    """A complete daily browsing routine."""
    name: str
    description: str
    persona: str
    time_slots: List[TimeSlot]
    weekend_modifier: Optional[Dict] = None

    def get_current_slot(self) -> Optional[TimeSlot]:
        """Get the time slot for the current hour."""
        hour = datetime.now().hour
        day = datetime.now().weekday()

        for slot in self.time_slots:
            if slot.start_hour <= slot.end_hour:
                if slot.start_hour <= hour < slot.end_hour:
                    return self._apply_weekend(slot, day)
            else:
                if hour >= slot.start_hour or hour < slot.end_hour:
                    return self._apply_weekend(slot, day)
        return None

    def _apply_weekend(self, slot: TimeSlot, day: int) -> TimeSlot:
        if day >= 5 and self.weekend_modifier:
            mod = self.weekend_modifier
            return TimeSlot(
                start_hour=slot.start_hour + mod.get("shift_hours", 0),
                end_hour=slot.end_hour + mod.get("shift_hours", 0),
                categories=mod.get("categories", slot.categories),
                intensity=slot.intensity * mod.get("intensity_mult", 0.7),
                description=slot.description + " (weekend)",
                search_queries=slot.search_queries,
                break_probability=slot.break_probability + 0.2,
            )
        return slot

    def get_active_categories(self) -> List[str]:
        """Get categories that should be active right now."""
        slot = self.get_current_slot()
        if slot:
            return slot.categories
        return ["Technology", "World"]

    def get_intensity(self) -> float:
        """Get current browsing intensity (0.0 - 1.0)."""
        slot = self.get_current_slot()
        if slot:
            return slot.intensity
        return 0.3

    def should_take_break(self) -> bool:
        """Check if it's break time."""
        slot = self.get_current_slot()
        if slot:
            return random.random() < slot.break_probability
        return False


DAILY_ROUTINES: Dict[str, DailyRoutine] = {
    "office_worker": DailyRoutine(
        name="Office Worker",
        description="9-to-5 knowledge worker. News in morning, work during day, entertainment at night.",
        persona="corporate",
        time_slots=[
            TimeSlot(6, 8, ["World", "Trending", "Health"],
                     0.5, "Morning news with coffee",
                     search_queries=["morning news today", "weather forecast", "stock market premarket"],
                     break_probability=0.1),
            TimeSlot(8, 9, ["Technology", "Trending"],
                     0.3, "Commute browsing",
                     search_queries=["traffic updates", "train delays"],
                     break_probability=0.05),
            TimeSlot(9, 12, ["Technology", "World", "SocialNetworkAds"],
                     0.7, "Morning work + quick breaks",
                     search_queries=["how to", "best practices", "tutorial"],
                     break_probability=0.15),
            TimeSlot(12, 13, ["Lifestyle", "Hobbies", "SocialMedia"],
                     0.6, "Lunch break browsing",
                     search_queries=["restaurants near me", "lunch recipes", "food delivery"],
                     break_probability=0.3),
            TimeSlot(13, 17, ["Technology", "World", "Trending"],
                     0.6, "Afternoon work",
                     search_queries=["documentation", "stackoverflow", "github"],
                     break_probability=0.1),
            TimeSlot(17, 19, ["Trending", "SocialMedia", "Hobbies"],
                     0.5, "Post-work decompression",
                     search_queries=["things to do tonight", "new movies", "happy hour"],
                     break_probability=0.2),
            TimeSlot(19, 22, ["Lifestyle", "Hobbies", "SocialMedia", "Tabloids"],
                     0.6, "Evening leisure",
                     search_queries=["Netflix recommendations", "recipes for dinner", "DIY projects"],
                     break_probability=0.15),
            TimeSlot(22, 0, ["SocialMedia", "Hobbies"],
                     0.3, "Pre-sleep scrolling",
                     search_queries=["reddit", "youtube", "funny videos"],
                     break_probability=0.3),
        ],
        weekend_modifier={
            "shift_hours": 2,
            "intensity_mult": 0.6,
            "categories": ["Hobbies", "Lifestyle", "SocialMedia", "Tabloids"],
        },
    ),

    "student": DailyRoutine(
        name="College Student",
        description="Late nights, research binges, and procrastination masquerading as productivity.",
        persona="tech_enthusiast",
        time_slots=[
            TimeSlot(9, 11, ["SocialMedia", "Trending", "Lifestyle"],
                     0.4, "Late start, checking socials",
                     search_queries=["reddit front page", "tiktok", "memes"],
                     break_probability=0.1),
            TimeSlot(11, 13, ["Technology", "World"],
                     0.6, "Morning class topics",
                     search_queries=["lecture notes", "Khan Academy", "Coursera"],
                     break_probability=0.15),
            TimeSlot(13, 14, ["SocialMedia", "Lifestyle", "Hobbies"],
                     0.5, "Lunch + procrastination",
                     search_queries=["meal prep easy", "cheap food near me"],
                     break_probability=0.3),
            TimeSlot(14, 18, ["Technology", "World", "Privacy"],
                     0.7, "Study/research session",
                     search_queries=["research paper", "Wikipedia", "scholarly articles", "study guide"],
                     break_probability=0.2),
            TimeSlot(18, 21, ["SocialMedia", "Hobbies", "Lifestyle", "Tabloids"],
                     0.6, "Evening socializing/gaming",
                     search_queries=["Discord", "Twitch", "Steam", "Netflix"],
                     break_probability=0.1),
            TimeSlot(21, 2, ["Technology", "SocialMedia", "Trending"],
                     0.8, "Late night study/browsing",
                     search_queries=["how to write essay fast", "caffeine effects", "all nighter tips"],
                     break_probability=0.05),
        ],
        weekend_modifier={
            "shift_hours": 3,
            "intensity_mult": 0.5,
        },
    ),

    "remote_worker": DailyRoutine(
        name="Remote Worker",
        description="Working from home. Blurred lines between work and everything else.",
        persona="tech_enthusiast",
        time_slots=[
            TimeSlot(7, 9, ["World", "Technology", "Health"],
                     0.5, "Morning routine + news",
                     search_queries=["morning news", "weather", "workout at home"],
                     break_probability=0.1),
            TimeSlot(9, 11, ["Technology", "World"],
                     0.8, "Deep work morning block",
                     search_queries=["Slack", "Jira", "code review", "pull request"],
                     break_probability=0.05),
            TimeSlot(11, 12, ["Lifestyle", "SocialMedia", "Hobbies"],
                     0.4, "Mid-morning break",
                     search_queries=["coffee delivery", "standing desk", "home office setup"],
                     break_probability=0.3),
            TimeSlot(12, 13, ["Lifestyle", "Hobbies"],
                     0.3, "Lunch + household tasks",
                     search_queries=["quick lunch ideas", "laundry tips", "meal delivery"],
                     break_probability=0.4),
            TimeSlot(13, 16, ["Technology", "World", "Trending"],
                     0.7, "Afternoon work",
                     search_queries=["documentation", "API reference", "deployment guide"],
                     break_probability=0.1),
            TimeSlot(16, 17, ["SocialMedia", "Trending", "Hobbies"],
                     0.4, "Winding down work",
                     search_queries=["afternoon slump", "quick break activities"],
                     break_probability=0.25),
            TimeSlot(17, 20, ["Hobbies", "Lifestyle", "SocialMedia"],
                     0.5, "Personal time",
                     search_queries=["running routes near me", "guitar lessons", "book recommendations"],
                     break_probability=0.2),
            TimeSlot(20, 23, ["SocialMedia", "Lifestyle", "Tabloids", "Hobbies"],
                     0.5, "Evening relaxation",
                     search_queries=["streaming new releases", "podcast recommendations"],
                     break_probability=0.15),
        ],
        weekend_modifier={
            "shift_hours": 1,
            "intensity_mult": 0.4,
            "categories": ["Hobbies", "Lifestyle", "SocialMedia"],
        },
    ),

    "night_owl": DailyRoutine(
        name="Night Owl",
        description="Peak productivity after midnight. The sun is optional.",
        persona="tech_enthusiast",
        time_slots=[
            TimeSlot(12, 14, ["World", "Trending", "SocialMedia"],
                     0.3, "Waking up, catching up",
                     search_queries=["what happened today", "morning news", "reddit top posts"],
                     break_probability=0.1),
            TimeSlot(14, 18, ["Technology", "World", "Privacy"],
                     0.5, "Afternoon productivity",
                     search_queries=["programming tutorial", "open source projects"],
                     break_probability=0.15),
            TimeSlot(18, 21, ["SocialMedia", "Lifestyle", "Hobbies"],
                     0.6, "Evening socializing",
                     search_queries=["Discord servers", "online games", "Twitch streams"],
                     break_probability=0.1),
            TimeSlot(21, 2, ["Technology", "Privacy", "Hobbies"],
                     0.9, "Peak hours - deep focus",
                     search_queries=["advanced tutorial", "deep dive", "security research"],
                     break_probability=0.05),
            TimeSlot(2, 4, ["Technology", "SocialMedia"],
                     0.6, "Late night rabbit holes",
                     search_queries=["Wikipedia random", "obscure topics", "3am questions"],
                     break_probability=0.1),
            TimeSlot(4, 6, ["SocialMedia", "Lifestyle"],
                     0.2, "Pre-sleep wind down",
                     search_queries=["relaxing music", "sleep tips", "insomnia help"],
                     break_probability=0.4),
        ],
    ),

    "parent": DailyRoutine(
        name="Busy Parent",
        description="Browsing in stolen moments between school runs and snack requests.",
        persona="health_conscious",
        time_slots=[
            TimeSlot(5, 7, ["World", "Health", "Lifestyle"],
                     0.4, "Early morning quiet time",
                     search_queries=["morning news", "healthy breakfast ideas", "workout 15 min"],
                     break_probability=0.2),
            TimeSlot(7, 9, ["Lifestyle", "Trending"],
                     0.2, "Morning chaos - minimal browsing",
                     search_queries=["school closures", "weather", "packed lunch ideas"],
                     break_probability=0.5),
            TimeSlot(9, 12, ["Lifestyle", "Health", "Hobbies", "World"],
                     0.6, "Kids at school - productive time",
                     search_queries=["meal planning", "home organization", "parenting advice"],
                     break_probability=0.15),
            TimeSlot(12, 15, ["Lifestyle", "SocialMedia", "Hobbies"],
                     0.4, "Afternoon errands + browsing",
                     search_queries=["grocery deals", "kid activities near me", "pediatrician"],
                     break_probability=0.3),
            TimeSlot(15, 18, ["Lifestyle", "Hobbies"],
                     0.2, "After school - minimal browsing",
                     search_queries=["homework help", "science fair ideas", "kids recipes"],
                     break_probability=0.5),
            TimeSlot(18, 20, ["Lifestyle"],
                     0.1, "Dinner and bedtime routine",
                     break_probability=0.7),
            TimeSlot(20, 23, ["SocialMedia", "Lifestyle", "Tabloids", "Hobbies"],
                     0.7, "Kids asleep - ME TIME",
                     search_queries=["Netflix what to watch", "book club", "wine reviews", "weekend getaways"],
                     break_probability=0.05),
        ],
        weekend_modifier={
            "intensity_mult": 0.4,
            "categories": ["Lifestyle", "Hobbies", "SocialMedia"],
        },
    ),

    "retiree": DailyRoutine(
        name="Retiree",
        description="All the time in the world. Steady, deliberate browsing with a cup of tea.",
        persona="news_junkie",
        time_slots=[
            TimeSlot(6, 8, ["World", "Health"],
                     0.3, "Early morning news + health",
                     search_queries=["morning news", "weather forecast", "health tips seniors"],
                     break_probability=0.1),
            TimeSlot(8, 10, ["World", "Trending", "Lifestyle"],
                     0.5, "Breakfast reading",
                     search_queries=["today headlines", "local news", "obituaries"],
                     break_probability=0.2),
            TimeSlot(10, 12, ["Hobbies", "Lifestyle", "Health"],
                     0.4, "Morning activities",
                     search_queries=["gardening tips", "woodworking plans", "knitting patterns"],
                     break_probability=0.3),
            TimeSlot(12, 14, ["Lifestyle", "Hobbies"],
                     0.3, "Lunch and rest",
                     break_probability=0.4),
            TimeSlot(14, 17, ["Hobbies", "World", "Technology"],
                     0.5, "Afternoon interests",
                     search_queries=["genealogy search", "travel deals", "grandkid gifts"],
                     break_probability=0.2),
            TimeSlot(17, 19, ["World", "Lifestyle"],
                     0.4, "Evening news",
                     search_queries=["evening news", "weather tomorrow", "local events"],
                     break_probability=0.2),
            TimeSlot(19, 21, ["Lifestyle", "Hobbies", "SocialMedia"],
                     0.3, "Evening leisure",
                     search_queries=["crossword puzzle", "sudoku online", "classic movies"],
                     break_probability=0.3),
        ],
    ),
}


def get_routine(name: str) -> Optional[DailyRoutine]:
    """Get a daily routine by name."""
    return DAILY_ROUTINES.get(name)


def list_routines() -> None:
    """Print all available daily routines."""
    print("\nAvailable Daily Routines:\n")
    for name, routine in DAILY_ROUTINES.items():
        current_slot = routine.get_current_slot()
        current_desc = current_slot.description if current_slot else "inactive"
        print(f"  {name:20s} - {routine.description}")
        print(f"  {'':20s}   Now: {current_desc} (intensity: {routine.get_intensity():.0%})")
    print()


def get_routine_categories(routine_name: str) -> List[str]:
    """Get currently active categories for a routine."""
    routine = DAILY_ROUTINES.get(routine_name)
    if routine:
        return routine.get_active_categories()
    return ["Technology", "World"]


def get_routine_search_queries(routine_name: str) -> List[str]:
    """Get contextual search queries for the current time slot."""
    routine = DAILY_ROUTINES.get(routine_name)
    if routine:
        slot = routine.get_current_slot()
        if slot and slot.search_queries:
            return slot.search_queries
    return []


if __name__ == "__main__":
    list_routines()
    print("\nCurrent time slot details:\n")
    for name, routine in DAILY_ROUTINES.items():
        slot = routine.get_current_slot()
        if slot:
            print(f"  {name}: {slot.description}")
            print(f"    Categories: {', '.join(slot.categories)}")
            print(f"    Intensity: {slot.intensity:.0%}")
            print(f"    Break chance: {slot.break_probability:.0%}")
        else:
            print(f"  {name}: No active slot")
        print()
