"""
Parsers package for job vacancy extraction from various platforms.
"""

from .djinni_parser import DjinniParser
from .linkedin_parser import LinkedInParser

__all__ = ['DjinniParser', 'LinkedInParser']

