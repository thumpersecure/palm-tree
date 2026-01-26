#!/usr/bin/env python3
"""
Identity Forge - Mint fresh humans on demand.

"We're not playing god, we're playing HR department."

This module generates complete fake identities for each request,
making it impossible for trackers to build a consistent profile.
Every request is a different person with different cookies, headers,
and existential crises.
"""

import random
import string
import hashlib
import base64
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from datetime import datetime, timedelta

# Try to import faker, fall back to built-in generation if not available
try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False


@dataclass
class FakeHuman:
    """
    A complete fake human identity.

    Born in the fires of randomness, destined to make one HTTP request,
    then vanish like tears in rain.
    """
    # Basic info
    name: str
    email: str
    username: str

    # Location (for headers)
    country_code: str
    language_code: str
    timezone: str
    latitude: float
    longitude: float
    city: str

    # Device info
    user_agent: str
    screen_resolution: str
    color_depth: int
    platform: str

    # Browser fingerprint
    session_id: str
    canvas_hash: str
    webgl_hash: str
    audio_hash: str
    font_hash: str

    # Tracking cookies (fake ones to confuse trackers)
    ga_cookie: str  # Fake Google Analytics
    fb_cookie: str  # Fake Facebook pixel
    ad_cookies: Dict[str, str] = field(default_factory=dict)

    # Optional extended info
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    credit_card: Optional[str] = None  # Fake but valid format

    def get_headers(self) -> Dict[str, str]:
        """
        Generate HTTP headers for this identity.

        Returns headers that make this fake human look very real
        to any tracker unfortunate enough to encounter them.
        """
        headers = {
            "User-Agent": self.user_agent,
            "Accept-Language": f"{self.language_code}-{self.country_code},{self.language_code};q=0.9,en;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": random.choice(["keep-alive", "close"]),
            "DNT": str(random.randint(0, 1)),
            "Sec-CH-UA-Platform": f'"{self.platform}"',
            "Sec-CH-UA-Mobile": "?0" if "Mobile" not in self.user_agent else "?1",
        }

        # Add fake cookies
        cookies = [
            f"_ga={self.ga_cookie}",
            f"_fbp={self.fb_cookie}",
            f"session={self.session_id}",
        ]
        for name, value in self.ad_cookies.items():
            cookies.append(f"{name}={value}")

        headers["Cookie"] = "; ".join(cookies)

        # Sometimes add geolocation hints
        if random.random() > 0.7:
            headers["X-Forwarded-For"] = self._generate_fake_ip()

        return headers

    def _generate_fake_ip(self) -> str:
        """Generate a fake but plausible IP address."""
        return f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


