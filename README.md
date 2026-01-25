# upgraded-palm-tree
Random network traffic packet generator

## Overview

A Python-based tool for generating random network packets with support for TCP, UDP, and ICMP protocols. Useful for testing, simulation, and educational purposes.

## Features

- Generate random TCP, UDP, and ICMP packets
- Customizable packet parameters (IPs, ports, payload size)
- Reproducible generation with seed support
- JSON and human-readable output formats
- Command-line interface for easy use

## Installation

No external dependencies required. Just clone and run:

```bash
git clone https://github.com/thumpersecure/upgraded-palm-tree.git
cd upgraded-palm-tree
```

## Usage

### Command Line Interface

Generate a single random packet:
```bash
python3 cli.py
```

Generate 10 TCP packets:
```bash
python3 cli.py --count 10 --protocol TCP
```

Generate 5 UDP packets with custom parameters:
```bash
python3 cli.py -c 5 -p UDP --dst-port 53 --payload-size 512
```

Generate packets with JSON output:
```bash
python3 cli.py --count 3 --json
```

Generate reproducible packets with a seed:
```bash
python3 cli.py --count 5 --seed 42
```

### Python API

```python
from random_packet import RandomPacket

# Create generator
generator = RandomPacket()

# Generate a single TCP packet
tcp_packet = generator.generate_tcp_packet()

# Generate a UDP packet with specific parameters
udp_packet = generator.generate_udp_packet(
    src_ip='192.168.1.1',
    dst_ip='10.0.0.1',
    src_port=8080,
    dst_port=443
)

# Generate multiple random packets
packets = generator.generate_packets(count=10, protocol='TCP')

# Generate with reproducible seed
seeded_gen = RandomPacket(seed=42)
packet = seeded_gen.generate_random_packet()
```

## Running Tests

```bash
python3 -m unittest test_random_packet.py
```

## CLI Options

- `-c, --count`: Number of packets to generate (default: 1)
- `-p, --protocol`: Protocol type - TCP, UDP, ICMP, or RANDOM (default: RANDOM)
- `--src-ip`: Source IP address
- `--dst-ip`: Destination IP address
- `--src-port`: Source port (TCP/UDP only)
- `--dst-port`: Destination port (TCP/UDP only)
- `--payload-size`: Payload size in bytes (default: 100)
- `--seed`: Random seed for reproducibility
- `--json`: Output in JSON format
- `--verbose`: Verbose output with detailed information

## License

MIT License - see LICENSE file for details 
