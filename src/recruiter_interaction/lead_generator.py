"""
Lead Generation and Recruiter Interaction Module

This module handles the generation of leads, sending responses to recruiters,
and notifying the designated contact (Maxim) about potential opportunities.
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeadGenerator:
    """
    Generates leads from job vacancies and manages recruiter interactions.
    
    This class is responsible for:
    - Creating lead records from analyzed vacancies
    - Generating personalized responses for recruiters
    - Tracking lead status and interactions
    - Notifying designated contacts about new leads
    """
    
    def __init__(self, maxim_contact: Optional[Dict] = None):
        """
        Initialize the lead generator.
        
        Args:
            maxim_contact (Dict, optional): Contact information for Maxim
                Should include: email, phone, slack_id, etc.
        """
        self.maxim_contact = maxim_contact or {}
        self.leads = []
    
    def create_lead(self, vacancy: Dict, analysis: Dict, 
                   generated_response: str) -> Dict:
        """
        Create a lead record from a vacancy and analysis.
        
        Args:
            vacancy (Dict): Original vacancy information
            analysis (Dict): Analysis results from VacancyAnalyzer
            generated_response (str): Generated response/proposal for the recruiter
            
        Returns:
            Dict: Lead record with all relevant information
        """
        lead = {
            'lead_id': self._generate_lead_id(),
            'vacancy_title': vacancy.get('title'),
            'company': vacancy.get('company'),
            'recruiter_name': vacancy.get('recruiter_name'),
            'recruiter_email': vacancy.get('recruiter_email'),
            'recruiter_phone': vacancy.get('recruiter_phone'),
            'vacancy_url': vacancy.get('vacancy_url'),
            'analysis': analysis,
            'generated_response': generated_response,
            'status': 'pending',  # pending, sent, responded, qualified, closed
            'created_at': datetime.now().isoformat(),
            'sent_at': None,
            'response_received_at': None,
            'meeting_scheduled': False,
            'meeting_url': None,
            'notes': []
        }
        
        self.leads.append(lead)
        logger.info(f"Created lead: {lead['lead_id']} for {vacancy.get('company')}")
        
        return lead
    
    def generate_recruiter_response(self, vacancy: Dict, analysis: Dict,
                                   specialist_contact: Optional[Dict] = None) -> str:
        """
        Generate a personalized response message for the recruiter.
        
        Args:
            vacancy (Dict): Vacancy information
            analysis (Dict): Analysis results
            specialist_contact (Dict, optional): Technical specialist contact information
            
        Returns:
            str: Generated response message
        """
        response = f"""
Dear Hiring Manager,

Thank you for sharing this exciting opportunity for the {vacancy.get('title')} position at {vacancy.get('company')}.

We have reviewed your job description and identified the following key requirements:

Technical Stack:
{self._format_list(analysis.get('technical_requirements', []))}

Key Responsibilities:
{self._format_list(analysis.get('key_responsibilities', []))}

Success Metrics:
{self._format_list(analysis.get('kpis', []))}

Our Proposed Solution:
We have a team of experienced specialists who can effectively address all these requirements. 
Our approach focuses on:
- Rapid understanding of your technical challenges
- Implementation of scalable, maintainable solutions
- Continuous optimization to exceed your KPIs
- Seamless integration with your existing team

We would like to schedule a brief technical discussion to better understand your specific needs 
and propose a tailored solution that aligns with your timeline and budget.

"""
        
        if specialist_contact:
            response += f"""
Technical Specialist Contact:
Name: {specialist_contact.get('name')}
Email: {specialist_contact.get('email')}
Phone: {specialist_contact.get('phone')}

"""
        
        response += """
Please let us know your availability for a 30-minute call this week.

