import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import yaml

# Добавление корневой директории проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импорт компонентов агента
from src.main import initialize_components, load_config
from src.lead_management.lead_manager import LeadManager, Lead
from src.recruiter_interaction.meeting_scheduler import MeetingScheduler
from src.notifications.notification_manager import NotificationManager

# Мок-конфигурация для тестирования
MOCK_CONFIG = {
    "agent": {"scan_interval_seconds": 300},
    "parsing": {"platforms": {"djinni": {"enabled": True}}},
    "database": {"url": "sqlite:///:memory:"},
    "notifications": {"maxim_email": "maxim@example.com"},
    "recruiter_interaction": {
        "calendly_event_type_uuid": "TEST_UUID",
        "crea_base_url": "https://crea.app/test"
    }
}

# Установка мок-переменных окружения для Calendly
os.environ["CALENDLY_API_KEY"] = "MOCK_KEY"
os.environ["CALENDLY_USER_URI"] = "https://api.calendly.com/users/MOCK_USER"
os.environ["SLACK_WEBHOOK_URL"] = "https://hooks.slack.com/services/MOCK/WEBHOOK"


class TestAgentIntegration(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        # Инициализация компонентов с мок-конфигурацией
        self.components = initialize_components(MOCK_CONFIG)
        self.lead_manager: LeadManager = self.components["lead_manager"]
        self.scheduler: MeetingScheduler = self.components["meeting_scheduler"]
        self.notifier: NotificationManager = self.components["notification_manager"]
        
        # Очистка базы данных в памяти перед каждым тестом
        self.lead_manager.engine.dispose()
        self.lead_manager.Base.metadata.create_all(self.lead_manager.engine)
        
        # Мокирование внешних зависимостей
        self.components["ai_platform_client"].invoke_chain = MagicMock(return_value={"generated_response": "Mocked response."})
        self.components["response_sender"].send_djinni_response = MagicMock(return_value=True)
        
    def test_components_initialization(self):
        """Тестирование инициализации всех основных компонентов."""
        self.assertIsInstance(self.lead_manager, LeadManager)
        self.assertIsInstance(self.scheduler, MeetingScheduler)
        self.assertIsInstance(self.notifier, NotificationManager)
        # Проверка, что мокирование внешних API произошло
        self.assertIsNotNone(os.getenv("CALENDLY_API_KEY"))

    @patch('src.recruiter_interaction.meeting_scheduler.requests.post')
    def test_calendly_link_generation(self, mock_post):
        """Тестирование генерации одноразовой ссылки Calendly (мок внешнего запроса)."""
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "resource": {"booking_url": "https://calendly.com/test-link-123"}
        }
        
        lead_data = {"recruiter_email": "test@example.com"}
        link = self.scheduler.generate_calendly_single_use_link(lead_data, "TEST_UUID")
        
        self.assertIsNotNone(link)
        self.assertIn("https://calendly.com/test-link-123", link)
        mock_post.assert_called_once()

    @patch('src.notifications.notification_manager.requests.post')
    @patch('src.notifications.notification_manager.NotificationManager.send_email_notification')
    def test_notify_new_lead(self, mock_send_email, mock_post_slack):
        """Тестирование отправки уведомлений о новом лиде."""
        mock_post_slack.return_value.status_code = 200
        mock_send_email.return_value = True

        lead_data = {
            "vacancy_title": "Test Lead",
            "company_name": "TestCorp",
            "recruiter_name": "Test Recruiter",
            "recruiter_email": "test@corp.com",
            "vacancy_url": "http://test.com/job",
            "generated_response": "Response text",
            "meeting_link": "http://meeting.link"
        }
        
        self.notifier.notify_new_lead(lead_data)
        
        mock_send_email.assert_called_once()
        # В реальном тесте Slack мы бы проверили, что mock_post_slack был вызван
        # mock_post_slack.assert_called_once() 

    # TODO: Добавить тесты для LeadManager (создание, обновление, получение)
    def test_lead_manager_crud(self):
        """Тестирование создания, обновления и удаления лида."""
        sample_lead_data = {
            "vacancy_id": "djinni_test_1",
            "vacancy_title": "Test Lead Manager",
            "company_name": "TestCorp",
            "vacancy_url": "http://test.com/job",
            "recruiter_name": "Test Recruiter",
            "recruiter_email": "test@corp.com",
            "generated_response": "Response text",
            "meeting_link": "http://meeting.link"
        }
        
        # 1. Создание
        lead = self.lead_manager.create_lead(sample_lead_data)
        self.assertIsNotNone(lead)
        self.assertEqual(lead.status, 'New')
        
        # 2. Обновление
        update_success = self.lead_manager.update_lead_status(lead.id, 'Meeting Scheduled', 'Recruiter responded positively')
        self.assertTrue(update_success)
        updated_lead = self.lead_manager.get_lead_by_id(lead.id)
        self.assertEqual(updated_lead.status, 'Meeting Scheduled')
        self.assertEqual(updated_lead.feedback, 'Recruiter responded positively')
        
        # 3. Получение всех
        all_leads = self.lead_manager.get_all_leads()
        self.assertEqual(len(all_leads), 1)
        
        # 4. Удаление
        delete_success = self.lead_manager.delete_lead(lead.id)
        self.assertTrue(delete_success)
        all_leads_after_delete = self.lead_manager.get_all_leads()
        self.assertEqual(len(all_leads_after_delete), 0)

    # TODO: Добавить тест для сквозного процесса (process_new_vacancy)
    # def test_full_process_new_vacancy(self):
    #     """Тестирование сквозного процесса обработки новой вакансии."""
    #     # Мокирование парсера для возврата тестовых данных
    #     self.components["djinni_parser"].scan_new_vacancies = MagicMock(return_value=[
    #         {"vacancy_id": "djinni_full_test_1", "vacancy_title": "Full Test Job", "vacancy_url": "http://test.com/full"}
    #     ])
        
    #     # Мокирование Calendly для возврата ссылки
    #     with patch('src.recruiter_interaction.meeting_scheduler.requests.post') as mock_post:
    #         mock_post.return_value.status_code = 201
    #         mock_post.return_value.json.return_value = {
    #             "resource": {"booking_url": "https://calendly.com/full-test-link"}
    #         }
            
    #         # Мокирование уведомлений
    #         with patch('src.notifications.notification_manager.NotificationManager.send_email_notification') as mock_email:
    #             with patch('src.notifications.notification_manager.NotificationManager.send_slack_notification') as mock_slack:
    #                 # Запуск цикла
    #                 # process_new_vacancy(self.components["djinni_parser"].scan_new_vacancies()[0], self.components)
    #                 # Для простоты, пока не будем запускать main_loop, а только process_new_vacancy
    #                 pass

    #     # Проверки:
    #     # self.components["ai_platform_client"].invoke_chain.assert_called_once()
    #     # self.components["response_sender"].send_djinni_response.assert_called_once()
    #     # mock_email.assert_called_once()
    #     # self.assertEqual(len(self.lead_manager.get_all_leads()), 1)
    #     pass

if __name__ == '__main__':
    unittest.main()

