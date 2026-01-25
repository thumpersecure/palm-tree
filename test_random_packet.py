#!/usr/bin/env python3
"""
Unit tests for the Random Packet Generator.
"""

import unittest
from random_packet import RandomPacket, format_packet


class TestRandomPacket(unittest.TestCase):
    """Test cases for RandomPacket class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = RandomPacket(seed=42)
    
    def test_generate_random_ip(self):
        """Test random IP generation."""
        ip = self.generator.generate_random_ip()
        parts = ip.split('.')
        self.assertEqual(len(parts), 4)
        for part in parts:
            self.assertTrue(0 <= int(part) <= 255)
    
    def test_generate_random_port(self):
        """Test random port generation."""
        port = self.generator.generate_random_port()
        self.assertTrue(1024 <= port <= 65535)
    
    def test_generate_random_payload(self):
        """Test random payload generation."""
        payload = self.generator.generate_random_payload(10, 20)
        self.assertTrue(10 <= len(payload) <= 20)
        self.assertIsInstance(payload, bytes)
    
    def test_generate_tcp_packet(self):
        """Test TCP packet generation."""
        packet = self.generator.generate_tcp_packet()
        self.assertEqual(packet['protocol'], RandomPacket.PROTOCOL_TCP)
        self.assertIn('src_ip', packet)
        self.assertIn('dst_ip', packet)
        self.assertIn('src_port', packet)
        self.assertIn('dst_port', packet)
        self.assertIn('seq_num', packet)
        self.assertIn('ack_num', packet)
        self.assertIn('flags', packet)
        self.assertIn('window', packet)
        self.assertIn('payload', packet)
        
        # Validate port ranges
        self.assertTrue(1024 <= packet['src_port'] <= 65535)
        self.assertTrue(1024 <= packet['dst_port'] <= 65535)
    
    def test_generate_udp_packet(self):
        """Test UDP packet generation."""
        packet = self.generator.generate_udp_packet()
        self.assertEqual(packet['protocol'], RandomPacket.PROTOCOL_UDP)
        self.assertIn('src_ip', packet)
        self.assertIn('dst_ip', packet)
        self.assertIn('src_port', packet)
        self.assertIn('dst_port', packet)
        self.assertIn('payload', packet)
        
        # Validate port ranges
        self.assertTrue(1024 <= packet['src_port'] <= 65535)
        self.assertTrue(1024 <= packet['dst_port'] <= 65535)
    
    def test_generate_icmp_packet(self):
        """Test ICMP packet generation."""
        packet = self.generator.generate_icmp_packet()
        self.assertEqual(packet['protocol'], RandomPacket.PROTOCOL_ICMP)
        self.assertIn('src_ip', packet)
        self.assertIn('dst_ip', packet)
        self.assertIn('type', packet)
        self.assertIn('code', packet)
        self.assertIn('id', packet)
        self.assertIn('seq', packet)
        self.assertIn('payload', packet)
    
    def test_generate_tcp_packet_with_params(self):
        """Test TCP packet generation with specific parameters."""
        packet = self.generator.generate_tcp_packet(
            src_ip='192.168.1.1',
            dst_ip='10.0.0.1',
            src_port=8080,
            dst_port=443
        )
        self.assertEqual(packet['src_ip'], '192.168.1.1')
        self.assertEqual(packet['dst_ip'], '10.0.0.1')
        self.assertEqual(packet['src_port'], 8080)
        self.assertEqual(packet['dst_port'], 443)
    
    def test_generate_random_packet(self):
        """Test random packet generation."""
        packet = self.generator.generate_random_packet()
        self.assertIn(packet['protocol'], [
            RandomPacket.PROTOCOL_TCP,
            RandomPacket.PROTOCOL_UDP,
            RandomPacket.PROTOCOL_ICMP
        ])
    
    def test_generate_random_packet_tcp(self):
        """Test random packet generation with specific protocol."""
        packet = self.generator.generate_random_packet(protocol='TCP')
        self.assertEqual(packet['protocol'], RandomPacket.PROTOCOL_TCP)
    
    def test_generate_packets(self):
        """Test generating multiple packets."""
        packets = self.generator.generate_packets(count=5)
        self.assertEqual(len(packets), 5)
        for packet in packets:
            self.assertIn(packet['protocol'], [
                RandomPacket.PROTOCOL_TCP,
                RandomPacket.PROTOCOL_UDP,
                RandomPacket.PROTOCOL_ICMP
            ])
    
    def test_generate_packets_tcp_only(self):
        """Test generating multiple TCP packets."""
        packets = self.generator.generate_packets(count=3, protocol='TCP')
        self.assertEqual(len(packets), 3)
        for packet in packets:
            self.assertEqual(packet['protocol'], RandomPacket.PROTOCOL_TCP)
    
    def test_format_packet_tcp(self):
        """Test formatting TCP packet."""
        packet = self.generator.generate_tcp_packet()
        formatted = format_packet(packet)
        self.assertIn('Protocol: TCP', formatted)
        self.assertIn('Source:', formatted)
        self.assertIn('Destination:', formatted)
        self.assertIn('Sequence:', formatted)
        self.assertIn('Flags:', formatted)
    
    def test_format_packet_udp(self):
        """Test formatting UDP packet."""
        packet = self.generator.generate_udp_packet()
        formatted = format_packet(packet)
        self.assertIn('Protocol: UDP', formatted)
        self.assertIn('Source Port:', formatted)
        self.assertIn('Destination Port:', formatted)
    
    def test_format_packet_icmp(self):
        """Test formatting ICMP packet."""
        packet = self.generator.generate_icmp_packet()
        formatted = format_packet(packet)
        self.assertIn('Protocol: ICMP', formatted)
        self.assertIn('Type:', formatted)
        self.assertIn('Code:', formatted)
    
    def test_seeded_generation_reproducibility(self):
        """Test that seeded generation is reproducible."""
        # Generate multiple packets with same seed to verify reproducibility
        gen1 = RandomPacket(seed=12345)
        packets1 = gen1.generate_packets(count=3)
        
        gen2 = RandomPacket(seed=12345)
        packets2 = gen2.generate_packets(count=3)
        
        # Check that the same sequence is generated
        for p1, p2 in zip(packets1, packets2):
            self.assertEqual(p1['protocol'], p2['protocol'])
            self.assertEqual(p1['src_ip'], p2['src_ip'])
            self.assertEqual(p1['dst_ip'], p2['dst_ip'])
    
    def test_invalid_protocol(self):
        """Test that invalid protocol raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_random_packet(protocol='INVALID')


if __name__ == '__main__':
    unittest.main()