Best regards,
Job Application Agent
"""
        
        return response.strip()
    
    def send_response(self, lead: Dict, response_text: str) -> bool:
        """
        Send a response to the recruiter.
        
        Args:
            lead (Dict): Lead record
            response_text (str): Response message to send
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # TODO: Implement actual sending mechanism
            # This could be:
            # - Direct message through the job platform
            # - Email via SMTP
            # - API call to the platform
            
            logger.info(f"Sending response for lead {lead['lead_id']} to {lead['recruiter_email']}")
            
            # Update lead status
            lead['status'] = 'sent'
            lead['sent_at'] = datetime.now().isoformat()
            
            return True
        
        except Exception as e:
            logger.error(f"Error sending response: {str(e)}")
            return False
    
    def schedule_meeting(self, lead: Dict, calendly_url: str, 
                        crea_url: Optional[str] = None) -> bool:
        """
        Schedule a meeting with the recruiter.
        
        Args:
            lead (Dict): Lead record
            calendly_url (str): Calendly meeting link
            crea_url (str, optional): Crea meeting link
            
        Returns:
            bool: True if scheduled successfully
        """
        try:
            # TODO: Implement actual meeting scheduling
            # This could involve:
            # - Creating a Calendly event
            # - Creating a Crea meeting
            # - Sending meeting invitation
            
            logger.info(f"Scheduling meeting for lead {lead['lead_id']}")
            
            lead['meeting_scheduled'] = True
            lead['meeting_url'] = calendly_url
            
            return True
        
        except Exception as e:
            logger.error(f"Error scheduling meeting: {str(e)}")
            return False
    
    def notify_maxim(self, lead: Dict) -> bool:
        """
        Notify Maxim about a new lead.
        
        Args:
            lead (Dict): Lead record to notify about
            
        Returns:
            bool: True if notification sent successfully
        """
        try:
            notification = self._prepare_notification(lead)
            
            # TODO: Implement actual notification mechanism
            # This could be:
            # - Email
            # - Slack message
            # - SMS
            # - CRM integration
            
            logger.info(f"Notifying Maxim about lead {lead['lead_id']}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error notifying Maxim: {str(e)}")
            return False
    
    def _prepare_notification(self, lead: Dict) -> Dict:
        """
        Prepare a notification message for Maxim.
        
        Args:
            lead (Dict): Lead record
            
        Returns:
            Dict: Notification content
        """
        notification = {
            'lead_id': lead['lead_id'],
            'company': lead['company'],
            'position': lead['vacancy_title'],
            'recruiter_name': lead['recruiter_name'],
            'recruiter_email': lead['recruiter_email'],
            'recruiter_phone': lead['recruiter_phone'],
            'vacancy_url': lead['vacancy_url'],
            'generated_response': lead['generated_response'],
            'meeting_url': lead.get('meeting_url'),
            'timestamp': datetime.now().isoformat(),
            'action_required': 'Review and follow up with recruiter'
        }
        
        return notification
    
    def get_lead_status(self, lead_id: str) -> Optional[Dict]:
        """
        Get the status of a specific lead.
        
        Args:
            lead_id (str): Lead ID
            
        Returns:
            Dict: Lead information, or None if not found
        """
        for lead in self.leads:
            if lead['lead_id'] == lead_id:
                return lead
        return None
    
    def get_all_leads(self, status: Optional[str] = None) -> List[Dict]:
        """
        Get all leads, optionally filtered by status.
        
        Args:
            status (str, optional): Filter by lead status
            
        Returns:
            List[Dict]: List of leads
        """
        if status:
            return [lead for lead in self.leads if lead['status'] == status]
        return self.leads
    
    def save_leads(self, filepath: str) -> bool:
        """
        Save all leads to a JSON file.
        
        Args:
            filepath (str): Path to save the leads file
            
        Returns:
            bool: True if successful
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.leads, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.leads)} leads to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving leads: {str(e)}")
            return False
    
    @staticmethod
    def _generate_lead_id() -> str:
        """Generate a unique lead ID."""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = random.randint(1000, 9999)
        return f"LEAD_{timestamp}_{random_suffix}"
    
    @staticmethod
    def _format_list(items: List[str]) -> str:
        """Format a list of items for display."""
        if not items:
            return "- Not specified"
        return '\n'.join([f"- {item}" for item in items])


if __name__ == "__main__":
    # Example usage
    generator = LeadGenerator(
        maxim_contact={
            'name': 'Maxim',
            'email': 'maxim@example.com',
            'phone': '+1234567890'
        }
    )
    
    sample_vacancy = {
        'title': 'Senior Python Developer',
        'company': 'TechCorp',
        'recruiter_name': 'John Doe',
        'recruiter_email': 'john@techcorp.com',
        'recruiter_phone': '+1234567890',
        'vacancy_url': 'https://example.com/vacancy/123'
    }
    
    sample_analysis = {
        'technical_requirements': ['Python', 'Django', 'PostgreSQL'],
        'key_responsibilities': ['Design solutions', 'Lead team'],
        'kpis': ['Deliver on time', 'Code quality']
    }
    
    lead = generator.create_lead(sample_vacancy, sample_analysis, "Test response")
    print(json.dumps(lead, indent=2))

