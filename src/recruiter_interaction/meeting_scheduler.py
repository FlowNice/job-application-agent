import logging
import requests
from typing import Dict, Optional
import os

logger = logging.getLogger(__name__)

class MeetingScheduler:
    """
    Manages the creation of meeting links using various scheduling platforms.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.calendly_api_key = os.getenv("CALENDLY_API_KEY")
        self.calendly_api_url = "https://api.calendly.com"
        self.calendly_user_uri = os.getenv("CALENDLY_USER_URI") # e.g., "https://api.calendly.com/users/YOUR_USER_UUID"
        
        if not self.calendly_api_key or not self.calendly_user_uri:
            logger.warning("Calendly API key or User URI not set in environment variables. Calendly integration may not work.")
        
        logger.info("MeetingScheduler initialized.")

    def generate_calendly_single_use_link(self, lead_data: Dict, event_type_uuid: str) -> Optional[str]:
        """
        Generates a Calendly single-use meeting link for a specific event type.
        
        Args:
            lead_data (Dict): Data about the lead (e.g., recruiter email, name, vacancy title).
            event_type_uuid (str): The UUID of the Calendly event type to create a link for.
            
        Returns:
            Optional[str]: A Calendly scheduling URL, or None if generation fails.
        """
        if not self.calendly_api_key or not self.calendly_user_uri:
            logger.error("Calendly API key or User URI is missing. Cannot generate single-use link.")
            return None

        headers = {
            "Authorization": f"Bearer {self.calendly_api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "max_uses": 1, # Single-use link
            "owner": self.calendly_user_uri,
            "owner_type": "User",
            "event_type": f"{self.calendly_api_url}/event_types/{event_type_uuid}"
        }

        logger.info(f"Attempting to generate Calendly single-use link for lead: {lead_data.get('recruiter_email')}")
        try:
            response = requests.post(
                f"{self.calendly_api_url}/scheduling_links",
                headers=headers,
                json=payload
            )
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            
            scheduling_link = response.json().get("resource", {}).get("booking_url")
            if scheduling_link:
                logger.info(f"Successfully generated Calendly link: {scheduling_link}")
                # Optionally, add pre-fill parameters if Calendly supports them for single-use links
                # Example: f"{scheduling_link}?name={lead_data.get("recruiter_name", "")}&email={lead_data.get("recruiter_email", "")}"
                return scheduling_link
            else:
                logger.error(f"Calendly API did not return a booking_url: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating Calendly link: {e}")
            return None

    def generate_crea_link(self, lead_data: Dict) -> Optional[str]:
        """
        Generates a Crea meeting link based on lead data.
        Placeholder for future Crea integration.
        """
        crea_base_url = self.config.get("recruiter_interaction", {}).get("crea_base_url")
        if not crea_base_url:
            logger.warning("Crea base URL not configured. Cannot generate link.")
            return None
            
        logger.info(f"Generating Crea link for lead: {lead_data.get('recruiter_email')}")
        # Placeholder: Return a generic Crea link
        return f"{crea_base_url}?name={lead_data.get("recruiter_name", "")}&email={lead_data.get("recruiter_email", "")}"

if __name__ == "__main__":
    # Пример использования (Example usage)
    # Для запуска этого примера необходимо установить переменные окружения:
    # CALENDLY_API_KEY="YOUR_CALENDLY_PERSONAL_ACCESS_TOKEN"
    # CALENDLY_USER_URI="https://api.calendly.com/users/YOUR_USER_UUID"
    # EVENT_TYPE_UUID="YOUR_EVENT_TYPE_UUID"

    # from dotenv import load_dotenv
    # load_dotenv()

    # config_example = {"recruiter_interaction": {"crea_base_url": "https://crea.app/your-meeting-link"}}
    # scheduler = MeetingScheduler(config_example)
    
    # sample_lead_data = {
    #     "recruiter_name": "Jane Doe",
    #     "recruiter_email": "jane.doe@example.com",
    #     "vacancy_title": "Senior AI Engineer"
    # }
    
    # # Пример генерации одноразовой ссылки Calendly
    # event_type_uuid = os.getenv("EVENT_TYPE_UUID")
    # if event_type_uuid:
    #     calendly_link = scheduler.generate_calendly_single_use_link(sample_lead_data, event_type_uuid)
    #     if calendly_link:
    #         print(f"Generated Calendly single-use link: {calendly_link}")
    # else:
    #     print("EVENT_TYPE_UUID not set. Cannot test Calendly single-use link generation.")
    
    # crea_link = scheduler.generate_crea_link(sample_lead_data)
    # if crea_link:
    #     print(f"Generated Crea link: {crea_link}")