class IdentityForge:
    """
    The Identity Forge - Where fake people are born.

    "Every human you meet today could be one of our creations."
        - Marketing slogan we definitely shouldn't use

    This class mints complete fake identities with consistent
    fingerprints, making each HTTP request appear to come from
    a unique, real person.
    """

    # User agents by platform (expanded with humor)
    USER_AGENTS = {
        "Windows": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            # The classics
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",  # Grandma's computer
        ],
        "macOS": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ],
        "Linux": [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ],
        "iOS": [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        ],
        "Android": [
            "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
        ],
        # The fun ones
        "Exotic": [
            "Mozilla/5.0 (PlayStation; PlayStation 5/1.0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",  # Gamer
            "Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/609.4 (KHTML, like Gecko) NF/6.0.2.21.3 NintendoBrowser/5.1.0.22474",  # Nintendo fan
            "Mozilla/5.0 (SMART-TV; Linux; Tizen 6.5) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.0 Chrome/85.0.4183.93 TV Safari/537.36",  # Couch potato
            "Mozilla/5.0 (Linux; Android 10; SM-R800) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",  # Smart Watch (because why not)
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Tesla/2021.44.25.2",  # Tesla browser (stuck in traffic)
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",  # You ARE the crawler now
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",  # Meta's finest
            "Twitterbot/1.0",  # Elon's creation
            "Mozilla/5.0 (SmartFridge; Linux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 LG/1.0",  # Your fridge, browsing recipes
        ],
    }

    # Screen resolutions with their platforms
    SCREEN_RESOLUTIONS = {
        "desktop": ["1920x1080", "2560x1440", "1366x768", "1536x864", "3840x2160", "1440x900", "1680x1050"],
        "mobile": ["390x844", "360x640", "375x667", "414x896", "428x926"],
        "tablet": ["768x1024", "1024x768", "1280x800", "2048x1536"],
        "exotic": ["800x480", "1280x720", "3440x1440"],  # TV, watch, ultrawide
    }

    # Countries and their languages
    LOCALES = [
        ("US", "en", "America/New_York"),
        ("US", "en", "America/Los_Angeles"),
        ("US", "en", "America/Chicago"),
        ("GB", "en", "Europe/London"),
        ("CA", "en", "America/Toronto"),
        ("AU", "en", "Australia/Sydney"),
        ("DE", "de", "Europe/Berlin"),
        ("FR", "fr", "Europe/Paris"),
        ("ES", "es", "Europe/Madrid"),
        ("IT", "it", "Europe/Rome"),
        ("JP", "ja", "Asia/Tokyo"),
        ("KR", "ko", "Asia/Seoul"),
        ("BR", "pt", "America/Sao_Paulo"),
        ("MX", "es", "America/Mexico_City"),
        ("IN", "en", "Asia/Kolkata"),
        ("NL", "nl", "Europe/Amsterdam"),
        ("SE", "sv", "Europe/Stockholm"),
        ("NO", "no", "Europe/Oslo"),
        ("PL", "pl", "Europe/Warsaw"),
        ("RU", "ru", "Europe/Moscow"),
    ]

    # Job titles for extra realism (and humor)
    JOB_TITLES = [
        "Software Engineer", "Product Manager", "Data Scientist", "UX Designer",
        "Marketing Manager", "Sales Representative", "Accountant", "HR Specialist",
        "Project Manager", "Business Analyst", "DevOps Engineer", "Full Stack Developer",
        # The fun ones
        "Professional Netflix Watcher", "Chief Vibes Officer", "Wizard of Light Bulb Moments",
        "Digital Overlord", "Retail Jedi", "Galactic Viceroy of Research Excellence",
        "Chief Troublemaker", "Director of First Impressions", "Happiness Engineer",
    ]

    # Company name generators
    COMPANY_SUFFIXES = ["Inc", "LLC", "Corp", "Co", "Ltd", "Group", "Solutions", "Technologies", "Dynamics", "Labs"]
    COMPANY_WORDS = ["Tech", "Digital", "Global", "Smart", "Cloud", "Data", "Cyber", "Net", "Web", "App",
                     "Quantum", "Infinite", "Dynamic", "Synergy", "Nexus", "Vertex", "Matrix", "Alpha", "Omega"]

    def __init__(self, use_faker: bool = True):
        """
        Initialize the Identity Forge.

        Args:
            use_faker: Whether to use the Faker library if available.
                      Falls back to built-in generation if False or unavailable.
        """
        self.use_faker = use_faker and FAKER_AVAILABLE
        if self.use_faker:
            self.faker = Faker()
            # Add some locale variety
            self.faker_locales = {
                'en_US': Faker('en_US'),
                'en_GB': Faker('en_GB'),
                'de_DE': Faker('de_DE'),
                'fr_FR': Faker('fr_FR'),
                'es_ES': Faker('es_ES'),
                'ja_JP': Faker('ja_JP'),
            }

    def mint_identity(self, platform: Optional[str] = None, exotic_chance: float = 0.15) -> FakeHuman:
        """
        Mint a fresh fake human identity.

        This human has never existed, will make one request, and then
        vanish into the void. Like a mayfly, but for HTTP.

        Args:
            platform: Force a specific platform (Windows, macOS, Linux, iOS, Android, Exotic)
            exotic_chance: Probability of getting an exotic device (PlayStation, Smart TV, etc.)

        Returns:
            A FakeHuman with a complete fake identity
        """
        # Decide platform
        if platform is None:
            if random.random() < exotic_chance:
                platform = "Exotic"
            else:
                platform = random.choice(["Windows", "macOS", "Linux", "iOS", "Android"])

        # Get user agent
        user_agent = random.choice(self.USER_AGENTS.get(platform, self.USER_AGENTS["Windows"]))

        # Get location
        country_code, language_code, timezone = random.choice(self.LOCALES)

        # Generate screen resolution based on platform
        if platform in ["iOS", "Android"]:
            resolution_type = "mobile"
        elif platform == "Exotic":
            resolution_type = random.choice(["desktop", "exotic"])
        else:
            resolution_type = random.choice(["desktop", "tablet"])

        screen_resolution = random.choice(self.SCREEN_RESOLUTIONS[resolution_type])

        # Generate the person
        if self.use_faker:
            return self._mint_with_faker(
                platform=platform,
                user_agent=user_agent,
                country_code=country_code,
                language_code=language_code,
                timezone=timezone,
                screen_resolution=screen_resolution,
            )
        else:
            return self._mint_builtin(
                platform=platform,
                user_agent=user_agent,
                country_code=country_code,
                language_code=language_code,
                timezone=timezone,
                screen_resolution=screen_resolution,
            )

    def _mint_with_faker(self, **kwargs) -> FakeHuman:
        """Mint identity using Faker library for extra realism."""
        # Pick a faker locale that matches
        lang = kwargs['language_code']
        locale_key = f"{lang}_{kwargs['country_code']}"
        faker = self.faker_locales.get(locale_key, self.faker)

        name = faker.name()

        return FakeHuman(
            name=name,
            email=faker.email(),
            username=faker.user_name(),
            country_code=kwargs['country_code'],
            language_code=kwargs['language_code'],
            timezone=kwargs['timezone'],
            latitude=float(faker.latitude()),
            longitude=float(faker.longitude()),
            city=faker.city(),
            user_agent=kwargs['user_agent'],
            screen_resolution=kwargs['screen_resolution'],
            color_depth=random.choice([24, 32]),
            platform=kwargs['platform'],
            session_id=self._generate_session_id(),
            canvas_hash=self._generate_fingerprint_hash("canvas"),
            webgl_hash=self._generate_fingerprint_hash("webgl"),
            audio_hash=self._generate_fingerprint_hash("audio"),
            font_hash=self._generate_fingerprint_hash("fonts"),
            ga_cookie=self._generate_ga_cookie(),
            fb_cookie=self._generate_fb_cookie(),
            ad_cookies=self._generate_ad_cookies(),
            phone=faker.phone_number(),
            job_title=faker.job() if random.random() > 0.3 else random.choice(self.JOB_TITLES),
            company=faker.company(),
            credit_card=faker.credit_card_number() if random.random() > 0.5 else None,
        )

    def _mint_builtin(self, **kwargs) -> FakeHuman:
        """Mint identity using built-in generation (no Faker dependency)."""
        name = self._generate_name()
        username = name.lower().replace(" ", "_") + str(random.randint(1, 999))

        return FakeHuman(
            name=name,
            email=f"{username}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com'])}",
            username=username,
            country_code=kwargs['country_code'],
            language_code=kwargs['language_code'],
            timezone=kwargs['timezone'],
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            city=self._generate_city_name(),
            user_agent=kwargs['user_agent'],
            screen_resolution=kwargs['screen_resolution'],
            color_depth=random.choice([24, 32]),
            platform=kwargs['platform'],
            session_id=self._generate_session_id(),
            canvas_hash=self._generate_fingerprint_hash("canvas"),
            webgl_hash=self._generate_fingerprint_hash("webgl"),
            audio_hash=self._generate_fingerprint_hash("audio"),
            font_hash=self._generate_fingerprint_hash("fonts"),
            ga_cookie=self._generate_ga_cookie(),
            fb_cookie=self._generate_fb_cookie(),
            ad_cookies=self._generate_ad_cookies(),
            phone=self._generate_phone(),
            job_title=random.choice(self.JOB_TITLES),
            company=self._generate_company_name(),
            credit_card=None,
        )

    def _generate_name(self) -> str:
        """Generate a random name."""
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                       "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
                       "Thomas", "Sarah", "Charles", "Karen", "Daniel", "Lisa", "Matthew", "Nancy",
                       "Anthony", "Betty", "Mark", "Margaret", "Donald", "Sandra", "Steven", "Ashley"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                      "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
                      "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    def _generate_city_name(self) -> str:
        """Generate a random city name."""
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
                  "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
                  "Fort Worth", "Columbus", "Charlotte", "Seattle", "Denver", "Boston"]
        return random.choice(cities)

    def _generate_company_name(self) -> str:
        """Generate a random company name."""
        word1 = random.choice(self.COMPANY_WORDS)
        word2 = random.choice(self.COMPANY_WORDS)
        suffix = random.choice(self.COMPANY_SUFFIXES)
        return f"{word1}{word2} {suffix}"

    def _generate_phone(self) -> str:
        """Generate a random phone number."""
        return f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"

    def _generate_session_id(self) -> str:
        """Generate a session ID that looks real."""
        return ''.join(random.choices(string.hexdigits.lower(), k=32))

    def _generate_fingerprint_hash(self, prefix: str) -> str:
        """Generate a fingerprint hash that looks legitimate."""
        data = f"{prefix}_{random.random()}_{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]

    def _generate_ga_cookie(self) -> str:
        """Generate a fake Google Analytics cookie."""
        ts = int(datetime.now().timestamp())
        return f"GA1.2.{random.randint(100000000, 999999999)}.{ts - random.randint(0, 86400 * 30)}"

    def _generate_fb_cookie(self) -> str:
        """Generate a fake Facebook pixel cookie."""
        ts = int(datetime.now().timestamp())
        return f"fb.1.{ts - random.randint(0, 86400 * 30)}.{random.randint(100000000, 999999999)}"

    def _generate_ad_cookies(self) -> Dict[str, str]:
        """Generate a variety of fake advertising cookies."""
        cookies = {}

        # Possible ad network cookies
        ad_cookies = [
            ("_gcl_au", lambda: f"1.1.{random.randint(100000000, 999999999)}.{int(datetime.now().timestamp())}"),
            ("_gid", lambda: f"GA1.2.{random.randint(100000000, 999999999)}.{int(datetime.now().timestamp())}"),
            ("_uetsid", lambda: ''.join(random.choices(string.hexdigits.lower(), k=32))),
            ("_uetvid", lambda: ''.join(random.choices(string.hexdigits.lower(), k=32))),
            ("IDE", lambda: base64.b64encode(f"{random.randint(1, 999999)}".encode()).decode()),
            ("NID", lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=64))),
            ("MUID", lambda: ''.join(random.choices(string.hexdigits.upper(), k=32))),
            ("fr", lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=24))),
        ]

        # Add 2-5 random ad cookies
        for name, generator in random.sample(ad_cookies, random.randint(2, 5)):
            cookies[name] = generator()

        return cookies

    def mint_batch(self, count: int, **kwargs) -> List[FakeHuman]:
        """
        Mint a batch of fake humans.

        For when you need an army of fake people.
        Like a very weird RPG party.

        Args:
            count: Number of humans to create
            **kwargs: Arguments to pass to mint_identity

        Returns:
            List of FakeHuman instances
        """
        return [self.mint_identity(**kwargs) for _ in range(count)]


