"""
Coconuts Modes - Different flavors of chaos.

Each mode represents a different way to generate traffic noise.
Pick your poison:

- Sleepy: For the night owls who want to appear awake
- Quadcore: For the power users who want ALL the terminals
- Coconut: For the headless browser enthusiasts

"Why have one mode when you can have CHAOS?"
    - Ancient proverb, probably
"""

from .sleepy import SleepyMode, BehaviorModel
from .quadcore import QuadcoreMode
from .coconut import CoconutMode

__all__ = ['SleepyMode', 'BehaviorModel', 'QuadcoreMode', 'CoconutMode']
