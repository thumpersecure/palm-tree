#!/usr/bin/env python3
"""
Geo-Rotation Mode - Browse like a globe-trotter.

"Today I'm in Tokyo. Tomorrow, Reykjavik. My ISP is very confused."

This module rotates through geographic locations, adjusting language
headers, timezone hints, Accept-Language, and location-based cookies
to make it look like you're browsing from a different country every
few minutes.

Trackers that build location profiles will see someone teleporting
around the world at impossible speeds. As they should.
"""

__version__ = "1.0.0"

import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime


@dataclass
class GeoLocation:
    """A geographic browsing location with all its fingerprint data."""
    country_code: str
    country_name: str
    language_code: str
    accept_language: str
    timezone: str
    currency: str
    locale_sites: List[str]
    search_engine: str
    latitude: float
    longitude: float


GEO_LOCATIONS: List[GeoLocation] = [
    GeoLocation(
        country_code="US", country_name="United States",
        language_code="en", accept_language="en-US,en;q=0.9",
        timezone="America/New_York", currency="USD",
        locale_sites=["https://www.nytimes.com", "https://www.washingtonpost.com", "https://www.cnn.com", "https://www.usatoday.com"],
        search_engine="https://www.google.com/search?q=",
        latitude=40.7128, longitude=-74.0060,
    ),
    GeoLocation(
        country_code="GB", country_name="United Kingdom",
        language_code="en", accept_language="en-GB,en;q=0.9",
        timezone="Europe/London", currency="GBP",
        locale_sites=["https://www.bbc.co.uk", "https://www.theguardian.com", "https://www.telegraph.co.uk", "https://www.independent.co.uk"],
        search_engine="https://www.google.co.uk/search?q=",
        latitude=51.5074, longitude=-0.1278,
    ),
    GeoLocation(
        country_code="DE", country_name="Germany",
        language_code="de", accept_language="de-DE,de;q=0.9,en;q=0.7",
        timezone="Europe/Berlin", currency="EUR",
        locale_sites=["https://www.spiegel.de", "https://www.zeit.de", "https://www.faz.net", "https://www.sueddeutsche.de"],
        search_engine="https://www.google.de/search?q=",
        latitude=52.5200, longitude=13.4050,
    ),
    GeoLocation(
        country_code="FR", country_name="France",
        language_code="fr", accept_language="fr-FR,fr;q=0.9,en;q=0.7",
        timezone="Europe/Paris", currency="EUR",
        locale_sites=["https://www.lemonde.fr", "https://www.lefigaro.fr", "https://www.liberation.fr", "https://www.france24.com/fr/"],
        search_engine="https://www.google.fr/search?q=",
        latitude=48.8566, longitude=2.3522,
    ),
    GeoLocation(
        country_code="JP", country_name="Japan",
        language_code="ja", accept_language="ja-JP,ja;q=0.9,en;q=0.5",
        timezone="Asia/Tokyo", currency="JPY",
        locale_sites=["https://www.asahi.com", "https://www.yomiuri.co.jp", "https://www.nhk.or.jp", "https://www.japantimes.co.jp"],
        search_engine="https://www.google.co.jp/search?q=",
        latitude=35.6762, longitude=139.6503,
    ),
    GeoLocation(
        country_code="BR", country_name="Brazil",
        language_code="pt", accept_language="pt-BR,pt;q=0.9,en;q=0.5",
        timezone="America/Sao_Paulo", currency="BRL",
        locale_sites=["https://www.globo.com", "https://www.folha.uol.com.br", "https://www.uol.com.br"],
        search_engine="https://www.google.com.br/search?q=",
        latitude=-23.5505, longitude=-46.6333,
    ),
    GeoLocation(
        country_code="AU", country_name="Australia",
        language_code="en", accept_language="en-AU,en;q=0.9",
        timezone="Australia/Sydney", currency="AUD",
        locale_sites=["https://www.abc.net.au", "https://www.smh.com.au", "https://www.news.com.au", "https://www.theaustralian.com.au"],
        search_engine="https://www.google.com.au/search?q=",
        latitude=-33.8688, longitude=151.2093,
    ),
    GeoLocation(
        country_code="IN", country_name="India",
        language_code="en", accept_language="en-IN,en;q=0.9,hi;q=0.7",
        timezone="Asia/Kolkata", currency="INR",
        locale_sites=["https://www.thehindu.com", "https://www.ndtv.com", "https://www.hindustantimes.com", "https://timesofindia.indiatimes.com"],
        search_engine="https://www.google.co.in/search?q=",
        latitude=28.6139, longitude=77.2090,
    ),
    GeoLocation(
        country_code="CA", country_name="Canada",
        language_code="en", accept_language="en-CA,en;q=0.9,fr;q=0.5",
        timezone="America/Toronto", currency="CAD",
        locale_sites=["https://www.cbc.ca", "https://www.theglobeandmail.com", "https://www.nationalpost.com"],
        search_engine="https://www.google.ca/search?q=",
        latitude=43.6532, longitude=-79.3832,
    ),
    GeoLocation(
        country_code="KR", country_name="South Korea",
        language_code="ko", accept_language="ko-KR,ko;q=0.9,en;q=0.5",
        timezone="Asia/Seoul", currency="KRW",
        locale_sites=["https://www.chosun.com", "https://www.donga.com", "https://www.hani.co.kr"],
        search_engine="https://www.google.co.kr/search?q=",
        latitude=37.5665, longitude=126.9780,
    ),
    GeoLocation(
        country_code="MX", country_name="Mexico",
        language_code="es", accept_language="es-MX,es;q=0.9,en;q=0.5",
        timezone="America/Mexico_City", currency="MXN",
        locale_sites=["https://www.eluniversal.com.mx", "https://www.milenio.com", "https://www.reforma.com"],
        search_engine="https://www.google.com.mx/search?q=",
        latitude=19.4326, longitude=-99.1332,
    ),
    GeoLocation(
        country_code="SE", country_name="Sweden",
        language_code="sv", accept_language="sv-SE,sv;q=0.9,en;q=0.7",
        timezone="Europe/Stockholm", currency="SEK",
        locale_sites=["https://www.dn.se", "https://www.svd.se", "https://www.svt.se"],
        search_engine="https://www.google.se/search?q=",
        latitude=59.3293, longitude=18.0686,
    ),
    GeoLocation(
        country_code="NL", country_name="Netherlands",
        language_code="nl", accept_language="nl-NL,nl;q=0.9,en;q=0.7",
        timezone="Europe/Amsterdam", currency="EUR",
        locale_sites=["https://www.nos.nl", "https://www.telegraaf.nl", "https://www.volkskrant.nl"],
        search_engine="https://www.google.nl/search?q=",
        latitude=52.3676, longitude=4.9041,
    ),
    GeoLocation(
        country_code="IT", country_name="Italy",
        language_code="it", accept_language="it-IT,it;q=0.9,en;q=0.5",
        timezone="Europe/Rome", currency="EUR",
        locale_sites=["https://www.corriere.it", "https://www.repubblica.it", "https://www.lastampa.it"],
        search_engine="https://www.google.it/search?q=",
        latitude=41.9028, longitude=12.4964,
    ),
    GeoLocation(
        country_code="ES", country_name="Spain",
        language_code="es", accept_language="es-ES,es;q=0.9,en;q=0.5",
        timezone="Europe/Madrid", currency="EUR",
        locale_sites=["https://www.elpais.com", "https://www.elmundo.es", "https://www.abc.es"],
        search_engine="https://www.google.es/search?q=",
        latitude=40.4168, longitude=-3.7038,
    ),
    GeoLocation(
        country_code="PL", country_name="Poland",
        language_code="pl", accept_language="pl-PL,pl;q=0.9,en;q=0.5",
        timezone="Europe/Warsaw", currency="PLN",
        locale_sites=["https://www.gazeta.pl", "https://www.onet.pl", "https://www.wp.pl"],
        search_engine="https://www.google.pl/search?q=",
        latitude=52.2297, longitude=21.0122,
    ),
]


