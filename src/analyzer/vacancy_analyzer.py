"""
Vacancy Analysis Module

This module handles the analysis of job vacancy descriptions,
extracting key requirements, tasks, and KPIs that need to be addressed.
"""

from typing import Dict, List, Optional
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VacancyAnalyzer:
    """
    Analyzer for job vacancies that extracts key information and requirements.
    
    This class processes vacancy descriptions to identify:
    - Main responsibilities
    - Key technical requirements
    - KPIs and success metrics
    - Team structure and reporting lines
    """
    
    def __init__(self):
        """Initialize the vacancy analyzer."""
        self.key_responsibility_keywords = [
            'responsible', 'develop', 'design', 'implement', 'maintain',
            'improve', 'optimize', 'manage', 'lead', 'coordinate'
        ]
        
        self.kpi_keywords = [
            'kpi', 'metric', 'target', 'goal', 'objective', 'deadline',
            'performance', 'efficiency', 'quality', 'delivery'
        ]
    
    def analyze_vacancy(self, vacancy: Dict) -> Dict:
        """
        Analyze a single vacancy and extract key information.
        
        Args:
            vacancy (Dict): Vacancy information with title, description, etc.
            
        Returns:
            Dict: Analysis results including key responsibilities, requirements, and KPIs
        """
        try:
            analysis = {
                'vacancy_title': vacancy.get('title'),
                'company': vacancy.get('company'),
                'key_responsibilities': self._extract_responsibilities(vacancy),
                'technical_requirements': self._extract_technical_requirements(vacancy),
                'kpis': self._extract_kpis(vacancy),
                'team_context': self._extract_team_context(vacancy),
                'seniority_level': self._determine_seniority_level(vacancy),
                'analysis_timestamp': None
            }
            
            logger.info(f"Analyzed vacancy: {vacancy.get('title')}")
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing vacancy: {str(e)}")
            return {}
    
    def _extract_responsibilities(self, vacancy: Dict) -> List[str]:
        """
        Extract main responsibilities from vacancy description.
        
        Args:
            vacancy (Dict): Vacancy information
            
        Returns:
            List[str]: List of identified responsibilities
        """
        description = vacancy.get('description', '').lower()
        responsibilities = []
        
        # TODO: Implement NLP-based extraction
        # For now, using simple keyword matching
        lines = description.split('\n')
        for line in lines:
            if any(keyword in line for keyword in self.key_responsibility_keywords):
                responsibilities.append(line.strip())
        
        return responsibilities[:5]  # Return top 5 responsibilities
    
    def _extract_technical_requirements(self, vacancy: Dict) -> List[str]:
        """
        Extract technical requirements from vacancy description.
        
        Args:
            vacancy (Dict): Vacancy information
            
        Returns:
            List[str]: List of technical requirements
        """
        description = (vacancy.get('description', '') + ' ' + 
                      vacancy.get('requirements', '')).lower()
        
        # Common tech stack keywords
        tech_keywords = [
            'python', 'javascript', 'java', 'c++', 'golang', 'rust',
            'react', 'vue', 'angular', 'django', 'fastapi', 'flask',
            'postgresql', 'mongodb', 'redis', 'docker', 'kubernetes',
            'aws', 'gcp', 'azure', 'git', 'ci/cd', 'agile'
        ]
        
        found_requirements = [tech for tech in tech_keywords if tech in description]
        
        return found_requirements
    
    def _extract_kpis(self, vacancy: Dict) -> List[str]:
        """
        Extract KPIs and success metrics from vacancy description.
        
        Args:
            vacancy (Dict): Vacancy information
            
        Returns:
            List[str]: List of identified KPIs
        """
        description = vacancy.get('description', '').lower()
        kpis = []
        
        # TODO: Implement NLP-based KPI extraction
        # For now, using simple keyword matching
        lines = description.split('\n')
        for line in lines:
            if any(keyword in line for keyword in self.kpi_keywords):
                kpis.append(line.strip())
        
        return kpis[:5]  # Return top 5 KPIs
    
    def _extract_team_context(self, vacancy: Dict) -> Dict:
        """
        Extract team context and reporting structure.
        
        Args:
            vacancy (Dict): Vacancy information
            
        Returns:
            Dict: Team context information
        """
        description = vacancy.get('description', '').lower()
        
        team_context = {
            'team_size': None,
            'reporting_to': None,
            'direct_reports': None
        }
        
        # TODO: Implement team context extraction
        
        return team_context
    
    def _determine_seniority_level(self, vacancy: Dict) -> str:
        """
        Determine the seniority level of the position.
        
        Args:
            vacancy (Dict): Vacancy information
            
        Returns:
            str: Seniority level (junior, middle, senior, lead, etc.)
        """
        description = (vacancy.get('description', '') + ' ' + 
                      vacancy.get('title', '')).lower()
        
        if any(word in description for word in ['junior', 'entry', 'graduate']):
            return 'junior'
        elif any(word in description for word in ['lead', 'principal', 'architect']):
            return 'lead'
        elif any(word in description for word in ['senior', 'expert']):
            return 'senior'
        else:
            return 'middle'
    
    def generate_solution_proposal(self, analysis: Dict) -> str:
        """
        Generate a solution proposal based on vacancy analysis.
        
        Args:
            analysis (Dict): Analysis results from analyze_vacancy
            
        Returns:
            str: Generated solution proposal
        """
        proposal = f"""
Based on the analysis of the {analysis.get('vacancy_title')} position at {analysis.get('company')}:

Key Responsibilities Identified:
{self._format_list(analysis.get('key_responsibilities', []))}

Technical Stack Required:
{self._format_list(analysis.get('technical_requirements', []))}

Success Metrics (KPIs):
{self._format_list(analysis.get('kpis', []))}

Our Proposed Solution:
We can provide a full-stack team of specialists who can address all identified requirements
and help achieve the defined KPIs. Our approach includes:
1. Rapid onboarding and understanding of your technical needs
2. Implementation of best practices and scalable solutions
3. Continuous optimization to meet and exceed your KPIs

We would like to schedule a technical discussion to better understand your specific challenges
and propose a tailored solution.
"""
        
        return proposal.strip()
    
    @staticmethod
    def _format_list(items: List[str]) -> str:
        """Format a list of items for display."""
        if not items:
            return "- No items identified"
        return '\n'.join([f"- {item}" for item in items])


if __name__ == "__main__":
    # Example usage
    analyzer = VacancyAnalyzer()
    
    sample_vacancy = {
        'title': 'Senior Python Developer',
        'company': 'TechCorp',
        'description': 'We are looking for a senior developer responsible for designing and implementing scalable solutions.',
        'requirements': 'Required: Python, Django, PostgreSQL, Docker'
    }
    
    analysis = analyzer.analyze_vacancy(sample_vacancy)
    print(json.dumps(analysis, indent=2))
    
    proposal = analyzer.generate_solution_proposal(analysis)
    print("\nGenerated Proposal:")
    print(proposal)

