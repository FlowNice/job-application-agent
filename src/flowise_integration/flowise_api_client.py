"""
Flowise API Client Module

Этот модуль предоставляет клиент для взаимодействия с Flowise API (Flowise API).
Он включает функции для отправки данных в чатфлоу (chatflows) Flowise
и получения ответов.
"""

import requests
import json
import logging
from typing import Dict, Any, Optional

# Настройка логирования (Logging setup)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlowiseAPIClient:
    """
    Клиент для взаимодействия с Flowise API (Client for Flowise API interaction).
    """

    def __init__(self, api_url: str, api_key: str):
        """
        Инициализирует клиент Flowise API (Initializes the Flowise API client).

        Args:
            api_url (str): Базовый URL для Flowise API (Base URL for Flowise API).
            api_key (str): API ключ для аутентификации (API key for authentication).
        """
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        logger.info(f"FlowiseAPIClient инициализирован для {api_url}")

    def invoke_chatflow(self, chatflow_id: str, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Вызывает определенный чатфлоу Flowise (Invokes a specific Flowise chatflow).

        Args:
            chatflow_id (str): ID чатфлоу для вызова (Chatflow ID to invoke).
            input_data (Dict[str, Any]): Входные данные для чатфлоу (Input data for the chatflow).

        Returns:
            Optional[Dict[str, Any]]: Ответ от чатфлоу Flowise или None в случае ошибки (Response from Flowise chatflow or None on error).
        """
        endpoint = f"{self.api_url}/v1/prediction/{chatflow_id}"
        payload = {
            "question": json.dumps(input_data) # Flowise часто ожидает строковый JSON в поле 'question'
        }

        logger.info(f"Вызов чатфлоу {chatflow_id} с данными: {input_data}")
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()  # Вызывает исключение для HTTP ошибок (Raises HTTPError for bad responses)
            result = response.json()
            logger.info(f"Успешный ответ от Flowise: {result}")
            return result
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка при вызове Flowise чатфлоу {chatflow_id}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Ошибка подключения к Flowise API {self.api_url}: {e}")
        except requests.exceptions.Timeout as e:
            logger.error(f"Таймаут при ожидании ответа от Flowise API {self.api_url}: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при вызове Flowise чатфлоу: {e}")
        return None

    def analyze_vacancy(self, vacancy_data: Dict[str, Any], chatflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Отправляет данные о вакансии для анализа в Flowise (Sends vacancy data for analysis to Flowise).

        Args:
            vacancy_data (Dict[str, Any]): Данные о вакансии (Vacancy data).
            chatflow_id (str): ID чатфлоу для анализа вакансий (Chatflow ID for vacancy analysis).

        Returns:
            Optional[Dict[str, Any]]: Результат анализа от Flowise (Analysis result from Flowise).
        """
        logger.info(f"Отправка вакансии на анализ в Flowise (чатфлоу: {chatflow_id})")
        return self.invoke_chatflow(chatflow_id, vacancy_data)

    def generate_response(self, analysis_result: Dict[str, Any], chatflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Генерирует ответ на вакансию с помощью Flowise (Generates a response to a vacancy using Flowise).

        Args:
            analysis_result (Dict[str, Any]): Результат анализа вакансии (Vacancy analysis result).
            chatflow_id (str): ID чатфлоу для генерации ответа (Chatflow ID for response generation).

        Returns:
            Optional[Dict[str, Any]]: Сгенерированный ответ от Flowise (Generated response from Flowise).
        """
        logger.info(f"Отправка результатов анализа для генерации ответа в Flowise (чатфлоу: {chatflow_id})")
        return self.invoke_chatflow(chatflow_id, analysis_result)

if __name__ == "__main__":
    # Пример использования (Example usage)
    # В реальном приложении эти значения будут браться из config.yaml или переменных окружения
    # In a real application, these values would come from config.yaml or environment variables
    
    # Замените на ваш реальный URL и ключ Flowise (Replace with your actual Flowise URL and key)
    MOCK_FLOWISE_API_URL = "http://localhost:3000/api"
    MOCK_FLOWISE_API_KEY = "your_flowise_api_key_here"
    MOCK_VACANCY_ANALYSIS_CHATFLOW_ID = "your_vacancy_analysis_chatflow_id_here"
    MOCK_RESPONSE_GENERATION_CHATFLOW_ID = "your_response_generation_chatflow_id_here"

    client = FlowiseAPIClient(MOCK_FLOWISE_API_URL, MOCK_FLOWISE_API_KEY)

    # Пример данных о вакансии (Example vacancy data)
    sample_vacancy_data = {
        "vacancy_title": "Senior Python Developer",
        "company": "Tech Solutions Inc.",
        "description": "Looking for an experienced Python developer with strong Django and FastAPI skills. Must be proficient in AWS and microservices. KPI: Improve system performance by 15% in Q4.",
        "requirements": "5+ years Python, Django, FastAPI, AWS, Docker, Microservices."
    }

    print("\n--- Тестирование анализа вакансий (Testing Vacancy Analysis) ---")
    analysis_result = client.analyze_vacancy(sample_vacancy_data, MOCK_VACANCY_ANALYSIS_CHATFLOW_ID)
    if analysis_result:
        print("Результат анализа вакансии:")
        print(json.dumps(analysis_result, indent=2))
    else:
        print("Ошибка при анализе вакансии.")

    print("\n--- Тестирование генерации ответа (Testing Response Generation) ---")
    if analysis_result:
        response_result = client.generate_response(analysis_result, MOCK_RESPONSE_GENERATION_CHATFLOW_ID)
        if response_result:
            print("Сгенерированный ответ:")
            print(json.dumps(response_result, indent=2))
        else:
            print("Ошибка при генерации ответа.")
    else:
        print("Невозможно сгенерировать ответ без результата анализа.")

