"""
Identity Forge - Because one identity is for amateurs.

This module provides tools for generating completely fake but convincingly
realistic human identities. Each request gets a whole person with a backstory
they never asked for.

"Today I am Karen, 47, from Wisconsin. I love scrapbooking and judging others."
    - Your HTTP request, probably
"""

from .forge import IdentityForge, FakeHuman, generate_identity

__all__ = ['IdentityForge', 'FakeHuman', 'generate_identity']
