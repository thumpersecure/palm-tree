# 🥥 COCONUTS BY PALM-TREE 🌴 - Release Notes

*"If your browsing history doesn't confuse you, it's not private enough."*

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
