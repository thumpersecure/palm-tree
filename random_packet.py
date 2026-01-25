#!/usr/bin/env python3
"""
Random Network Packet Generator

This module generates random network packets with various protocols
for testing and simulation purposes.
"""

import random
from typing import Dict, List, Optional


class RandomPacket:
    """Generate random network packets with various protocols."""
    
    # Common protocols
    PROTOCOL_TCP = 'TCP'
    PROTOCOL_UDP = 'UDP'
    PROTOCOL_ICMP = 'ICMP'
    
    # Protocol numbers (IP protocol field)
    IP_PROTO_TCP = 6
    IP_PROTO_UDP = 17
    IP_PROTO_ICMP = 1
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the random packet generator.
        
        Args:
            seed: Optional random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
    
    def generate_random_ip(self) -> str:
        """
        Generate a random IP address.
        
        Note: Excludes certain reserved addresses by using 1-254 range for
        first and last octets to avoid network/broadcast addresses.
        """
        return f"{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    
    def generate_random_port(self) -> int:
        """Generate a random port number (1024-65535)."""
        return random.randint(1024, 65535)
    
    def generate_random_payload(self, min_size: int = 0, max_size: int = 1500) -> bytes:
        """
        Generate random payload data.
        
        Args:
            min_size: Minimum payload size in bytes
            max_size: Maximum payload size in bytes
            
        Returns:
            Random bytes payload
        """
        size = random.randint(min_size, max_size)
        return bytes([random.randint(0, 255) for _ in range(size)])
    
    def generate_tcp_packet(self, src_ip: Optional[str] = None, dst_ip: Optional[str] = None,
                           src_port: Optional[int] = None, dst_port: Optional[int] = None,
                           payload_size: int = 100) -> Dict:
        """
        Generate a random TCP packet.
        
        Args:
            src_ip: Source IP (random if None)
            dst_ip: Destination IP (random if None)
            src_port: Source port (random if None)
            dst_port: Destination port (random if None)
            payload_size: Size of payload data
            
        Returns:
            Dictionary containing packet information
        """
        packet = {
            'protocol': self.PROTOCOL_TCP,
            'src_ip': src_ip or self.generate_random_ip(),
            'dst_ip': dst_ip or self.generate_random_ip(),
            'src_port': src_port or self.generate_random_port(),
            'dst_port': dst_port or self.generate_random_port(),
            'seq_num': random.randint(0, 2**32 - 1),
            'ack_num': random.randint(0, 2**32 - 1),
            'flags': random.choice(['SYN', 'ACK', 'FIN', 'PSH', 'RST', 'SYN-ACK']),
            'window': random.randint(1024, 65535),
            'payload': self.generate_random_payload(0, payload_size)
        }
        return packet
    
    def generate_udp_packet(self, src_ip: Optional[str] = None, dst_ip: Optional[str] = None,
                           src_port: Optional[int] = None, dst_port: Optional[int] = None,
                           payload_size: int = 100) -> Dict:
        """
        Generate a random UDP packet.
        
        Args:
            src_ip: Source IP (random if None)
            dst_ip: Destination IP (random if None)
            src_port: Source port (random if None)
            dst_port: Destination port (random if None)
            payload_size: Size of payload data
            
        Returns:
            Dictionary containing packet information
        """
        packet = {
            'protocol': self.PROTOCOL_UDP,
            'src_ip': src_ip or self.generate_random_ip(),
            'dst_ip': dst_ip or self.generate_random_ip(),
            'src_port': src_port or self.generate_random_port(),
            'dst_port': dst_port or self.generate_random_port(),
            'payload': self.generate_random_payload(0, payload_size)
        }
        return packet
    
    def generate_icmp_packet(self, src_ip: Optional[str] = None, dst_ip: Optional[str] = None,
                            payload_size: int = 64) -> Dict:
        """
        Generate a random ICMP packet.
        
        Args:
            src_ip: Source IP (random if None)
            dst_ip: Destination IP (random if None)
            payload_size: Size of payload data
            
        Returns:
            Dictionary containing packet information
        """
        packet = {
            'protocol': self.PROTOCOL_ICMP,
            'src_ip': src_ip or self.generate_random_ip(),
            'dst_ip': dst_ip or self.generate_random_ip(),
            'type': random.choice([0, 8]),  # 0=Echo Reply, 8=Echo Request
            'code': 0,
            'id': random.randint(0, 65535),
            'seq': random.randint(0, 65535),
            'payload': self.generate_random_payload(0, payload_size)
        }
        return packet
    
    def generate_random_packet(self, protocol: Optional[str] = None, **kwargs) -> Dict:
        """
        Generate a random packet of any supported protocol.
        
        Args:
            protocol: Specific protocol (TCP, UDP, ICMP) or None for random
            **kwargs: Additional parameters to pass to protocol-specific generator
            
        Returns:
            Dictionary containing packet information
        """
        if protocol is None:
            protocol = random.choice([self.PROTOCOL_TCP, self.PROTOCOL_UDP, self.PROTOCOL_ICMP])
        
        if protocol == self.PROTOCOL_TCP:
            return self.generate_tcp_packet(**kwargs)
        elif protocol == self.PROTOCOL_UDP:
            return self.generate_udp_packet(**kwargs)
        elif protocol == self.PROTOCOL_ICMP:
            return self.generate_icmp_packet(**kwargs)
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")
    
    def generate_packets(self, count: int = 1, protocol: Optional[str] = None, **kwargs) -> List[Dict]:
        """
        Generate multiple random packets.
        
        Args:
            count: Number of packets to generate
            protocol: Specific protocol or None for random
            **kwargs: Additional parameters to pass to packet generator
            
        Returns:
            List of packet dictionaries
        """
        return [self.generate_random_packet(protocol, **kwargs) for _ in range(count)]


