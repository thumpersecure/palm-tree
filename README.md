# Traffic Noise Generator v3.4.0

<div align="center">

```
╔╦╗┬─┐┌─┐┌─┐┌─┐┬┌─┐  ╔╗╔┌─┐┬┌─┐┌─┐
 ║ ├┬┘├─┤├┤ ├┤ ││    ║║║│ │││└─┐├┤
 ╩ ┴└─┴ ┴└  └  ┴└─┘  ╝╚╝└─┘┴└─┘└─┘
```

[![GitHub stars](https://img.shields.io/github/stars/thumpersecure/palm-tree?style=for-the-badge&logo=github)](https://github.com/thumpersecure/palm-tree/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-3.4.0-green.svg?style=for-the-badge)](https://github.com/thumpersecure/palm-tree)

**Make advertisers cry. Make data brokers confused. Make tracking algorithms question their existence.**

[Quick Start](#-quick-start) | [Features](#-features) | [v3.4.0 Upgrades](#-v340-upgrades) | [Issue Simulation](#-issue-simulation-mode) | [Usage](#-usage)

</div>

---

## Why This Exists

> *"If you can't hide, overwhelm."* — Sun Tzu, probably

Advertisers and data brokers build detailed profiles of your browsing habits. This tool fights back by generating **randomized network traffic** that pollutes your profile with noise, making their data worthless.

**The result?** Trackers see a confused mess of someone who browses like 47 different people simultaneously - from a tech enthusiast on Chrome to someone checking news on a Samsung Smart Fridge.

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/thumpersecure/palm-tree.git
cd palm-tree
pip install httpx beautifulsoup4 lxml rich faker

# Interactive setup (recommended for first time)
python traffic_noise.py --interactive

# Or jump straight to chaos
python traffic_noise.py -c -w 5 --stealth --decoys
```

<details>
<summary><b>Need detailed setup help?</b></summary>

```bash
# Show setup instructions with a free joke
python traffic_noise.py --setup
```

**Manual Steps:**
1. Create virtual environment: `python3 -m venv venv`
2. Activate (use **bash**, not zsh!): `source venv/bin/activate`
3. Install deps: `pip install -r requirements.txt`

</details>

---

## v3.4.0 Upgrades

<details open>
<summary><b>What's New in v3.4.0</b></summary>

| Feature | What It Does | Why It's Better |
|---------|--------------|-----------------|
| **Geo-Rotation** | Rotates through 16 countries with matching language/timezone headers | Trackers see you teleporting across the globe |
| **Bandwidth Control** | 5 preset profiles (stealth to aggressive) with adaptive throttling | Won't nuke your Netflix anymore |
| **Proxy Chain Support** | Route through SOCKS5/HTTP proxies with rotation strategies | Even your ISP doesn't know what you're doing |
| **Session Export** | Full JSON analytics with privacy score trends and category breakdown | Measure exactly how confused the trackers are |
| **Daily Routines** | 6 pre-built realistic daily patterns (office worker, student, etc.) | Traffic looks like an actual human's day |

**New Commands:**
```bash
# Browse as if traveling the world
python traffic_noise.py -c --geo-rotate --geo-countries US,GB,DE,JP

# Limit bandwidth so your roommate doesn't kill you
python traffic_noise.py -c --bandwidth moderate

# Route through proxies
python traffic_noise.py -c --proxy socks5://proxy1:1080 --proxy http://proxy2:8080

# Export session analytics
python traffic_noise.py -c --export --export-path ./my_report.json

# Browse like a 9-to-5 office worker
python traffic_noise.py -c --daily-routine office_worker

# All the features at once
python traffic_noise.py -c --geo-rotate --bandwidth moderate --export --daily-routine remote_worker --stealth --decoys
```

**List commands:**
```bash
python traffic_noise.py --list-geo        # Show 16 available geo locations
python traffic_noise.py --list-bandwidth  # Show 5 bandwidth profiles
python traffic_noise.py --list-routines   # Show 6 daily routine profiles
```

</details>

<details>
<summary><b>Previous v3.3.2 Features</b></summary>

| Feature | What It Does | Why It's Better |
|---------|--------------|-----------------|
| **Issue Traffic Generator** | Generate traffic mimicking computer/network/adware troubleshooting | Makes your profile look like you're fighting with technology 24/7 |
| **15 Issue Categories** | DNS, SSL, WiFi, VPN, BSOD, Adware, Cryptominer, Ransomware, and more | Comprehensive coverage of tech support patterns |
| **Frustration Mode** | Search queries get more desperate over time | Realistic human behavior simulation |
| **Issue Chaining** | One issue leads to related issues (WiFi → DNS → Router) | Natural troubleshooting patterns |
| **Spicy-Cat Style** | Inspired by security testing patterns | Educational and privacy-focused |

**New Issue Types:**
- Network: `dns`, `ssl`, `wifi`, `vpn`, `networking`
- System: `bsod`, `system`, `hardware`, `software`
- Malware: `adware`, `ransomware`, `cryptominer`, `malware`
- Combined: `mixed` (random selection)

</details>

<details>
<summary><b>Previous v3.3 Features (Stealth Update)</b></summary>

| Feature | What It Does |
|---------|--------------|
| **Stealth Mode** | Randomizes TLS fingerprints, header ordering, Sec-CH-UA |
| **Scheduled Profiles** | Changes browsing patterns based on time of day |
| **Privacy Score** | Real-time confusion metric (0-100) |
| **Decoy Injection** | Injects fake interests, demographics, locations into cookies |
| **Plugin System** | Load custom sites/personas from `~/.traffic_noise/plugins/` |
| **Interactive Mode** | Guided setup wizard with prompts |

</details>

<details>
<summary><b>Core Features (v2.0+)</b></summary>

- **Markov Chains** - Human-like category transitions
- **Chaos Mathematics** - Logistic map timing for natural delays
- **200+ News Sites** - 50 left, 50 right, tabloids, hobbies, tech
- **30 Social Platforms** - Full coverage
- **Privacy Sites** - EFF, Tor Project, etc.
- **Persona Mode** - 9 different user types
- **10 Headlines** - Live display
- **30 Workers** - Max parallel identities

</details>

---

## Issue Simulation Mode

<details open>
<summary><b>What Is Issue Simulation?</b></summary>

Generate traffic that looks like you're troubleshooting computer problems. Perfect for:
- **Privacy**: Your browsing profile shows constant tech problems
- **Testing**: Simulate realistic troubleshooting behavior
- **Education**: Understand what malware/adware patterns look like

```bash
# Simulate WiFi problems
python traffic_noise.py --simulate-issues wifi -c

# Simulate adware infection troubleshooting
python traffic_noise.py --simulate-issues adware -c -w 5

# Mix all issue types
python traffic_noise.py --simulate-issues mixed -c --stealth
```

</details>

<details>
<summary><b>Available Issue Types</b></summary>

#### Network Issues
| Type | Description | Example Searches |
|------|-------------|------------------|
| `networking` | General connectivity | "internet not working", "connection timeout" |
| `dns` | DNS failures | "dns_probe_finished_nxdomain", "dns server not responding" |
| `ssl` | Certificate errors | "your connection is not private", "ssl handshake failed" |
| `wifi` | Wireless problems | "wifi keeps disconnecting", "no internet" |
| `vpn` | VPN issues | "vpn won't connect", "vpn slow" |

#### System Issues
| Type | Description | Example Searches |
|------|-------------|------------------|
| `hardware` | Device problems | "blue screen", "device not recognized" |
| `system` | Performance | "computer slow", "high cpu usage" |
| `bsod` | Crash errors | "IRQL_NOT_LESS_OR_EQUAL", "CRITICAL_PROCESS_DIED" |
| `software` | App crashes | "dll missing", "application won't start" |

#### Malware/Adware
| Type | Description | Example Searches |
|------|-------------|------------------|
| `malware` | General infections | "trojan removal", "virus scan" |
| `adware` | Ad infections | "popup ads won't stop", "browser hijacked" |
| `ransomware` | Encryption attacks | "files encrypted", "decrypt files" |
| `cryptominer` | Mining malware | "cpu 100% usage", "fan running high" |

#### Combined
| Type | Description |
|------|-------------|
| `mixed` | Random mix of all above |

</details>

<details>
<summary><b>Advanced Issue Traffic Generator</b></summary>

For programmatic access, use the `IssueTrafficGenerator` class directly:

```python
from issue_traffic import IssueTrafficGenerator, IssueType
import asyncio

async def main():
    generator = IssueTrafficGenerator(
        issue_types=[
            IssueType.WIFI_PROBLEMS,
            IssueType.ADWARE_INFECTION,
            IssueType.SLOW_COMPUTER,
        ],
        frustration_mode=True,  # Searches get more desperate
        chaos_factor=0.3,       # 30% chance to chain to related issues
    )

    await generator.run(duration_minutes=30)

asyncio.run(main())
```

**Features:**
- **Frustration Escalation**: Search queries become more desperate over time
- **Issue Chaining**: One problem leads to related problems naturally
- **Realistic Timing**: Delays mimic frustrated user behavior
- **Multiple Search Engines**: Google, Bing, DuckDuckGo, Reddit, YouTube

</details>

---

## Features

<details>
<summary><b>Feature Comparison: Bash vs Python</b></summary>

| Feature | Bash | Python | Notes |
|---------|:----:|:------:|-------|
| User Agents (30+) | ✅ | ✅ | PS5, Smart Fridge, Tesla included |
| DNS Rotation (14) | ✅ | ✅ | Google, Cloudflare, Quad9 |
| News Sites (200+) | ✅ | ✅ | Politically diverse |
| MAC Spoofing | ✅ | ❌ | Requires root |
| Chaos Mode | ✅ | ✅ | Python uses Markov chains |
| Workers (1-30) | ✅ | ✅ | Parallel identities |
| Live UI | ❌ | ✅ | Rich terminal dashboard |
| Issue Simulation | ❌ | ✅ | **NEW v3.3.2** - 15 types |
| Stealth Mode | ❌ | ✅ | v3.3 |
| Scheduled Profiles | ❌ | ✅ | v3.3 |
| Privacy Score | ❌ | ✅ | v3.3 |
| Decoy Injection | ❌ | ✅ | v3.3 |
| Interactive Setup | ❌ | ✅ | v3.3 |
| Plugin System | ❌ | ✅ | v3.3 |
| Geo-Rotation | ❌ | ✅ | **NEW v3.4.0** - 16 countries |
| Bandwidth Control | ❌ | ✅ | **NEW v3.4.0** - 5 profiles |
| Proxy Chain | ❌ | ✅ | **NEW v3.4.0** - SOCKS5/HTTP |
| Session Export | ❌ | ✅ | **NEW v3.4.0** - JSON reports |
| Daily Routines | ❌ | ✅ | **NEW v3.4.0** - 6 routines |

</details>

<details>
<summary><b>Content Categories (200+ Sites)</b></summary>

| Category | Sites | Examples |
|----------|-------|----------|
| General News | 40+ | BBC, Reuters, CNN, AP |
| Left-Leaning | 50 | MSNBC, Vox, HuffPost, Vice |
| Right-Leaning | 50 | Fox, Breitbart, Daily Wire |
| Tabloids | 20 | TMZ, Daily Mail, Page Six |
| Technology | 15 | Verge, Ars, Wired, TechCrunch |
| Social Media | 30 | All major platforms |
| Privacy | 20 | EFF, Tor Project, Schneier |
| Hobbies | 30 | DIY, cooking, photography |
| **Issue Categories** | **17** | **NEW: DNS, SSL, Adware, BSOD, etc.** |

</details>

<details>
<summary><b>User Agents (30+ Included)</b></summary>

**Standard Browsers:**
- Chrome (Windows, Mac, Linux)
- Firefox (Windows, Mac, Linux)
- Safari (Mac, iOS)
- Edge (Windows)
- Mobile browsers (Android, iOS)

**Exotic Devices:**
- PlayStation 5
- Nintendo Switch
- Samsung Smart TV
- Tesla Browser
- Samsung Smart Fridge
- Googlebot / Bingbot / Twitterbot

</details>

---

## Usage

<details open>
<summary><b>Common Commands</b></summary>

```bash
# Interactive setup wizard
python traffic_noise.py --interactive

# Maximum chaos with all features
python traffic_noise.py -c -w 5 --stealth --decoys --include-all --geo-rotate --export

# Geo-rotation: appear to browse from different countries (NEW v3.4.0)
python traffic_noise.py -c --geo-rotate --geo-countries US,GB,DE,JP,AU

# Bandwidth control: don't nuke your connection (NEW v3.4.0)
python traffic_noise.py -c --bandwidth moderate

# Proxy chain: route through proxies (NEW v3.4.0)
python traffic_noise.py -c --proxy socks5://proxy1:1080 --proxy-rotation random

# Daily routine: browse like a real human (NEW v3.4.0)
python traffic_noise.py -c --daily-routine office_worker

# Export session analytics (NEW v3.4.0)
python traffic_noise.py -c --export

# Simulate troubleshooting issues
python traffic_noise.py --simulate-issues mixed -c

# Browse as a specific persona
python traffic_noise.py --persona privacy_advocate -c

# Time-based profiles (different behavior day/night)
python traffic_noise.py -c --scheduled

# VPS mode - point at your home server
python traffic_noise.py -v YOUR_IP:8080 -c -w 5
```

</details>

<details>
<summary><b>All Python Options</b></summary>

| Option | Default | Description |
|--------|---------|-------------|
| `--interactive`, `-I` | - | Guided setup wizard |
| `--setup` | - | Show setup instructions + joke |
| `-c`, `--chaos` | off | Chaos mode with Markov chains |
| `-w NUM` | 3 | Parallel workers (1-30) |
| `-d MINS` | 0 | Duration (0 = continuous) |
| `--stealth` | off | Fingerprint randomization |
| `--decoys` | off | Inject misleading data |
| `--scheduled` | off | Time-based profiles |
| `--simulate-issues TYPE` | - | **15 types** (see below) |
| `--list-issues` | - | **NEW: List all issue types** |
| `--persona TYPE` | - | 9 types available |
| `--include-all` | off | All content categories |
| `--max-headlines` | 10 | Headlines to show |
| `--no-markov` | off | Disable Markov chains |
| `--no-privacy-score` | off | Hide privacy score |
| `--geo-rotate` | off | **v3.4.0**: Rotate browsing location |
| `--geo-countries CODES` | all | **v3.4.0**: Country codes (e.g., US,GB,DE) |
| `--geo-interval SECS` | 300 | **v3.4.0**: Rotation interval in seconds |
| `--bandwidth PROFILE` | - | **v3.4.0**: Bandwidth limit profile |
| `--bandwidth-max-kbps N` | - | **v3.4.0**: Hard KB/s limit |
| `--proxy URL` | - | **v3.4.0**: Proxy URL (repeatable) |
| `--proxy-file PATH` | - | **v3.4.0**: File with proxy URLs |
| `--proxy-rotation STRAT` | round_robin | **v3.4.0**: Rotation strategy |
| `--export` | off | **v3.4.0**: Export session report |
| `--export-path PATH` | auto | **v3.4.0**: Custom export path |
| `--daily-routine NAME` | - | **v3.4.0**: Daily browsing routine |

**Issue Types:**
`networking`, `hardware`, `software`, `malware`, `misconfigured`, `mixed`, `adware`, `ransomware`, `system`, `dns`, `ssl`, `wifi`, `vpn`, `bsod`, `cryptominer`

**Bandwidth Profiles:**
`unlimited`, `conservative`, `moderate`, `aggressive`, `stealth`

**Daily Routines:**
`office_worker`, `student`, `remote_worker`, `night_owl`, `parent`, `retiree`

**Proxy Rotation Strategies:**
`round_robin`, `random`, `least_used`, `fastest`

</details>

<details>
<summary><b>Persona Types</b></summary>

```bash
python traffic_noise.py --list-personas
```

| Persona | Browsing Focus |
|---------|---------------|
| `tech_enthusiast` | Technology, privacy, hobbies |
| `news_junkie` | World news, all political spectrums |
| `privacy_advocate` | Privacy tools, security sites |
| `social_butterfly` | Social media, lifestyle |
| `entertainment_seeker` | Tabloids, celebrities |
| `health_conscious` | Health, wellness, fitness |
| `political_observer` | Political news from all sides |
| `hobbyist` | DIY, crafts, projects |
| `troubleshooter` | Tech support, troubleshooting |

</details>

---

## How It Works

<details>
<summary><b>Architecture Diagram</b></summary>

```
┌─────────────────────────────────────────────────────────────┐
│                    Traffic Noise Generator v3.4.0           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │Worker 1 │  │Worker 2 │  │Worker 3 │  │Worker N │       │
│  │PS5 UA   │  │Chrome   │  │Bot      │  │Fridge   │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│       │            │            │            │             │
│       └────────────┴────────────┴────────────┘             │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │           Markov Chain + Chaos Math          │           │
│  │  (Determines timing, categories, patterns)   │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │       Daily Routine Engine (NEW v3.4.0)      │           │
│  │  (Time-based behavior: work, study, relax)    │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │         Issue Traffic Generator (v3.3.2)     │           │
│  │  (DNS, SSL, WiFi, Adware, BSOD patterns)     │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │      Geo-Rotation + Stealth Mode             │           │
│  │  (16 countries, fingerprints, header order)   │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │     Bandwidth Control (NEW v3.4.0)           │           │
│  │  (Token bucket, adaptive throttling)          │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │     Proxy Chain (NEW v3.4.0)                 │           │
│  │  (SOCKS5/HTTP, rotation, health checks)       │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│              ┌──────────────────────┐                       │
│              │    Internet / VPS    │                        │
│              └──────────┬──────────┘                        │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │     Session Analytics (NEW v3.4.0)           │           │
│  │  (JSON export, privacy trends, metrics)       │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│              ┌──────────────────────┐                        │
│              │    Ad Networks       │                        │
│              │    Trackers          │                        │
│              │    Data Brokers      │                        │
│              │                      │                        │
│              │   "WTF is this?!"    │                        │
│              │   "Is this person    │                        │
│              │    in 16 countries?!"│                        │
│              └──────────────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

</details>

<details>
<summary><b>Chaos Mode & Markov Chains</b></summary>

**Normal browsing:** Predictable patterns make you easy to track

**Chaos Mode:** Uses Markov chains for human-like but chaotic browsing:

```
Category Transitions:
Technology ─(35%)─► Technology
     │
     └─(15%)─► World ─(35%)─► World
                  │
                  └─(20%)─► Trending
```

**Chaos Mathematics (Logistic Map):**
```
x_{n+1} = 3.9 × x_n × (1 - x_n)

Result: Timing that LOOKS random but follows deterministic chaos
- Evades pattern detection
- Appears human-like
- Mathematically beautiful
```

</details>

<details>
<summary><b>Issue Traffic Patterns (v3.3.2)</b></summary>

**Frustration Escalation:**
```
Search 1: "wifi not connecting"
Search 3: "wifi not connecting fix"
Search 5: "why wifi keeps disconnecting"
Search 8: "please help wifi not working"
Search 12: "HELP wifi still broken nothing works"
```

**Issue Chaining:**
```
WiFi Problems → DNS Issues → Router Reset → Factory Reset →
"Should I buy a new router?" → Amazon router shopping
```

**Realistic Timing:**
- High urgency issues (BSOD, Ransomware) = faster, frantic searches
- Low urgency (slow computer) = longer delays, more thorough reading
- Frustration increases = shorter delays over time

</details>

---

## VPS Setup

<details>
<summary><b>Running on a VPS to protect your home traffic</b></summary>

**Scenario:** Run this on a VPS, point it at your home. Your ISP sees you connecting to VPS. VPS generates noise to your home.

```bash
# On your home machine - simple server
python -m http.server 8080

# On your VPS
python traffic_noise.py -v YOUR_HOME_IP:8080 -c -w 5 --stealth
```

**Port forwarding required on your router:**
- External: 8080 → Internal: YOUR_MACHINE:8080

</details>

---

## Plugin System

<details>
<summary><b>Adding Custom Sites/Personas</b></summary>

Create `~/.traffic_noise/plugins/sites.json`:
```json
{
  "MyCustomCategory": [
    "https://example1.com",
    "https://example2.com"
  ]
}
```

Create `~/.traffic_noise/plugins/personas.json`:
```json
{
  "my_persona": ["Technology", "MyCustomCategory", "Privacy"]
}
```

</details>

---

## Contributing

Found a bug? Want to add more exotic user agents? Have a smart toaster you want to impersonate?

```bash
git checkout -b feature/samsung-smart-toaster-user-agent
# Make changes
git push origin feature/samsung-smart-toaster-user-agent
# Open PR
```

---

## Disclaimer

```
┌─────────────────────────────────────────────────────────────┐
│  This tool is for EDUCATIONAL and PRIVACY TESTING purposes. │
│                                                             │
│  ✅ DO: Use on your own networks, test privacy setups       │
│  ❌ DON'T: Attack others, violate ToS, do illegal things    │
│                                                             │
│  Use responsibly. We are not responsible for misuse.        │
└─────────────────────────────────────────────────────────────┘
```

---

## Star History

If this tool saved you from targeted ads about that embarrassing thing you googled once, consider starring!

[![Star History Chart](https://api.star-history.com/svg?repos=thumpersecure/palm-tree&type=Date)](https://star-history.com/#thumpersecure/palm-tree&Date)

---

<div align="center">

**Made with chaos, caffeine, and coconuts**

*"In a world of surveillance, be the noise."*

```
    🥥
   /|\
  / | \
 /🌴|🌴\
/___|___\
    |
Your Traffic
(Untrackable)
```

</div>