class GeoRotator:
    """
    Rotates browsing location on a schedule.

    Makes it look like you're jet-setting across the globe while
    you're actually in your pajamas.
    """

    def __init__(
        self,
        rotation_interval: int = 300,
        locations: Optional[List[str]] = None,
        random_order: bool = True,
    ):
        """
        Args:
            rotation_interval: Seconds between location changes
            locations: List of country codes to rotate through (None = all)
            random_order: Shuffle location order vs sequential
        """
        self.rotation_interval = rotation_interval

        if locations:
            self.locations = [
                loc for loc in GEO_LOCATIONS
                if loc.country_code in [c.upper() for c in locations]
            ]
            if not self.locations:
                self.locations = GEO_LOCATIONS
        else:
            self.locations = list(GEO_LOCATIONS)

        if random_order:
            random.shuffle(self.locations)

        self._current_index = 0
        self._last_rotation = time.time()
        self._rotation_count = 0
        self._current: GeoLocation = self.locations[0]

    @property
    def current(self) -> GeoLocation:
        """Get the current geo location, rotating if needed."""
        now = time.time()
        if now - self._last_rotation >= self.rotation_interval:
            self._rotate()
        return self._current

    def _rotate(self):
        """Move to next location."""
        self._current_index = (self._current_index + 1) % len(self.locations)
        self._current = self.locations[self._current_index]
        self._last_rotation = time.time()
        self._rotation_count += 1

    def force_rotate(self) -> GeoLocation:
        """Force an immediate rotation."""
        self._rotate()
        return self._current

    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers matching the current geo location."""
        loc = self.current
        return {
            "Accept-Language": loc.accept_language,
        }

    def get_locale_url(self) -> str:
        """Get a URL specific to the current locale."""
        loc = self.current
        return random.choice(loc.locale_sites)

    def get_geo_cookie(self) -> str:
        """Generate a fake geolocation cookie matching current location."""
        loc = self.current
        return (
            f"_geo={loc.country_code}; "
            f"_tz={loc.timezone.replace('/', '_')}; "
            f"_cur={loc.currency}; "
            f"_loc={loc.latitude:.2f},{loc.longitude:.2f}"
        )

    def get_stats(self) -> Dict:
        return {
            "current_location": f"{self.current.country_name} ({self.current.country_code})",
            "rotation_count": self._rotation_count,
            "locations_available": len(self.locations),
            "rotation_interval": self.rotation_interval,
        }


def list_locations() -> None:
    """Print all available geo locations."""
    print("\nAvailable Geo Locations:\n")
    for loc in GEO_LOCATIONS:
        print(f"  {loc.country_code:4s} - {loc.country_name:20s} [{loc.timezone}]")
    print()


if __name__ == "__main__":
    list_locations()

    rotator = GeoRotator(rotation_interval=5)
    print(f"Current: {rotator.current.country_name}")

    for _ in range(5):
        loc = rotator.force_rotate()
        print(f"Rotated to: {loc.country_name} ({loc.country_code})")
        print(f"  Headers: {rotator.get_headers()}")
        print(f"  Cookie: {rotator.get_geo_cookie()}")
        print(f"  Local site: {rotator.get_locale_url()}")
        print()