# Convenience function
def generate_identity(**kwargs) -> FakeHuman:
    """
    Quick function to generate a single identity.

    For when you just need one fake human, right now.
    No questions asked.
    """
    forge = IdentityForge()
    return forge.mint_identity(**kwargs)


# For testing
if __name__ == "__main__":
    print("=" * 60)
    print("IDENTITY FORGE - Minting fake humans since 2024")
    print("=" * 60)

    forge = IdentityForge()

    print("\n[Minting 3 random humans...]\n")

    for i in range(3):
        human = forge.mint_identity()
        print(f"Human #{i+1}: {human.name}")
        print(f"  Email: {human.email}")
        print(f"  Location: {human.city}, {human.country_code}")
        print(f"  Job: {human.job_title} at {human.company}")
        print(f"  Device: {human.platform} ({human.screen_resolution})")
        print(f"  User-Agent: {human.user_agent[:60]}...")
        print()

    print("\n[Minting an exotic identity...]\n")
    exotic = forge.mint_identity(platform="Exotic")
    print(f"Exotic Human: {exotic.name}")
    print(f"  User-Agent: {exotic.user_agent}")
    print(f"  They're browsing from a... {exotic.platform}")

    print("\n[Sample HTTP Headers for this identity:]\n")
    headers = exotic.get_headers()
    for key, value in headers.items():
        print(f"  {key}: {value[:60]}{'...' if len(value) > 60 else ''}")
