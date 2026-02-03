# Traffic Noise Generator v3.3

<div align="center">

```
╔╦╗┬─┐┌─┐┌─┐┌─┐┬┌─┐  ╔╗╔┌─┐┬┌─┐┌─┐
 ║ ├┬┘├─┤├┤ ├┤ ││    ║║║│ │││└─┐├┤
 ╩ ┴└─┴ ┴└  └  ┴└─┘  ╝╚╝└─┘┴└─┘└─┘
```

[![GitHub stars](https://img.shields.io/github/stars/thumpersecure/palm-tree?style=for-the-badge&logo=github)](https://github.com/thumpersecure/palm-tree/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-3.3-green.svg?style=for-the-badge)](https://github.com/thumpersecure/palm-tree)

**Make advertisers cry. Make data brokers confused. Make tracking algorithms question their existence.**

[Quick Start](#-quick-start) | [Features](#-features) | [v3.3 Upgrades](#-v33-upgrades) | [Usage](#-usage) | [VPS Setup](#-vps-setup)

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
pip install httpx beautifulsoup4 lxml rich

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

## v3.3 Upgrades

This version brings **major improvements** to make your traffic noise more effective and harder to detect:

<details open>
<summary><b>What's New in v3.3</b></summary>

| Feature | What It Does | Why It's Better |
|---------|--------------|-----------------|
| **Stealth Mode** | Randomizes TLS fingerprints, header ordering, Sec-CH-UA | Evades advanced fingerprinting (JA3/JA4) that sees through basic user-agent switching |
| **Scheduled Profiles** | Changes browsing patterns based on time of day | Mimics realistic human behavior - tech sites during work, entertainment at night |
| **Privacy Score** | Real-time confusion metric (0-100) | Know exactly how much chaos you're generating |
| **Decoy Injection** | Injects fake interests, demographics, locations into cookies | Actively poisons tracking profiles with misleading data |
| **Plugin System** | Load custom sites/personas from `~/.traffic_noise/plugins/` | Extend without modifying core code |
| **Interactive Mode** | Guided setup wizard with prompts | No need to memorize CLI flags |
| **Issue Simulation** | Generate traffic that looks like troubleshooting | Masks your real browsing as "my wifi is broken" searches |

</details>

<details>
<summary><b>Previous Features (Still Available)</b></summary>

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
| Stealth Mode | ❌ | ✅ | **NEW v3.3** |
| Scheduled Profiles | ❌ | ✅ | **NEW v3.3** |
| Privacy Score | ❌ | ✅ | **NEW v3.3** |
| Decoy Injection | ❌ | ✅ | **NEW v3.3** |
| Interactive Setup | ❌ | ✅ | **NEW v3.3** |
| Plugin System | ❌ | ✅ | **NEW v3.3** |

</details>

<details>
<summary><b>Content Categories</b></summary>

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

</details>

---

## Usage

<details open>
<summary><b>Common Commands</b></summary>

```bash
# Interactive setup wizard
python traffic_noise.py --interactive

# Maximum chaos with all v3.3 features
python traffic_noise.py -c -w 5 --stealth --decoys --include-all

# Simulate someone troubleshooting computer issues
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
| `--simulate-issues TYPE` | - | networking/hardware/software/malware/mixed |
| `--persona TYPE` | - | 9 types available |
| `--include-all` | off | All content categories |
| `--max-headlines` | 10 | Headlines to show |
| `--no-markov` | off | Disable Markov chains |
| `--no-privacy-score` | off | Hide privacy score |

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

### Markov Chains & Chaos Mathematics

The Python version now uses **Markov chains** for human-like browsing patterns:

```
Category Transitions (simplified):
┌──────────┐  30%   ┌──────────┐
│ Lifestyle ├──────►│ Lifestyle │
└────┬─────┘       └──────────┘
     │ 15%
     ▼
┌──────────┐  35%   ┌──────────┐
│   World   ├──────►│   World   │
└────┬─────┘       └──────────┘
     │ 15%
     ▼
┌──────────┐
│Technology │  ... and so on
└──────────┘
```

**Chaos Mathematics** uses the **Logistic Map** for timing:
```
x_{n+1} = r × x_n × (1 - x_n)

Where r = 3.9 produces deterministic chaos:
- Looks random to observers
- Actually follows mathematical rules
- Creates natural-looking delays
```

---

## 🎭 Persona Mode

Browse like a specific type of person:

```bash
# Browse like a tech enthusiast
python traffic_noise.py --persona tech_enthusiast -c

# List all available personas
python traffic_noise.py --list-personas
```

| Persona | What They Browse |
|---------|-----------------|
| `tech_enthusiast` | Technology, privacy, and hobby sites |
| `news_junkie` | World news and trending topics across political spectrum |
| `privacy_advocate` | Privacy tools and security resources |
| `social_butterfly` | Social media, lifestyle, and trending content |
| `entertainment_seeker` | Tabloids, social media, and entertainment |
| `health_conscious` | Health, wellness, lifestyle, and hobbies |
| `political_observer` | Political news from multiple perspectives |
| `hobbyist` | DIY, crafts, cooking, and technology projects |
| `troubleshooter` | Technical support searches and problem-solving |

---

## 🔧 Issue Simulation Mode

Generate traffic that looks like you're troubleshooting technical problems:

```bash
# Simulate networking issues
python traffic_noise.py --simulate-issues networking -c

# Simulate hardware problems
python traffic_noise.py --simulate-issues hardware -c

# Simulate malware concerns
python traffic_noise.py --simulate-issues malware -c

# Mix all issue types
python traffic_noise.py --simulate-issues mixed -c
```

| Issue Type | Example Searches |
|------------|-----------------|
| `networking` | "wifi not connecting", "dns server not responding" |
| `hardware` | "computer won't turn on", "blue screen of death fix" |
| `software` | "windows update stuck", "application won't open" |
| `malware` | "remove malware", "browser hijacked fix" |
| `misconfigured` | "proxy settings wrong", "firewall blocking" |
| `mixed` | All of the above randomly |

---

## How It Works

<details>
<summary><b>Architecture Diagram</b></summary>

```
┌─────────────────────────────────────────────────────────────┐
│                    Traffic Noise Generator                   │
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
│  │              Stealth Mode                    │           │
│  │  (Randomizes fingerprints, header order)     │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│  ┌──────────────────────┴──────────────────────┐           │
│  │              Decoy Injector                  │           │
│  │  (Adds fake interests, demographics)         │           │
│  └──────────────────────┬──────────────────────┘           │
│                         │                                   │
│                         ▼                                   │
│                   ┌──────────┐                              │
│                   │ Internet │                              │
│                   └──────────┘                              │
│                         │                                   │
│              ┌──────────┴──────────┐                        │
│              │    Ad Networks       │                        │
│              │    Trackers          │                        │
│              │    Data Brokers      │                        │
│              │                      │                        │
│              │   "WTF is this?!"    │                        │
│              │   "Is this 47       │                        │
│              │    different people?"│                        │
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
