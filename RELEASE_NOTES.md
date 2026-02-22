# 🥥 COCONUTS BY PALM-TREE 🌴 - Release Notes

*"If your browsing history doesn't confuse you, it's not private enough."*

---

## Version 3.4.0 - "The Globe-Trotter Update"

**Release Date:** February 2026

**Codename:** "I Browsed From 16 Countries Today (Without Leaving My Couch)"

---

### What's New (A.K.A. "Your Tracker Profile Is Now International")

Five brand-new features that make your traffic noise smarter, more realistic, and harder to track than ever. We went from "confuse the trackers" to "make the trackers question the nature of reality."

---

### Feature 1: Geo-Rotation Mode

**Browse like a globe-trotter without a passport.**

Automatically rotates your apparent location through 16 countries, changing Accept-Language headers, timezone hints, locale-specific cookies, and even visiting country-specific websites.

**Countries:** US, GB, DE, FR, JP, BR, AU, IN, CA, KR, MX, SE, NL, IT, ES, PL

```bash
# Rotate through all 16 locations every 5 minutes
python traffic_noise.py -c --geo-rotate

# Only rotate between specific countries
python traffic_noise.py -c --geo-rotate --geo-countries US,JP,DE,BR

# Faster rotation (every 2 minutes)
python traffic_noise.py -c --geo-rotate --geo-interval 120

# See all available locations
python traffic_noise.py --list-geo
```

**What trackers see:** "This person was in Tokyo 5 minutes ago and is now in Berlin. Are they on a teleporter?"

---

### Feature 2: Bandwidth Control

**Generate noise without nuking your Netflix.**

Smart bandwidth management with 5 preset profiles and adaptive time-of-day throttling. Uses a token bucket algorithm for smooth rate limiting with burst allowance.

**Profiles:**
| Profile | Speed | Requests | Use Case |
|---------|-------|----------|----------|
| `stealth` | 50 KB/s | 15/min | Barely detectable |
| `conservative` | 100 KB/s | 30/min | Shared connections |
| `moderate` | 500 KB/s | 60/min | **Recommended** |
| `aggressive` | 2000 KB/s | 120/min | Dedicated connections |
| `unlimited` | No limit | No limit | Full send |

```bash
# Recommended profile
python traffic_noise.py -c --bandwidth moderate

# Hard limit at 200 KB/s
python traffic_noise.py -c --bandwidth-max-kbps 200

# Disable adaptive throttling (normally backs off during work hours)
python traffic_noise.py -c --bandwidth moderate --no-adaptive

# See all profiles
python traffic_noise.py --list-bandwidth
```

**Adaptive mode:** Automatically reduces traffic during work hours (9-5) and increases at night, mimicking natural usage patterns.

---

### Feature 3: Proxy Chain Support

**Route your noise through proxies for extra anonymity.**

Full SOCKS5 and HTTP proxy support with multiple rotation strategies, automatic health checking, and failover.

```bash
# Single proxy
python traffic_noise.py -c --proxy socks5://proxy1.example.com:1080

# Multiple proxies with rotation
python traffic_noise.py -c --proxy socks5://proxy1:1080 --proxy http://proxy2:8080 --proxy-rotation random

# Load proxies from a file
python traffic_noise.py -c --proxy-file ~/proxies.txt --proxy-rotation fastest
```

**Rotation strategies:**
- `round_robin` - Cycle through proxies in order
- `random` - Pick a random proxy each time
- `least_used` - Use the proxy with fewest requests
- `fastest` - Use the proxy with lowest latency

**Proxy file format:**
```
# One proxy per line, comments with #
socks5://proxy1.example.com:1080
http://user:pass@proxy2.example.com:8080
```

---

### Feature 4: Session Export & Analytics

**Measure exactly how confused the trackers are.**

Full session analytics tracking with JSON export. See privacy score trends over time, category distribution, identity rotation history, and top sites visited.

```bash
# Enable session export
python traffic_noise.py -c --export

# Custom export path
python traffic_noise.py -c --export --export-path ./my_session.json
```

**Report includes:**
- Session summary (duration, requests, success rate, data transferred)
- Privacy score trend over time
- Category distribution breakdown
- Top sites visited
- Identity rotation history
- Geo-rotation history
- Hourly request distribution
- Error log

Reports are saved to `~/.traffic_noise/reports/` by default.

---

### Feature 5: Daily Routine Profiles

**Browse like a real human, not a random noise generator.**

Six pre-built daily routines that mimic realistic human browsing patterns throughout the day. Each routine defines what to browse, when, at what intensity, and includes natural breaks.

**Available Routines:**
| Routine | Description |
|---------|-------------|
| `office_worker` | 9-to-5: news morning, work afternoon, entertainment evening |
| `student` | Late start, study sessions, procrastination, late-night cramming |
| `remote_worker` | WFH: blurred work/life lines, mid-day breaks, afternoon focus |
| `night_owl` | Peak at midnight, wakes up at noon, deep focus after dark |
| `parent` | Stolen moments between school runs, ME TIME after bedtime |
| `retiree` | Steady, deliberate browsing with morning news and evening hobbies |

