import logging
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True)
    vacancy_id = Column(String, unique=True, nullable=False) # ID вакансии на платформе
    vacancy_title = Column(String, nullable=False)
    company_name = Column(String)
    vacancy_url = Column(String, nullable=False)
    recruiter_name = Column(String)
    recruiter_email = Column(String)
    generated_response = Column(Text)
    meeting_link = Column(String)
    status = Column(String, default='New') # New, Contacted, Meeting Scheduled, Rejected, Hired
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Lead(id={self.id}, title='{self.vacancy_title}', status='{self.status}')>"

class LeadManager:
    """
    Manages lead data in the database using SQLAlchemy.
    """
    def __init__(self, db_url: str = "sqlite:///./leads.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine) # Create tables if they don't exist
        self.Session = sessionmaker(bind=self.engine)
        logger.info(f"LeadManager initialized with database: {db_url}")

    def create_lead(self, lead_data: Dict) -> Optional[Lead]:
        """
        Creates a new lead in the database.
        """
        session = self.Session()
        try:
            # Check if lead already exists to prevent duplicates
            existing_lead = session.query(Lead).filter_by(vacancy_id=lead_data['vacancy_id']).first()
            if existing_lead:
                logger.warning(f"Lead for vacancy_id {lead_data['vacancy_id']} already exists. Skipping creation.")
                return existing_lead

            new_lead = Lead(
                vacancy_id=lead_data.get('vacancy_id'),
                vacancy_title=lead_data.get('vacancy_title'),
                company_name=lead_data.get('company_name'),
                vacancy_url=lead_data.get('vacancy_url'),
                recruiter_name=lead_data.get('recruiter_name'),
                recruiter_email=lead_data.get('recruiter_email'),
                generated_response=lead_data.get('generated_response'),
                meeting_link=lead_data.get('meeting_link'),
                status=lead_data.get('status', 'New')
            )
            session.add(new_lead)
            session.commit()
            session.refresh(new_lead)
            logger.info(f"New lead created: {new_lead.vacancy_title}")
            return new_lead
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating lead: {e}")
            return None
        finally:
            session.close()

    def get_lead_by_id(self, lead_id: int) -> Optional[Lead]:
        """
        Retrieves a lead by its ID.
        """
        session = self.Session()
        try:
            return session.query(Lead).filter_by(id=lead_id).first()
        finally:
            session.close()

    def get_lead_by_vacancy_id(self, vacancy_id: str) -> Optional[Lead]:
        """
        Retrieves a lead by its vacancy ID.
        """
        session = self.Session()
        try:
            return session.query(Lead).filter_by(vacancy_id=vacancy_id).first()
        finally:
            session.close()

    def update_lead_status(self, lead_id: int, new_status: str, feedback: Optional[str] = None) -> bool:
        """
        Updates the status and feedback of an existing lead.
        """
        session = self.Session()
        try:
            lead = session.query(Lead).filter_by(id=lead_id).first()
            if lead:
                lead.status = new_status
                if feedback:
                    lead.feedback = feedback
                lead.updated_at = datetime.utcnow()
                session.commit()
                logger.info(f"Lead {lead.id} status updated to {new_status}.")
                return True
            logger.warning(f"Lead with ID {lead_id} not found for status update.")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating lead status for ID {lead_id}: {e}")
            return False
        finally:
            session.close()

    def get_all_leads(self, status: Optional[str] = None) -> List[Lead]:
        """
        Retrieves all leads, optionally filtered by status.
        """
        session = self.Session()
        try:
            query = session.query(Lead)
            if status:
                query = query.filter_by(status=status)
            return query.all()
        finally:
            session.close()

    def delete_lead(self, lead_id: int) -> bool:
        """
        Deletes a lead by its ID.
        """
        session = self.Session()
        try:
            lead = session.query(Lead).filter_by(id=lead_id).first()
            if lead:
                session.delete(lead)
                session.commit()
                logger.info(f"Lead {lead.id} deleted.")
                return True
            logger.warning(f"Lead with ID {lead_id} not found for deletion.")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting lead with ID {lead_id}: {e}")
            return False
        finally:
            session.close()

if __name__ == "__main__":
    # Пример использования (Example usage)
    # from dotenv import load_dotenv
    # load_dotenv()

    # manager = LeadManager(db_url="sqlite:///test_leads.db")

    # sample_lead_data = {
    #     "vacancy_id": "djinni_12345",
    #     "vacancy_title": "Python Developer",
    #     "company_name": "Tech Solutions Inc.",
    #     "vacancy_url": "https://djinni.co/jobs/12345",
    #     "recruiter_name": "John Doe",
    #     "recruiter_email": "john.doe@example.com",
    #     "generated_response": "Привет! Я очень заинтересован...",
    #     "meeting_link": "https://calendly.com/meeting-link-123",
    #     "status": "New"
    # }

    # lead = manager.create_lead(sample_lead_data)
    # if lead:
    #     print(f"Создан лид: {lead}")
    #     manager.update_lead_status(lead.id, "Contacted")
    #     updated_lead = manager.get_lead_by_id(lead.id)
    #     print(f"Обновленный лид: {updated_lead}")

    # all_leads = manager.get_all_leads()
    # print("Все лиды:")
    # for l in all_leads:
    #     print(l)

    # manager.delete_lead(lead.id)
    # print(f"Лид {lead.id} удален.")
    # all_leads_after_delete = manager.get_all_leads()
    # print(f"Лидов после удаления: {len(all_leads_after_delete)}")

