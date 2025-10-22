"""
Djinni.co Job Vacancy Parser

This module handles scraping and parsing job vacancies from Djinni.co.
It extracts key information such as job title, description, requirements,
and recruiter contact details.
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DjinniParser:
    """
    Parser for Djinni.co job vacancies.
    
    Attributes:
        base_url (str): Base URL for Djinni.co API or web scraping
        headers (dict): HTTP headers for requests
    """
    
    def __init__(self):
        """Initialize the Djinni parser with default configuration."""
        self.base_url = "https://djinni.co"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_vacancies(self, keywords: Optional[List[str]] = None, 
                       limit: int = 50) -> List[Dict]:
        """
        Fetch job vacancies from Djinni.co.
        
        Args:
            keywords (List[str], optional): Keywords to filter vacancies
            limit (int): Maximum number of vacancies to fetch
            
        Returns:
            List[Dict]: List of vacancy dictionaries with extracted information
        """
        try:
            logger.info(f"Fetching vacancies from Djinni.co with keywords: {keywords}")
            search_url = f"{self.base_url}/jobs/"
            params = {}
            if keywords:
                params["q"] = " ".join(keywords)
            
            response = self.session.get(search_url, params=params)
            response.raise_for_status() # Raise an exception for HTTP errors
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find job listings - this selector might need adjustment based on Djinni.co's current HTML
            job_cards = soup.find_all('div', class_='job-list-item') # Common class for job listings
            
            vacancies = []
            for card in job_cards:
                title_tag = card.find('a', class_='job-list-item__link') # Common class for job title link
                if title_tag:
                    title = title_tag.text.strip()
                    vacancy_url = self.base_url + title_tag['href']
                    
                    # Basic extraction, can be expanded later
                    vacancies.append({
                        'title': title,
                        'vacancy_url': vacancy_url,
                        'company': card.find('div', class_='text-muted').text.strip() if card.find('div', class_='text-muted') else None,
                        'posted_date': card.find('div', class_='text-date').text.strip() if card.find('div', class_='text-date') else None,
                        'description': None, # Detailed description requires visiting each page
                        'parsed_at': datetime.now().isoformat()
                    })
                    
                if len(vacancies) >= limit:
                    break
            
            logger.info(f"Successfully fetched {len(vacancies)} vacancies")
            return vacancies
        
        except Exception as e:
            logger.error(f"Error fetching vacancies: {str(e)}")
            return []
    
    def parse_vacancy(self, vacancy_html: str) -> Dict:
        """
        Parse a single vacancy HTML and extract key information.
        
        Args:
            vacancy_html (str): HTML content of the vacancy page
            
        Returns:
            Dict: Parsed vacancy information
        """
        try:
            soup = BeautifulSoup(vacancy_html, 'html.parser')
            
            vacancy = {
                'title': None,
                'company': None,
                'description': None,
                'requirements': None,
                'salary': None,
                'location': None,
                'job_type': None,
                'experience_level': None,
                'recruiter_name': None,
                'recruiter_email': None,
                'recruiter_phone': None,
                'vacancy_url': None,
                'posted_date': None,
                'parsed_at': datetime.now().isoformat()
            }
            
            # TODO: Implement actual parsing logic
            # Extract title, description, requirements, etc.
            
            return vacancy
        
        except Exception as e:
            logger.error(f"Error parsing vacancy: {str(e)}")
            return {}
    
    def filter_vacancies(self, vacancies: List[Dict], 
                        keywords: Optional[List[str]] = None,
                        min_experience: Optional[str] = None,
                        locations: Optional[List[str]] = None) -> List[Dict]:
        """
        Filter vacancies based on specified criteria.
        
        Args:
            vacancies (List[Dict]): List of vacancies to filter
            keywords (List[str], optional): Keywords that must appear in title/description
            min_experience (str, optional): Minimum experience level
            locations (List[str], optional): Desired locations
            
        Returns:
            List[Dict]: Filtered list of vacancies
        """
        filtered = vacancies
        
        if keywords:
            filtered = [v for v in filtered if any(
                keyword.lower() in (v.get('title', '') + ' ' + v.get('description', '')).lower()
                for keyword in keywords
            )]
        
        if locations:
            filtered = [v for v in filtered if v.get('location') in locations]
        
        return filtered
    
    def save_vacancies(self, vacancies: List[Dict], filepath: str) -> bool:
        """
        Save parsed vacancies to a JSON file.
        
        Args:
            vacancies (List[Dict]): Vacancies to save
            filepath (str): Path to save the JSON file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(vacancies)} vacancies to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving vacancies: {str(e)}")
            return False


if __name__ == "__main__":
    # Example usage
    parser = DjinniParser()
    print("\n--- Testing DjinniParser --- ")
    parser = DjinniParser()
    
    # Test fetching vacancies
    print("Fetching 5 Python vacancies...")
    vacancies = parser.fetch_vacancies(keywords=['Python'], limit=5)
    if vacancies:
        print(f"Fetched {len(vacancies)} vacancies:")
        for i, vacancy in enumerate(vacancies):
            print(f"  {i+1}. Title: {vacancy.get('title')}, URL: {vacancy.get('vacancy_url')}")
    else:
        print("No vacancies fetched or an error occurred.")

    # Test parsing a single vacancy (requires a full HTML, currently a placeholder)
    # print("\nTesting single vacancy parsing (placeholder)... ")
    # sample_html = "<html><body>...</body></html>" # Replace with actual HTML for testing
    # parsed_data = parser.parse_vacancy(sample_html)
    # print(json.dumps(parsed_data, indent=2))

