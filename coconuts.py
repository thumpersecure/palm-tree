#!/usr/bin/env python3
"""
🥥 COCONUTS BY PALM-TREE 🌴

The ultimate traffic noise generator with multiple modes of chaos.

"Making data brokers question their life choices since 2024."

Usage:
    python coconuts.py --quadcore      # 4-split terminal chaos
    python coconuts.py --sleepy        # Realistic overnight traffic
    python coconuts.py --coconuts      # Headless browser army
    python coconuts.py --all           # Why not all of them?
"""

import argparse
import asyncio
import sys
import os
import signal
from datetime import datetime
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Banner - because every good CLI needs ASCII art
BANNER = r"""
    🥥 COCONUTS BY PALM-TREE 🌴

   ██████╗ ██████╗  ██████╗ ██████╗ ███╗   ██╗██╗   ██╗████████╗███████╗
  ██╔════╝██╔═══██╗██╔════╝██╔═══██╗████╗  ██║██║   ██║╚══██╔══╝██╔════╝
  ██║     ██║   ██║██║     ██║   ██║██╔██╗ ██║██║   ██║   ██║   ███████╗
  ██║     ██║   ██║██║     ██║   ██║██║╚██╗██║██║   ██║   ██║   ╚════██║
  ╚██████╗╚██████╔╝╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝   ██║   ███████║
   ╚═════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚══════╝

  "If you can't hide, overwhelm with coconuts." — Sun Tzu, probably

  Make advertisers cry. Make data brokers confused. Make trackers despair.
"""

MINI_BANNER = """
🥥 COCONUTS BY PALM-TREE 🌴
"""


def print_banner(mini: bool = False):
    """Print the glorious banner."""
    print(BANNER if not mini else MINI_BANNER)


def print_mode_header(mode: str, description: str):
    """Print a header for the selected mode."""
    print(f"\n{'=' * 60}")
    print(f"  MODE: {mode}")
    print(f"  {description}")
    print(f"{'=' * 60}\n")


async def run_sleepy_mode(args):
    """Run Sleepy Mode - realistic overnight traffic."""
    from modes.sleepy import SleepyMode, SleepSchedule, BehaviorModel

    print_mode_header(
        "SLEEPY MODE 😴",
        "Generating realistic traffic while you sleep..."
    )

    # Create schedule if custom times provided
    schedule = SleepSchedule()

    # Initialize mode
    mode = SleepyMode(
        schedule=schedule,
        use_learning=args.learn,
    )

    # If learning from bash history
    if args.learn and args.learn_from:
        print(f"[Sleepy] Learning patterns from: {args.learn_from}")
        mode.behavior_model.train_from_bash_history(args.learn_from)

    try:
        await mode.run(duration_hours=args.duration / 60 if args.duration else 8)
    except KeyboardInterrupt:
        mode.stop()


async def run_coconut_mode(args):
    """Run Coconut Mode - headless browser army."""
    from modes.coconut import CoconutMode, CoconutConfig, CoconutModeLite, PLAYWRIGHT_AVAILABLE

    print_mode_header(
        "COCONUT MODE 🥥",
        "Spawning headless browsers to visit top sites..."
    )

    # Check if we should use lite mode
    use_lite = args.lite or not PLAYWRIGHT_AVAILABLE

    if use_lite:
        print("[Coconut] Running in Lite mode (HTTP only)")
        mode = CoconutModeLite()
        await mode.run(duration_minutes=args.duration or 60)
    else:
        # Full Playwright mode
        config = CoconutConfig(
            max_concurrent=args.clones or 2,
            headless=not args.show_browser,
            disable_images=not args.load_images,
        )

        # Try to use identity forge
        try:
            from identity.forge import IdentityForge
            identity_forge = IdentityForge()
            print("[Coconut] Using Identity Forge for realistic fingerprints")
        except ImportError:
            identity_forge = None
            print("[Coconut] Identity Forge not available, using defaults")

        mode = CoconutMode(config=config, identity_forge=identity_forge)

        try:
            await mode.run(
                duration_minutes=args.duration or 60,
                visits_per_coconut=10,
            )
        except KeyboardInterrupt:
            await mode.stop()


