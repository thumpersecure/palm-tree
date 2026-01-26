#!/usr/bin/env python3
"""
Quadcore Mode - 4 terminals of pure chaos.

"Why have one terminal when you can have FOUR?"
    - Someone with too many monitors

This mode spawns 4 synchronized processes in split terminal panes:
1. Prime number crunching (CPU intimidation theater)
2. Traffic noise with aggressive headlines
3. Random packet simulation display
4. Fake system metrics + "hacker movie" output

Requires tmux or screen for the full experience.
Falls back to background processes if neither is available.
"""

import asyncio
import subprocess
import shutil
import sys
import os
import random
import math
import time
from dataclasses import dataclass
from typing import Optional, List, Callable
from datetime import datetime


@dataclass
class PaneConfig:
    """Configuration for a terminal pane."""
    name: str
    command: str
    description: str


class QuadcoreMode:
    """
    Quadcore Mode - Maximum terminal presence.

    "Make it look like you're hacking the mainframe."

    Spawns 4 panes of activity:
    - Prime Theater: Calculate primes with dramatic output
    - Traffic Noise: The main traffic generator
    - Packet Display: Random packet simulation
    - System Metrics: Fake but impressive stats
    """

    # ASCII art for the prime theater
    PRIME_BANNER = r"""
    ╔═══════════════════════════════════════╗
    ║     PRIME NUMBER DISCOVERY ENGINE     ║
    ║   "Finding primes since just now"     ║
    ╚═══════════════════════════════════════╝
    """

    # Hacker movie style phrases
    HACKER_PHRASES = [
        "Bypassing mainframe encryption...",
        "Downloading more RAM...",
        "Reversing the polarity...",
        "Hacking the Gibson...",
        "Initializing quantum tunneling...",
        "Decrypting the cyber matrix...",
        "Uploading virus to alien mothership...",
        "Reticulating splines...",
        "Activating turbo encabulator...",
        "Calibrating flux capacitor...",
        "Engaging warp drive...",
        "Compiling the kernel...",
        "Defragmenting the blockchain...",
        "Synergizing the paradigm...",
        "Leveraging the cloud...",
        "Pivoting to enterprise...",
        "Disrupting the industry...",
        "Moving fast and breaking things...",
        "Putting it on the blockchain...",
        "Making it webscale...",
    ]

    def __init__(
        self,
        traffic_noise_path: Optional[str] = None,
        use_nice: bool = True,
    ):
        """
        Initialize Quadcore Mode.

        Args:
            traffic_noise_path: Path to traffic_noise.py
            use_nice: Whether to use nice for lower CPU priority
        """
        # Find the script directory
        self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.traffic_noise_path = traffic_noise_path or os.path.join(self.script_dir, "traffic_noise.py")
        self.use_nice = use_nice

        # Check available terminal multiplexers
        self.has_tmux = shutil.which("tmux") is not None
        self.has_screen = shutil.which("screen") is not None

        self.processes: List[subprocess.Popen] = []
        self.running = False

    def _get_pane_configs(self) -> List[PaneConfig]:
        """Get the configuration for all 4 panes."""
        python = sys.executable
        nice_prefix = "nice -n 19 " if self.use_nice else ""

        return [
            PaneConfig(
                name="Prime Theater",
                command=f"{nice_prefix}{python} -c \"{self._get_prime_script()}\"",
                description="Prime number calculation (CPU theater)"
            ),
            PaneConfig(
                name="Traffic Noise",
                command=f"{nice_prefix}{python} {self.traffic_noise_path} -c -w 2 --max-headlines 5",
                description="Traffic noise generator"
            ),
            PaneConfig(
                name="Packet Sim",
                command=f"{nice_prefix}{python} -c \"{self._get_packet_script()}\"",
                description="Random packet simulation display"
            ),
            PaneConfig(
                name="Hacker Mode",
                command=f"{nice_prefix}{python} -c \"{self._get_hacker_script()}\"",
                description="Fake system metrics & hacker movie output"
            ),
        ]

    def _get_prime_script(self) -> str:
        """Return the prime theater script as a string."""
        return '''
import time
import random
import sys

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def sieve_segment(start, end):
    """Find primes in a range using trial division."""
    primes = []
    for n in range(start, end):
        if is_prime(n):
            primes.append(n)
    return primes

print(chr(27) + "[2J")  # Clear screen
print("""
    ╔═══════════════════════════════════════╗
    ║     PRIME NUMBER DISCOVERY ENGINE     ║
    ║   \\"Finding primes since just now\\"    ║
    ╚═══════════════════════════════════════╝
""")

primes_found = 0
current = 2
batch_size = 1000

while True:
    try:
        primes = sieve_segment(current, current + batch_size)
        primes_found += len(primes)
        current += batch_size

        if primes:
            largest = primes[-1]
            print(f"[{time.strftime(\\"%H:%M:%S\\")}] Scanned up to {current:,}")
            print(f"  Found {len(primes)} primes in this batch")
            print(f"  Largest: {largest:,}")
            print(f"  Total primes found: {primes_found:,}")
            print()

        # Slow down to be nice
        time.sleep(random.uniform(1, 3))

    except KeyboardInterrupt:
        print(f"\\nTotal primes discovered: {primes_found:,}")
        break
'''

    def _get_packet_script(self) -> str:
        """Return the packet simulation script."""
        return '''
import time
import random
import sys

protocols = ["TCP", "UDP", "ICMP"]
flags = ["SYN", "ACK", "FIN", "PSH", "RST", "SYN-ACK"]

def random_ip():
    return f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def random_port():
    return random.randint(1024, 65535)

print(chr(27) + "[2J")  # Clear screen
print("""
    ╔═══════════════════════════════════════╗
    ║       PACKET SIMULATION ENGINE        ║
    ║     "Packets go brrrrr (safely)"      ║
    ╚═══════════════════════════════════════╝
""")

packet_count = 0

while True:
    try:
        protocol = random.choice(protocols)
        src_ip = random_ip()
        dst_ip = random_ip()

        print(f"[{time.strftime(\\"%H:%M:%S\\")}] Packet #{packet_count + 1}")
        print(f"  Protocol: {protocol}")
        print(f"  {src_ip} -> {dst_ip}")

        if protocol == "TCP":
            print(f"  Ports: {random_port()} -> {random_port()}")
            print(f"  Flags: {random.choice(flags)}")
            print(f"  Seq: {random.randint(0, 2**32-1)}")
        elif protocol == "UDP":
            print(f"  Ports: {random_port()} -> {random_port()}")
        else:
            print(f"  Type: {'Echo Request' if random.randint(0,1) else 'Echo Reply'}")

        print(f"  Payload: {random.randint(0, 1500)} bytes")
        print()

        packet_count += 1
        time.sleep(random.uniform(0.5, 2))

    except KeyboardInterrupt:
        print(f"\\nTotal packets simulated: {packet_count}")
        break
'''

    def _get_hacker_script(self) -> str:
        """Return the hacker movie script."""
        phrases = self.HACKER_PHRASES
        return f'''
import time
import random
import sys

phrases = {phrases}

def fake_progress():
    """Print a fake progress bar."""
    total = random.randint(20, 50)
    for i in range(total):
        progress = "=" * i + ">" + " " * (total - i - 1)
        percent = int((i / total) * 100)
        print(f"\\r  [{progress}] {percent}%", end="", flush=True)
        time.sleep(random.uniform(0.05, 0.2))
    print(f"\\r  [{'=' * total}] 100%")

def fake_ip():
    return f"{{random.randint(1,254)}}.{{random.randint(0,255)}}.{{random.randint(0,255)}}.{{random.randint(1,254)}}"

def fake_hex():
    return "".join(random.choices("0123456789ABCDEF", k=random.randint(8, 32)))

print(chr(27) + "[2J")  # Clear screen
print("""
    ╔═══════════════════════════════════════╗
    ║        SYSTEM OPERATIONS CENTER       ║
    ║       "We\\'re in the mainframe"       ║
    ╚═══════════════════════════════════════╝
""")

cycle = 0
while True:
    try:
        print(f"[{{time.strftime(\\"%H:%M:%S\\")}}] === Cycle {{cycle + 1}} ===")

        # Random hacker phrase
        phrase = random.choice(phrases)
        print(f"  {{phrase}}")
        fake_progress()

        # Fake system stats
        print(f"  CPU: {{random.randint(10, 95)}}% | RAM: {{random.randint(2000, 8000)}}MB | NET: {{random.randint(100, 5000)}}Kb/s")

        # Fake connection
        print(f"  Connected to {{fake_ip()}}:{{random.randint(1024, 65535)}}")

        # Fake hex data
        print(f"  Data: 0x{{fake_hex()}}")

        # Random "discovery"
        discoveries = [
            f"Found {{random.randint(1, 100)}} open ports",
            f"Detected {{random.randint(1, 50)}} active services",
            "Vulnerability scan complete",
            f"Downloaded {{random.randint(100, 9999)}} packets",
            "Encryption key extracted",
            "Firewall bypassed successfully",
            "Access granted to level {{random.randint(1, 10)}}",
        ]
        print(f"  >> {{random.choice(discoveries)}}")
        print()

        cycle += 1
        time.sleep(random.uniform(2, 5))

    except KeyboardInterrupt:
        print(f"\\nOperations complete. Cycles: {{cycle}}")
        break
'''

    def launch_tmux(self) -> bool:
        """Launch all panes in tmux."""
        session_name = "coconuts"

        try:
            # Kill existing session if it exists
            subprocess.run(["tmux", "kill-session", "-t", session_name], capture_output=True)

            # Create new session with first pane
            configs = self._get_pane_configs()
            subprocess.run([
                "tmux", "new-session", "-d", "-s", session_name,
                "-n", "Coconuts"
            ], check=True)

            # Split into 4 panes (2x2 grid)
            subprocess.run(["tmux", "split-window", "-h", "-t", f"{session_name}:0"], check=True)
            subprocess.run(["tmux", "split-window", "-v", "-t", f"{session_name}:0.0"], check=True)
            subprocess.run(["tmux", "split-window", "-v", "-t", f"{session_name}:0.2"], check=True)

            # Send commands to each pane
            for i, config in enumerate(configs):
                subprocess.run([
                    "tmux", "send-keys", "-t", f"{session_name}:0.{i}",
                    config.command, "Enter"
                ], check=True)

            # Attach to session
            print(f"[Quadcore] Launching tmux session '{session_name}'...")
            subprocess.run(["tmux", "attach-session", "-t", session_name])

            return True

        except Exception as e:
            print(f"[Quadcore] tmux launch failed: {e}")
            return False

    def launch_background(self) -> bool:
        """Launch all panes as background processes (fallback)."""
        configs = self._get_pane_configs()

        print("[Quadcore] No tmux/screen found, launching as background processes...")
        print("[Quadcore] Output will be interleaved in this terminal.\n")

        for config in configs:
            try:
                # Use bash -c to run the command
                proc = subprocess.Popen(
                    ["bash", "-c", config.command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
                self.processes.append(proc)
                print(f"[Quadcore] Started: {config.name} (PID {proc.pid})")
            except Exception as e:
                print(f"[Quadcore] Failed to start {config.name}: {e}")

        return len(self.processes) > 0

    def launch(self) -> bool:
        """
        Launch Quadcore Mode.

        Tries tmux first, then screen, then falls back to background processes.
        """
        self.running = True

        if self.has_tmux:
            return self.launch_tmux()
        elif self.has_screen:
            print("[Quadcore] Screen support coming soon, using background mode...")
            return self.launch_background()
        else:
            return self.launch_background()

    def stop(self) -> None:
        """Stop all processes."""
        self.running = False

        for proc in self.processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

        self.processes.clear()

        # Kill tmux session if it exists
        if self.has_tmux:
            subprocess.run(["tmux", "kill-session", "-t", "coconuts"], capture_output=True)


# Standalone prime calculator for dramatic effect
def prime_theater_standalone(nice: bool = True) -> None:
    """
    Run the prime theater as a standalone function.

    This is the "look busy" mode - calculates primes forever
    with dramatic terminal output.
    """
    print("\n" + "=" * 50)
    print("    PRIME NUMBER DISCOVERY ENGINE")
    print("    Finding primes since... *checks watch* ...now")
    print("=" * 50 + "\n")

    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    primes_found = 0
    current = 2
    batch_size = 1000
    start_time = time.time()

    try:
        while True:
            # Find primes in batch
            batch_primes = [n for n in range(current, current + batch_size) if is_prime(n)]
            primes_found += len(batch_primes)
            current += batch_size

            if batch_primes:
                elapsed = time.time() - start_time
                rate = primes_found / elapsed if elapsed > 0 else 0

                print(f"[{datetime.now().strftime('%H:%M:%S')}] Scanned: {current:,}")
                print(f"  Primes in batch: {len(batch_primes)}")
                print(f"  Largest found: {batch_primes[-1]:,}")
                print(f"  Total primes: {primes_found:,}")
                print(f"  Rate: {rate:.1f} primes/sec")
                print()

            # Be nice to the CPU
            time.sleep(random.uniform(0.5, 1.5))

    except KeyboardInterrupt:
        print(f"\n{'=' * 50}")
        print(f"Prime theater concluded.")
        print(f"Total primes discovered: {primes_found:,}")
        print(f"Largest prime found: {batch_primes[-1] if batch_primes else 'N/A':,}")
        print(f"{'=' * 50}")


# For testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Quadcore Mode - 4 terminals of chaos")
    parser.add_argument("--prime-only", action="store_true", help="Only run prime theater")
    parser.add_argument("--no-nice", action="store_true", help="Don't use nice for CPU priority")
    args = parser.parse_args()

    if args.prime_only:
        prime_theater_standalone(nice=not args.no_nice)
    else:
        mode = QuadcoreMode(use_nice=not args.no_nice)
        try:
            mode.launch()
        except KeyboardInterrupt:
            mode.stop()
            print("\n[Quadcore] Shutdown complete.")
