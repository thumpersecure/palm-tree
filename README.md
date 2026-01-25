# Traffic Noise Generator

Network traffic obfuscation tool for privacy testing. Generates randomized network traffic to obscure browsing patterns from advertisers and data collectors.

**Two versions available:**
- `traffic-noise.sh` - Bash script for Kali Linux
- `traffic_noise.py` - Python version with **live terminal UI** showing headlines

## Features

- **30+ User Agents** - Browsers, bots, exotic devices (PlayStation, Smart TV, etc.)
- **14 DNS Servers** - Google, Cloudflare, Quad9, OpenDNS, AdGuard, etc.
- **50+ News Sites** - Lifestyle, World, Technology, Health, Trending categories
- **MAC Address Spoofing** - Automatic rotation with macchanger (Bash version)
- **Chaos Mode** - Simulate multiple bots/users simultaneously
- **Parallel Workers** - Up to 10 independent browsing identities
- **Varied Fingerprints** - Different headers, cookies, timing patterns per request
- **Local UDP Noise** - Additional traffic obfuscation
- **Live Headlines UI** - Python version shows 2-3 live headlines in terminal
- **VPS Mode** - Point to your own server for custom endpoints

---

## Python Version (Recommended for VPS)

The Python version features a beautiful live terminal UI with real-time headline display.

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install directly
pip install httpx beautifulsoup4 lxml rich
```

### Usage

```bash
# Basic usage with live headlines
python traffic_noise.py

# Chaos mode with 5 workers
python traffic_noise.py -c -w 5

# Connect to your home server
python traffic_noise.py -v YOUR_HOME_IP:8080

# Maximum obfuscation for 60 minutes
python traffic_noise.py -c -w 10 -d 60

# Show more headlines (up to 5)
python traffic_noise.py --max-headlines 5
```

### Python Options

| Option | Description |
|--------|-------------|
| `-n, --news-only` | Browse random news sites (default) |
| `-v, --vps IP:PORT` | Connect to specific endpoint (your home server) |
| `-H, --headlines` | Show live headlines (default: on) |
| `--no-headlines` | Disable headline display |
| `-c, --chaos` | Chaos mode - multi-bot simulation |
| `-w, --workers NUM` | Parallel workers (default: 3, max: 10) |
| `-d, --duration MINS` | Run duration in minutes |
| `--max-headlines NUM` | Headlines to show (default: 3) |
| `-q, --quiet` | Minimal output |

### Terminal UI Preview

```
┌──────────────────────────────────────────────────────────────────┐
│ 🌐 Traffic Noise Generator | Mode: CHAOS MODE | Workers: 5       │
└──────────────────────────────────────────────────────────────────┘
┌─ 📰 Live Headlines ──────────────────────────────────────────────┐
│ Time     Category    Headline                          Source    │
│ 14:32:01 Technology  Apple announces new AI features   theverge  │
│ 14:32:15 World       UN Security Council meets today   bbc.com   │
│ 14:32:28 Health      New study on sleep patterns       webmd.com │
└──────────────────────────────────────────────────────────────────┘
┌─ 📊 Statistics ──────────────────────────────────────────────────┐
│ Requests: 127          Errors: 2                                 │
│ Last Category: World   Active Workers: 5                         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Bash Version (Kali Linux)

### Installation

```bash
# Make executable
chmod +x traffic-noise.sh

# Install dependencies (Kali Linux)
sudo apt install curl netcat macchanger
```

### Usage

```bash
# Basic usage - browse news sites
./traffic-noise.sh -n -h

# RECOMMENDED: Chaos mode with multiple workers
sudo ./traffic-noise.sh -c -r -w 5 -h

# Maximum obfuscation
sudo ./traffic-noise.sh -c -r -w 10 -d 60

# Connect to your VPS
./traffic-noise.sh -v 192.168.1.100:8080

# Background operation
./traffic-noise.sh -n -q -d 60 &
```

### Bash Options

| Option | Description |
|--------|-------------|
| `-n, --news-only` | Browse random news sites (default) |
| `-v, --vps IP:PORT` | Connect to specific VPS endpoint |
| `-h, --headlines` | Display fetched news headlines |
| `-r, --randomize-id` | Full identity randomization (MAC, DNS) |
| `-c, --chaos` | Chaos mode - multi-bot simulation |
| `-w, --workers NUM` | Parallel workers (1-10) |
| `-d, --duration MINS` | Run duration in minutes |
| `-i, --interface IFACE` | Network interface (default: eth0) |
| `-q, --quiet` | Suppress output |

---

## VPS Setup

To use with your home server:

1. **On your home machine**, run a simple web server:
   ```bash
   # Python simple server
   python -m http.server 8080

   # Or netcat listener
   nc -lk 8080
   ```

2. **On your VPS**, run the traffic noise generator:
   ```bash
   # Python version (recommended)
   python traffic_noise.py -v YOUR_HOME_IP:8080 -c -w 5

   # Bash version
   ./traffic-noise.sh -v YOUR_HOME_IP:8080 -c -w 5
   ```

---

## Chaos Mode

The `-c` flag enables chaos mode which makes your traffic appear as multiple different users/bots:

- Erratic timing patterns (1-120 seconds between requests)
- Frequent mid-session identity rotation
- Mixed bot and human user agents
- Varied browser fingerprints per request
- Different browsing patterns (normal, bursty, slow, erratic, scanner)
- Simulates traffic from different OS, devices, and locations

## Browsing Patterns

The tool automatically rotates between these patterns:

| Pattern | Behavior |
|---------|----------|
| `normal` | Regular intervals (5-30s) |
| `bursty` | Quick bursts then long pauses |
| `slow` | Very slow browsing (45-180s) |
| `erratic` | Completely random timing |
| `scanner` | Fast, systematic (bot-like) |

## Requirements

**Python version:**
- Python 3.8+
- httpx, beautifulsoup4, lxml, rich (see requirements.txt)

**Bash version:**
- curl (required)
- netcat (optional, for UDP traffic)
- macchanger (optional, for MAC spoofing)
- root privileges (optional, for MAC/DNS changes)

## Notes

- Press Ctrl+C to stop gracefully
- MAC spoofing may temporarily disconnect network (Bash version)
- Some sites may block automated requests
- Use responsibly and in accordance with applicable laws

## License

MIT License - See LICENSE file