def run_quadcore_mode(args):
    """Run Quadcore Mode - 4 terminal panes of chaos."""
    from modes.quadcore import QuadcoreMode, prime_theater_standalone

    print_mode_header(
        "QUADCORE MODE 🖥️🖥️🖥️🖥️",
        "Spawning 4 terminal panes of pure chaos..."
    )

    if args.prime_only:
        print("[Quadcore] Running prime theater only...")
        prime_theater_standalone(nice=not args.no_nice)
    else:
        mode = QuadcoreMode(use_nice=not args.no_nice)
        try:
            mode.launch()
        except KeyboardInterrupt:
            mode.stop()


async def run_traffic_noise(args):
    """Run the original traffic noise generator."""
    print_mode_header(
        "TRAFFIC NOISE 📰",
        "Classic traffic noise generation with headlines..."
    )

    # Import and run the original traffic_noise.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    traffic_noise_path = os.path.join(script_dir, "traffic_noise.py")

    if os.path.exists(traffic_noise_path):
        cmd = [sys.executable, traffic_noise_path]
        if args.chaos:
            cmd.append("-c")
        if args.workers:
            cmd.extend(["-w", str(args.workers)])
        if args.duration:
            cmd.extend(["-d", str(args.duration)])

        import subprocess
        subprocess.run(cmd)
    else:
        print("[Error] traffic_noise.py not found!")


async def run_all_modes(args):
    """Run all modes simultaneously. Maximum chaos."""
    print_mode_header(
        "ALL THE COCONUTS 🥥🥥🥥",
        "Running ALL modes at once. Your ISP will be confused."
    )

    print("[WARNING] This is maximum chaos mode.")
    print("[WARNING] Your network will be very busy.")
    print("[WARNING] Press Ctrl+C at any time to stop.\n")

    # We can't truly run all modes at once since some are blocking
    # Instead, we'll run the async ones together
    tasks = []

    # Sleepy mode in background
    from modes.sleepy import SleepyMode
    sleepy = SleepyMode(use_learning=False)
    tasks.append(asyncio.create_task(
        sleepy.run(duration_hours=args.duration / 60 if args.duration else 1)
    ))

    # Coconut mode
    from modes.coconut import CoconutModeLite
    coconut = CoconutModeLite()
    tasks.append(asyncio.create_task(
        coconut.run(duration_minutes=args.duration or 60)
    ))

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        for task in tasks:
            task.cancel()


async def run_personality_mode(args):
    """Run as a specific personality type."""
    from modes.personalities import PersonalityMode, PERSONALITIES

    if args.personality not in PERSONALITIES:
        print(f"[Error] Unknown personality: {args.personality}")
        print(f"[Error] Available: {', '.join(PERSONALITIES.keys())}")
        print("[Hint] Use --list-personalities to see all options")
        return

    mode = PersonalityMode(args.personality)
    await mode.run(duration_minutes=args.duration or 60)


async def run_yolo_mode(args):
    """
    YOLO Mode - Maximum chaos, no regrets (maybe some regrets).

    "What's bandwidth limiting? Never heard of it."
    """
    print_mode_header(
        "🔥 YOLO MODE 🔥",
        "NO LIMITS. MAXIMUM CHAOS. YOUR ROUTER WILL REMEMBER THIS."
    )

    print("""
    ⚠️  WARNING: YOLO MODE ACTIVATED ⚠️

    This mode:
    - Ignores all bandwidth limits (sorry, Netflix)
    - Runs maximum parallel workers
    - Enables chaos mode on everything
    - May anger your ISP
    - Definitely angers data brokers
    - Might summon a daemon (the Unix kind, probably)

    Press Ctrl+C when you've had enough.
    Or don't. I'm not your mom.
    """)

    await asyncio.sleep(3)  # Dramatic pause

    # Run everything with no limits
    from modes.sleepy import SleepyMode
    from modes.coconut import CoconutModeLite
    from modes.personalities import PersonalityMode
    import random

    tasks = []

    # Sleepy mode
    sleepy = SleepyMode(use_learning=False)
    tasks.append(asyncio.create_task(
        sleepy.run(duration_hours=args.duration / 60 if args.duration else 24)
    ))

    # Coconut mode
    coconut = CoconutModeLite()
    tasks.append(asyncio.create_task(
        coconut.run(duration_minutes=args.duration or 1440)  # 24 hours default
    ))

    # Random personality
    personalities = ["paranoid", "drunk", "crypto_bro", "doomscroller", "3am_you"]
    personality = PersonalityMode(random.choice(personalities))
    tasks.append(asyncio.create_task(
        personality.run(duration_minutes=args.duration or 1440)
    ))

    print("[YOLO] All systems go. Godspeed, you magnificent chaos machine.\n")

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        for task in tasks:
            task.cancel()