```bash
# Browse like an office worker
python traffic_noise.py -c --daily-routine office_worker

# Browse like a night owl
python traffic_noise.py -c --daily-routine night_owl

# See all routines and current activity
python traffic_noise.py --list-routines
```

**Weekend awareness:** Routines automatically adjust on weekends (later start, different categories, lower intensity).

---

### Technical Stuff

**New files:**
- `geo_rotate.py` - 16-country geo-rotation engine
- `bandwidth_control.py` - Token bucket rate limiter with adaptive profiles
- `proxy_chain.py` - Proxy pool manager with health checking
- `session_export.py` - Analytics tracker with JSON export
- `daily_routines.py` - Time-slot based daily behavior patterns

**Updated:**
- `traffic_noise.py` - All features integrated with CLI flags, display, and shutdown hooks
- Version bumped to 3.4.0

**New CLI flags:** 13 new command-line arguments
**New `--list` commands:** `--list-geo`, `--list-bandwidth`, `--list-routines`

---

### Dependencies

Still no new required dependencies! All v3.4.0 features use stdlib + existing deps:
```
httpx          # Now also used by proxy_chain
```

---

### Breaking Changes

None. All new features are opt-in via CLI flags. Your existing commands work exactly the same.

---

## Version 3.3.2 - "The Spicy Cat Update"

**Release Date:** February 2026

**Codename:** "My WiFi Is Broken (Again)"

---

### What's New (A.K.A. "Now Your Computer Looks Perpetually Broken")

Ever noticed how IT support people always seem to be googling the same problems over and over? Now you can too! This release makes your browsing profile look like you're eternally fighting with technology.

Inspired by the legendary spicy-cat approach to chaos generation.

---

### Issue Traffic Generator - The Star of the Show

**What it do:**
- Generates traffic that looks like you're troubleshooting computer problems
- 15 different issue types from "WiFi won't connect" to "help I have ransomware"
- Searches get progressively more desperate (just like real troubleshooting)
- One problem leads to another (WiFi → DNS → "should I buy a new router?")

**Why would you want this?**
- Your browsing profile now shows you as "that person who can't figure out technology"
- Data brokers think you're perpetually confused
- Advertisers start targeting you with IT support services instead of whatever embarrassing thing you actually searched

**How to use it:**
```bash
# Look like you can't get WiFi to work
python traffic_noise.py --simulate-issues wifi -c

# Look like you downloaded something sketchy
python traffic_noise.py --simulate-issues adware -c -w 5

# Full chaos - every problem at once
python traffic_noise.py --simulate-issues mixed -c --stealth --decoys

# See all available problems you can pretend to have
python traffic_noise.py --list-issues
```

---

### Frustration Mode - Because Real Troubleshooting Gets Desperate

We studied actual human behavior (read: watched people yell at their computers) and implemented realistic frustration escalation.

**Search #1:** `"wifi not connecting"`

**Search #3:** `"wifi not connecting fix"`

**Search #7:** `"why won't my wifi work please help"`

**Search #12:** `"WIFI STILL BROKEN NOTHING WORKS I'VE TRIED EVERYTHING"`

**Search #15:** `"best buy wifi routers free shipping"`

It's basically a simulation of every Thanksgiving when you visit your parents.

---

### Issue Chaining - One Problem Leads to Another

Just like in real life, one problem cascades into seventeen more:

```
WiFi Problems
    → "Maybe it's DNS?"
        → DNS Issues
            → "Did I break something?"
                → Factory Reset Guide
                    → "Wait, where did my files go?"
                        → Data Recovery Tools
                            → "I should have backed up"
                                → External Hard Drive Shopping
```

We call this "The Full IT Support Experience™"

---

### 15 Flavors of Technical Despair

| Category | Issue Types | Vibe |
|----------|-------------|------|
| **Network** | dns, ssl, wifi, vpn, networking | "The internet is a lie" |
| **System** | bsod, system, hardware, software | "My computer hates me" |
| **Malware** | adware, ransomware, cryptominer, malware | "I clicked something I shouldn't have" |
| **Config** | misconfigured | "I changed a setting and now everything's broken" |
| **Chaos** | mixed | "All of the above, simultaneously" |

---

### Technical Stuff (For the Nerds)

**New file:** `issue_traffic.py`
- `IssueTrafficGenerator` class - for when you want to programmatically pretend your computer is broken
- `IssueType` enum - 25+ ways your computer can theoretically fail
- `IssuePattern` dataclass - defines how each problem behaves
- Frustration escalation system - mathematically models human desperation
- Issue chaining logic - problems beget problems

