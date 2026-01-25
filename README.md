# Traffic Noise Generator

Network traffic obfuscation tool for privacy testing. Generates randomized network traffic to obscure browsing patterns from advertisers and data collectors.

## Features

- **30+ User Agents** - Browsers, bots, exotic devices (PlayStation, Smart TV, etc.)
- **14 DNS Servers** - Google, Cloudflare, Quad9, OpenDNS, AdGuard, etc.
- **50+ News Sites** - Lifestyle, World, Technology, Health, Trending categories
- **MAC Address Spoofing** - Automatic rotation with macchanger
- **Chaos Mode** - Simulate multiple bots/users simultaneously
- **Parallel Workers** - Up to 10 independent browsing identities
- **Varied Fingerprints** - Different headers, cookies, timing patterns per request
- **Local UDP Noise** - Additional traffic obfuscation

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/upgraded-palm-tree.git
cd upgraded-palm-tree

# Make executable
chmod +x traffic-noise.sh

# Install dependencies (Kali Linux)
sudo apt install curl netcat macchanger
```

## Usage

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

## Options

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

- **curl** (required)
- **netcat** (optional, for UDP traffic)
- **macchanger** (optional, for MAC spoofing)
- **root privileges** (optional, for MAC/DNS changes)

## Notes

- Press Ctrl+C to stop gracefully
- MAC spoofing may temporarily disconnect network
- Some sites may block automated requests
- Use responsibly and in accordance with applicable laws

## License

MIT License - See LICENSE file
