import time
import yaml
import logging
from typing import Dict, Any

# Импорт модулей агента
from src.parsers.djinni_parser import DjinniParser
from src.analyzer.vacancy_analyzer import VacancyAnalyzer
from src.recruiter_interaction.response_sender import ResponseSender
from src.recruiter_interaction.meeting_scheduler import MeetingScheduler
from src.notifications.notification_manager import NotificationManager
from src.lead_management.lead_manager import LeadManager
from src.ai_platform_integration.ai_platform_api_client import AIPlatformAPIClient
# from src.utils.logger import setup_logging # Предполагается, что setup_logging будет реализован

# Настройка базового логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TalentFlowAgent")

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Загружает конфигурацию из YAML-файла."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        return {}

def initialize_components(config: Dict) -> Dict[str, Any]:
    """Инициализирует все компоненты агента."""
    
    # Инициализация AI-платформы (LLM Orchestration)
    ai_platform_client = AIPlatformAPIClient(config)
    
    # Инициализация парсеров
    djinni_config = config.get("parsing", {}).get("platforms", {}).get("djinni", {})
    djinni_parser = DjinniParser(djinni_config)
    
    # Инициализация менеджера лидов (CRM)
    db_url = config.get("database", {}).get("url", "sqlite:///leads.db")
    lead_manager = LeadManager(db_url=db_url)

    # Инициализация анализатора
    vacancy_analyzer = VacancyAnalyzer(config, ai_platform_client, lead_manager)
    
    # Инициализация модулей взаимодействия
    response_sender = ResponseSender(config)
    meeting_scheduler = MeetingScheduler(config)
    notification_manager = NotificationManager(config)

    return {
        "djinni_parser": djinni_parser,
        "vacancy_analyzer": vacancy_analyzer,
        "response_sender": response_sender,
        "meeting_scheduler": meeting_scheduler,
        "notification_manager": notification_manager,
        "lead_manager": lead_manager,
        "ai_platform_client": ai_platform_client,
    }

def process_new_vacancy(vacancy_data: Dict, components: Dict):
    """
    Обрабатывает одну новую вакансию: анализирует, генерирует ответ,
    отправляет отклик, создает лид и уведомляет Максима.
    """
    logger.info(f"Processing new vacancy: {vacancy_data.get('vacancy_title')}")
    
    # 1. Проверка на дубликат (уже есть в лидах)
    if components["lead_manager"].get_lead_by_vacancy_id(vacancy_data.get("vacancy_id")):
        logger.info(f"Vacancy {vacancy_data.get('vacancy_id')} already processed. Skipping.")
        return

    # 2. Анализ и генерация ответа
    analysis_result = components["vacancy_analyzer"].analyze_and_generate_response(vacancy_data)
    
    if not analysis_result or not analysis_result.get("generated_response"):
        logger.error(f"Failed to analyze or generate response for {vacancy_data.get('vacancy_id')}")
        return

    generated_response = analysis_result["generated_response"]
    
    # 3. Генерация ссылки на встречу (Placeholder for real data)
    lead_data_for_scheduler = {
        "recruiter_name": analysis_result.get("recruiter_name", "Recruiter"),
        "recruiter_email": analysis_result.get("recruiter_email", "unknown@example.com"),
        "vacancy_title": vacancy_data.get('vacancy_title')
    }
    
    # Получение UUID event_type из конфигурации
    event_type_uuid = components["meeting_scheduler"].config.get("recruiter_interaction", {}).get("calendly_event_type_uuid")
    
    meeting_link = components["meeting_scheduler"].generate_calendly_single_use_link(
        lead_data_for_scheduler,
        event_type_uuid=event_type_uuid or "placeholder_uuid" # Заглушка, если нет в конфиге
    )

    # 4. Отправка отклика
    send_success = components["response_sender"].send_djinni_response(
        vacancy_data.get("vacancy_id"),
        generated_response
    )

    # 5. Создание лида в CRM
    lead_data = {
        **vacancy_data,
        "generated_response": generated_response,
        "meeting_link": meeting_link,
        "status": "Contacted" if send_success else "Analysis Complete"
    }
    new_lead = components["lead_manager"].create_lead(lead_data)

    # 6. Уведомление Максима
    if new_lead and send_success:
        components["notification_manager"].notify_new_lead(lead_data)
        logger.info(f"Successfully processed and notified Maxim about new lead: {new_lead.vacancy_title}")
    elif new_lead:
        logger.warning(f"Lead created but response failed to send for {new_lead.vacancy_title}. Maxim not notified.")

def main_loop(config: Dict, components: Dict):
    """Основной цикл работы агента."""
    scan_interval = config.get("agent", {}).get("scan_interval_seconds", 300) # 5 минут

    while True:
        logger.info("--- Starting new scan cycle ---")
        
        # 1. Парсинг новых вакансий (Djinni)
        try:
            new_vacancies = components["djinni_parser"].scan_new_vacancies()
            logger.info(f"Found {len(new_vacancies)} new vacancies on Djinni.co.")
            
            for vacancy in new_vacancies:
                process_new_vacancy(vacancy, components)
                
        except Exception as e:
            logger.error(f"Critical error during scan cycle: {e}", exc_info=True)

        logger.info(f"--- Scan cycle finished. Sleeping for {scan_interval} seconds ---")
        time.sleep(scan_interval)

def start_agent():
    """Точка входа для запуска агента."""
    logger.info("Starting TalentFlow Agent...")
    
    config = load_config()
    if not config:
        logger.critical("Agent cannot start without a valid configuration.")
        return

    components = initialize_components(config)
    
    # Запуск основного цикла
    try:
        main_loop(config, components)
    except KeyboardInterrupt:
        logger.info("Agent stopped by user (KeyboardInterrupt).")
    except Exception as e:
        logger.critical(f"Agent crashed due to unhandled exception: {e}", exc_info=True)

if __name__ == "__main__":
    start_agent()

