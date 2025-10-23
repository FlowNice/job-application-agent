import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class NotificationManager:
    """
    Manages sending notifications to Maxim via various channels like Email and Slack.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.maxim_email = self.config.get("notifications", {}).get("maxim_email")
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")

        if not self.maxim_email:
            logger.warning("Maxim's email not configured in config.yaml. Email notifications will not be sent.")
        if not self.slack_webhook_url:
            logger.warning("Slack webhook URL not set in environment variables. Slack notifications will not be sent.")

        logger.info("NotificationManager initialized.")

    def send_email_notification(self, subject: str, body: str) -> bool:
        """
        Sends an email notification to Maxim.
        """
        if not self.maxim_email:
            logger.error("Maxim's email is not configured. Cannot send email notification.")
            return False
        
        logger.info(f"Attempting to send email to {self.maxim_email} with subject: {subject}")
        # Placeholder for actual email sending logic (e.g., using SMTPLIB or a transactional email service API)
        # For now, just simulate success
        logger.warning("Email sending is not yet implemented. Simulating success.")
        return True

    def send_slack_notification(self, message: str) -> bool:
        """
        Sends a Slack notification to a configured webhook URL.
        """
        if not self.slack_webhook_url:
            logger.error("Slack webhook URL is not configured. Cannot send Slack notification.")
            return False
        
        logger.info("Attempting to send Slack notification.")
        # Placeholder for actual Slack sending logic using requests
        # try:
        #     response = requests.post(self.slack_webhook_url, json={'text': message})
        #     response.raise_for_status()
        #     logger.info("Slack notification sent successfully.")
        #     return True
        # except requests.exceptions.RequestException as e:
        #     logger.error(f"Error sending Slack notification: {e}")
        #     return False
        logger.warning("Slack sending is not yet implemented. Simulating success.")
        return True

    def notify_new_lead(self, lead_data: Dict) -> None:
        """
        Notifies Maxim about a new generated lead.
        """
        subject = f"Новый потенциальный лид: {lead_data.get('vacancy_title', 'Без названия')}"
        body = (
            f"Привет, Максим!\n\n" 
            f"Был сгенерирован новый потенциальный лид:\n" 
            f"Вакансия: {lead_data.get('vacancy_title', 'N/A')}\n" 
            f"Компания: {lead_data.get('company_name', 'N/A')}\n" 
            f"Рекрутер: {lead_data.get('recruiter_name', 'N/A')} ({lead_data.get('recruiter_email', 'N/A')})\n" 
            f"Ссылка на вакансию: {lead_data.get('vacancy_url', 'N/A')}\n" 
            f"Сгенерированный отклик: {lead_data.get('generated_response', 'N/A')}\n" 
            f"Ссылка для встречи: {lead_data.get('meeting_link', 'N/A')}\n\n" 
            f"Пожалуйста, проверь и свяжись с рекрутером.\n" 
            f"С уважением, TalentFlow Agent"
        )
        slack_message = f"*Новый лид:* {lead_data.get('vacancy_title', 'Без названия')} от {lead_data.get('company_name', 'N/A')}. Подробности: {lead_data.get('vacancy_url', 'N/A')}"

        self.send_email_notification(subject, body)
        self.send_slack_notification(slack_message)
        logger.info(f"Notified Maxim about new lead: {lead_data.get('vacancy_title')}")

    def notify_recruiter_response(self, lead_data: Dict, response_text: str) -> None:
        """
        Notifies Maxim about a response from a recruiter.
        """
        subject = f"Ответ от рекрутера по вакансии: {lead_data.get('vacancy_title', 'Без названия')}"
        body = (
            f"Привет, Максим!\n\n" 
            f"Получен ответ от рекрутера {lead_data.get('recruiter_name', 'N/A')} ({lead_data.get('recruiter_email', 'N/A')})\n" 
            f"по вакансии: {lead_data.get('vacancy_title', 'N/A')} в компании {lead_data.get('company_name', 'N/A')}.\n" 
            f"Текст ответа: {response_text}\n\n" 
            f"Ссылка на вакансию: {lead_data.get('vacancy_url', 'N/A')}\n\n" 
            f"С уважением, TalentFlow Agent"
        )
        slack_message = f"*Ответ от рекрутера:* {lead_data.get('recruiter_name', 'N/A')} по вакансии {lead_data.get('vacancy_title', 'N/A')}. Текст: {response_text[:100]}..."

        self.send_email_notification(subject, body)
        self.send_slack_notification(slack_message)
        logger.info(f"Notified Maxim about recruiter response for: {lead_data.get('vacancy_title')}")

    def notify_scheduled_meeting(self, lead_data: Dict, meeting_link: str) -> None:
        """
        Notifies Maxim about a newly scheduled meeting.
        """
        subject = f"Запланирована встреча по вакансии: {lead_data.get('vacancy_title', 'Без названия')}"
        body = (
            f"Привет, Максим!\n\n" 
            f"Запланирована встреча с рекрутером {lead_data.get('recruiter_name', 'N/A')} ({lead_data.get('recruiter_email', 'N/A')})\n" 
            f"по вакансии: {lead_data.get('vacancy_title', 'N/A')} в компании {lead_data.get('company_name', 'N/A')}.\n" 
            f"Ссылка на встречу: {meeting_link}\n\n" 
            f"С уважением, TalentFlow Agent"
        )
        slack_message = f"*Встреча запланирована:* по вакансии {lead_data.get('vacancy_title', 'N/A')} с {lead_data.get('recruiter_name', 'N/A')}. Ссылка: {meeting_link}"

        self.send_email_notification(subject, body)
        self.send_slack_notification(slack_message)
        logger.info(f"Notified Maxim about scheduled meeting for: {lead_data.get('vacancy_title')}")


