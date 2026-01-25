#!/usr/bin/env python3
"""
Command-line interface for the Random Packet Generator.
"""

import argparse
import json
import sys
from random_packet import RandomPacket, format_packet


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate random network packets for testing and simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --count 10 --protocol TCP
  %(prog)s -c 5 -p UDP --json
  %(prog)s --count 3 --seed 42
        """
    )
    
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=1,
        help='Number of packets to generate (default: 1)'
    )
    
    parser.add_argument(
        '-p', '--protocol',
        choices=['TCP', 'UDP', 'ICMP', 'RANDOM'],
        default='RANDOM',
        help='Protocol type (default: RANDOM)'
    )
    
    parser.add_argument(
        '--src-ip',
        help='Source IP address (random if not specified)'
    )
    
    parser.add_argument(
        '--dst-ip',
        help='Destination IP address (random if not specified)'
    )
    
    parser.add_argument(
        '--src-port',
        type=int,
        help='Source port (random if not specified, TCP/UDP only)'
    )
    
    parser.add_argument(
        '--dst-port',
        type=int,
        help='Destination port (random if not specified, TCP/UDP only)'
    )
    
    parser.add_argument(
        '--payload-size',
        type=int,
        default=100,
        help='Payload size in bytes (default: 100)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output with detailed information'
    )
    
    args = parser.parse_args()
    
    # Create generator
    generator = RandomPacket(seed=args.seed)
    
    # Build kwargs for packet generation
    kwargs = {}
    if args.src_ip:
        kwargs['src_ip'] = args.src_ip
    if args.dst_ip:
        kwargs['dst_ip'] = args.dst_ip
    if args.src_port and args.protocol in ['TCP', 'UDP', 'RANDOM']:
        kwargs['src_port'] = args.src_port
    if args.dst_port and args.protocol in ['TCP', 'UDP', 'RANDOM']:
        kwargs['dst_port'] = args.dst_port
    kwargs['payload_size'] = args.payload_size
    
    # Generate packets
    protocol = None if args.protocol == 'RANDOM' else args.protocol
    packets = generator.generate_packets(args.count, protocol, **kwargs)
    
    # Output results
    if args.json:
        # Convert bytes to hex strings for JSON serialization
        json_packets = []
        for packet in packets:
            json_packet = packet.copy()
            json_packet['payload'] = packet['payload'].hex()
            json_packets.append(json_packet)
        print(json.dumps(json_packets, indent=2))
    else:
        for i, packet in enumerate(packets, 1):
            if args.count > 1:
                print(f"\n{'=' * 50}")
                print(f"Packet {i}/{args.count}")
                print('=' * 50)
            print(format_packet(packet))
            
            if args.verbose:
                payload_hex = packet['payload'].hex()
                if len(payload_hex) > 100:
                    print(f"\nPayload (hex): {payload_hex[:100]}...")
                else:
                    print(f"\nPayload (hex): {payload_hex}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
