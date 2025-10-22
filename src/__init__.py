"""
Job Application Agent - Main Package

This package provides an automated solution for applying to job vacancies
across multiple platforms and managing recruiter interactions.
"""

__version__ = "0.1.0"
__author__ = "Job Application Agent Team"

from .parsers import DjinniParser, LinkedInParser, LinkedInJobScraper
from .analyzer import VacancyAnalyzer
from .recruiter_interaction import LeadGenerator, MeetingScheduler
from .flowise_integration import FlowiseClient

__all__ = [
    'DjinniParser',
    'LinkedInParser',
    'LinkedInJobScraper',
    'VacancyAnalyzer',
    'LeadGenerator',
    'MeetingScheduler',
    'FlowiseClient'
]