def run_incognito_theater(args):
    """
    Incognito Theater - Makes it LOOK like you're in incognito mode.

    Spoiler: This is security theater. Like TSA but for browsers.
    """
    print_mode_header(
        "🕵️ INCOGNITO THEATER 🕵️",
        "Making it LOOK like incognito mode (it's not, but shhh)"
    )

    print("""
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │   🕵️  You've gone incognito*                               │
    │                                                             │
    │   Now you can browse privately, and other people who        │
    │   use this device won't see your activity.**                │
    │                                                             │
    │   * Not really                                              │
    │   ** Your ISP, employer, and that guy named Kevin at        │
    │      the NSA can still see everything                       │
    │                                                             │
    │   This won't affect:                                        │
    │   ✗ Your ISP's ability to judge your 3am searches          │
    │   ✗ Your employer's network monitoring                      │
    │   ✗ Kevin (he's seen things)                               │
    │   ✗ The crushing weight of digital surveillance             │
    │                                                             │
    │   What this DOES do:                                        │
    │   ✓ Makes you FEEL like a spy                              │
    │   ✓ Displays this cool ASCII art                           │
    │   ✓ Runs traffic noise in the background                   │
    │   ✓ Absolutely nothing else security-related               │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

    Press Ctrl+C to exit incognito theater and face reality.
    """)

    # Actually run traffic noise
    import subprocess
    script_dir = os.path.dirname(os.path.abspath(__file__))
    traffic_noise_path = os.path.join(script_dir, "traffic_noise.py")

    if os.path.exists(traffic_noise_path):
        cmd = [sys.executable, traffic_noise_path, "-c", "-w", "3"]
        if args.duration:
            cmd.extend(["-d", str(args.duration)])
        subprocess.run(cmd)
    else:
        print("[Incognito Theater] traffic_noise.py not found. The theater is empty.")


def test_identity_forge():
    """Test the Identity Forge."""
    print_mode_header(
        "IDENTITY FORGE TEST 🎭",
        "Minting fake humans..."
    )

    try:
        from identity.forge import IdentityForge
        forge = IdentityForge()

        print("Minting 3 random identities:\n")
        for i in range(3):
            human = forge.mint_identity()
            print(f"Identity #{i+1}:")
            print(f"  Name: {human.name}")
            print(f"  Email: {human.email}")
            print(f"  Location: {human.city}, {human.country_code}")
            print(f"  Job: {human.job_title}")
            print(f"  Platform: {human.platform}")
            print(f"  User-Agent: {human.user_agent[:50]}...")
            print()

        print("\nMinting an exotic identity:")
        exotic = forge.mint_identity(platform="Exotic")
        print(f"  Name: {exotic.name}")
        print(f"  Device: {exotic.platform}")
        print(f"  User-Agent: {exotic.user_agent}")

    except Exception as e:
        print(f"[Error] {e}")