def format_packet(packet: Dict) -> str:
    """
    Format a packet dictionary as a human-readable string.
    
    Args:
        packet: Packet dictionary
        
    Returns:
        Formatted string representation
    """
    lines = [f"Protocol: {packet['protocol']}"]
    lines.append(f"Source: {packet['src_ip']}")
    lines.append(f"Destination: {packet['dst_ip']}")
    
    if 'src_port' in packet:
        lines.append(f"Source Port: {packet['src_port']}")
    if 'dst_port' in packet:
        lines.append(f"Destination Port: {packet['dst_port']}")
    
    if packet['protocol'] == RandomPacket.PROTOCOL_TCP:
        lines.append(f"Sequence: {packet['seq_num']}")
        lines.append(f"Acknowledgment: {packet['ack_num']}")
        lines.append(f"Flags: {packet['flags']}")
        lines.append(f"Window: {packet['window']}")
    elif packet['protocol'] == RandomPacket.PROTOCOL_ICMP:
        lines.append(f"Type: {packet['type']}")
        lines.append(f"Code: {packet['code']}")
        lines.append(f"ID: {packet['id']}")
        lines.append(f"Sequence: {packet['seq']}")
    
    lines.append(f"Payload Size: {len(packet['payload'])} bytes")
    return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    generator = RandomPacket()
    
    print("=== Random TCP Packet ===")
    tcp_packet = generator.generate_tcp_packet()
    print(format_packet(tcp_packet))
    print()
    
    print("=== Random UDP Packet ===")
    udp_packet = generator.generate_udp_packet()
    print(format_packet(udp_packet))
    print()
    
    print("=== Random ICMP Packet ===")
    icmp_packet = generator.generate_icmp_packet()
    print(format_packet(icmp_packet))
    print()
    
    print("=== 5 Random Mixed Packets ===")
    packets = generator.generate_packets(5)
    for i, packet in enumerate(packets, 1):
        print(f"\nPacket {i}:")
        print(format_packet(packet))