**Fixed:**
- Removed duplicate MarkovChain class (it was defined twice, we were seeing double)
- Removed duplicate ChaosGenerator class (chaos shouldn't be THAT chaotic)
- Code is now 68 lines shorter and 100% less redundant

**Extended:**
- `NEWS_SITES` now has 17 new issue-related categories
- `--simulate-issues` supports 15 types (was 6, we tripled down)
- New `--list-issues` flag because remembering 15 things is hard

---

### Dependencies

None new! Still just:
```
httpx          # For pretending to browse
beautifulsoup4 # For soup-related activities
lxml           # Speed demon
rich           # Making terminals pretty
faker          # Generating fake humans (ethically)
```

---

### Breaking Changes

Absolutely none. We're not monsters.

Your old commands still work. New commands are additive. Sleep soundly.

---

### FAQ

**Q: Why would I want to look like I have computer problems?**
A: Because "person who can't figure out WiFi" is a way better advertising profile than whatever you actually browse.

**Q: Does this actually connect to malware sites?**
A: No! It searches for how to FIX malware. You look like a victim, not a villain.

**Q: My computer actually IS slow. Will this help?**
A: No, but at least the ads will be relevant now.

**Q: Can I simulate specific problems?**
A: Yes! `--simulate-issues bsod` if you want to look like a Windows user, `--simulate-issues cryptominer` if you want to look like you clicked a Discord link you shouldn't have.

---

### Acknowledgments

- Inspired by spicy-cat's approach to controlled chaos
- Thanks to everyone who's ever asked "have you tried turning it off and on again?"
- Special shoutout to DNS servers for being unreliable enough that we can realistically simulate you
- Dedicated to IT support workers everywhere. We see you. We appreciate you. We're sorry.

---

## Version 3.3 - "The Stealth Update"

**Release Date:** 2025

The one where we got sneaky.

**What it do:**
- **Stealth Mode:** Randomizes TLS fingerprints, header ordering, browser hints
- **Scheduled Profiles:** Different browsing at different times (work hours vs. 3am)
- **Privacy Score:** Real-time confusion metric (higher = more confusing)
- **Decoy Injection:** Fake interests, fake demographics, fake everything
- **Plugin System:** Load your own sites and personas
- **Interactive Mode:** For people who don't like reading documentation

---

## Version 2.0.0 - "The One Where We Added Coconuts"

**Release Date:** 2024

---

### What's New in v2.0

#### Coconut Mode - Headless Browser Army

Ever wanted to be 10 different people visiting 100 different websites simultaneously? No? Well, you can now anyway.

**What it do:**
- Spawns headless Chrome instances like they're going out of style
- Visits top 100 websites silently (no windows, just vibes)
- Each browser gets its own fake identity (we're method actors here)
- Configurable chaos levels from "polite visitor" to "digital flash mob"

**How to use it:**
```bash
python coconuts.py --coconuts --clones 3
```

---

#### Sleepy Mode - Fake Insomnia

For when you want your computer to pretend it can't sleep. Just like you at 3am scrolling through Reddit.

**What it do:**
- Generates realistic "can't sleep" browsing patterns
- Time-aware activity (slow at 3am, faster in morning)
- Optional Markov chain learning (fancy words for "it watches and learns")
- Makes you appear awake when you're actually touching grass

**How to use it:**
```bash
python coconuts.py --sleepy --duration 480  # 8 hours of fake insomnia
```

---

#### Quadcore Mode - 4 Terminals of Pure Chaos

Because one terminal is for amateurs.

**What it do:**
- Splits your terminal into 4 panes (requires tmux)
- Pane 1: Prime number calculations (CPU goes brrr)
- Pane 2: Traffic noise with headlines
- Pane 3: Packet simulation display
- Pane 4: Hacker movie nonsense ("Hacking the Gibson...")

**How to use it:**
```bash
python coconuts.py --quadcore
```

---

#### Identity Forge - Fake Human Factory

Every request now gets a complete fake human identity. We're basically playing The Sims but for HTTP requests.

**Generated for each request:**
- Name, email, username (all fake, legally speaking)
- Location, timezone, language
- Device fingerprint
- Browser cookies (fake ones)
- Job title (including "Chief Vibes Officer" and "Galactic Viceroy of Research Excellence")

---

### Technical Improvements (v2.0)

- **Bandwidth Throttling:** No longer nukes your Netflix streaming
- **CPU Niceness:** Uses `nice` so you can still run other stuff
- **User Activity Detection:** Backs off when you're actually browsing
- **Resource Limits:** Because "unlimited power" caused problems

---

### Bug Fixes (v2.0)

- Fixed issue where smart fridge user agent was too realistic
- Resolved race condition in coconut spawning
- Addressed feedback that prime number theater was "too dramatic"
- Fixed typo in hacker phrase ("hacking the Gibson" not "hacking the Gibbons")

---

### Legal Disclaimer

This software is provided "as is" with no warranty that it will:
- Make you invisible to the NSA
- Get you a date
- Fix your relationship with your parents
- Make your code compile on the first try

Use responsibly. Don't do crimes. Touch grass occasionally.

---

<p align="center">
  <b>🥥 COCONUTS BY PALM-TREE 🌴</b><br>
  <i>"Making data brokers cry since 2024"</i>
</p>

---

*P.S. - If you actually read all of this, you're either very thorough or very bored. Either way, respect.*

*P.P.S. - The WiFi issue simulator was tested by actually breaking our WiFi. For science.*