def main():
    parser = argparse.ArgumentParser(
        description="🥥 COCONUTS BY PALM-TREE 🌴 - Advanced Traffic Noise Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --sleepy                    # Run sleepy mode for 8 hours
  %(prog)s --sleepy --learn            # Sleepy mode with behavior learning
  %(prog)s --coconuts --clones 3       # 3 headless browsers
  %(prog)s --quadcore                  # 4-split terminal chaos
  %(prog)s --traffic -c -w 5           # Classic chaos mode with 5 workers
  %(prog)s --all                       # MAXIMUM CHAOS

"Never gonna give you up, never gonna let trackers find you."
        """
    )

    # Mode selection
    mode_group = parser.add_argument_group('Modes')
    mode_group.add_argument('--sleepy', action='store_true',
                           help='Run Sleepy Mode (realistic overnight traffic)')
    mode_group.add_argument('--coconuts', action='store_true',
                           help='Run Coconut Mode (headless browser army)')
    mode_group.add_argument('--quadcore', action='store_true',
                           help='Run Quadcore Mode (4-split terminal chaos)')
    mode_group.add_argument('--traffic', action='store_true',
                           help='Run classic traffic noise mode')
    mode_group.add_argument('--all', action='store_true',
                           help='Run all modes at once (MAXIMUM CHAOS)')
    mode_group.add_argument('--test-identity', action='store_true',
                           help='Test the Identity Forge')
    mode_group.add_argument('--personality', type=str, metavar='TYPE',
                           help='Run as a personality (paranoid, drunk, crypto_bro, etc.)')
    mode_group.add_argument('--list-personalities', action='store_true',
                           help='List all available personalities')
    mode_group.add_argument('--yolo', action='store_true',
                           help='YOLO mode - no limits, maximum chaos, pray for your router')
    mode_group.add_argument('--incognito-theater', action='store_true',
                           help='Makes it LOOK like incognito mode (spoiler: it\'s not)')

    # Sleepy mode options
    sleepy_group = parser.add_argument_group('Sleepy Mode Options')
    sleepy_group.add_argument('--learn', action='store_true',
                             help='Enable behavior learning (Markov chains)')
    sleepy_group.add_argument('--learn-from', type=str, default='~/.bash_history',
                             help='Path to learn browsing patterns from')

    # Coconut mode options
    coconut_group = parser.add_argument_group('Coconut Mode Options')
    coconut_group.add_argument('--clones', type=int, default=2,
                              help='Number of concurrent headless browsers')
    coconut_group.add_argument('--lite', action='store_true',
                              help='Use lite mode (HTTP only, no browser)')
    coconut_group.add_argument('--show-browser', action='store_true',
                              help='Show browser windows (not headless)')
    coconut_group.add_argument('--load-images', action='store_true',
                              help='Load images (uses more bandwidth)')

    # Quadcore mode options
    quad_group = parser.add_argument_group('Quadcore Mode Options')
    quad_group.add_argument('--prime-only', action='store_true',
                           help='Only run prime number theater')
    quad_group.add_argument('--no-nice', action='store_true',
                           help="Don't use nice for CPU priority")

    # Traffic noise options
    traffic_group = parser.add_argument_group('Traffic Noise Options')
    traffic_group.add_argument('-c', '--chaos', action='store_true',
                              help='Enable chaos mode')
    traffic_group.add_argument('-w', '--workers', type=int, default=3,
                              help='Number of parallel workers')

    # Global options
    global_group = parser.add_argument_group('Global Options')
    global_group.add_argument('-d', '--duration', type=int, default=0,
                             help='Duration in minutes (0 = continuous)')
    global_group.add_argument('--bandwidth-limit', type=int, default=500,
                             help='Bandwidth limit in KB/s')
    global_group.add_argument('-q', '--quiet', action='store_true',
                             help='Minimal output')
    global_group.add_argument('--yield-to-user', action='store_true',
                             help='Pause when user is actively browsing')
    global_group.add_argument('--no-banner', action='store_true',
                             help='Skip the banner')

    args = parser.parse_args()

    # Print banner
    if not args.quiet and not args.no_banner:
        print_banner()

    # Handle list-personalities separately
    if args.list_personalities:
        from modes.personalities import list_personalities
        list_personalities()
        return

    # Default to traffic mode if nothing selected
    if not any([args.sleepy, args.coconuts, args.quadcore, args.traffic,
                args.all, args.test_identity, args.personality, args.yolo,
                args.incognito_theater]):
        parser.print_help()
        print("\n[Hint] Try: python coconuts.py --sleepy")
        print("[Hint] Or:  python coconuts.py --coconuts")
        print("[Hint] Or:  python coconuts.py --personality drunk")
        print("[Hint] Or:  python coconuts.py --list-personalities")
        return

    # Handle keyboard interrupt gracefully
    def signal_handler(sig, frame):
        print("\n\n🥥 Coconuts falling gracefully...")
        print("Thanks for using COCONUTS BY PALM-TREE!")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Run selected mode
    try:
        if args.test_identity:
            test_identity_forge()
        elif args.list_personalities:
            pass  # Already handled above
        elif args.personality:
            asyncio.run(run_personality_mode(args))
        elif args.yolo:
            asyncio.run(run_yolo_mode(args))
        elif args.incognito_theater:
            run_incognito_theater(args)
        elif args.quadcore:
            run_quadcore_mode(args)
        elif args.sleepy:
            asyncio.run(run_sleepy_mode(args))
        elif args.coconuts:
            asyncio.run(run_coconut_mode(args))
        elif args.traffic:
            asyncio.run(run_traffic_noise(args))
        elif args.all:
            asyncio.run(run_all_modes(args))

    except KeyboardInterrupt:
        print("\n\n🥥 Coconuts stopped falling.")
    except Exception as e:
        print(f"\n[Error] {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()

    print("\nThanks for using COCONUTS BY PALM-TREE! 🥥🌴")


if __name__ == "__main__":
    main()
