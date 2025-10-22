# Setup Guide for Job Application Agent

This guide provides instructions for setting up the Job Application Agent, including dependencies, Flowise, and API keys.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

*   **Git**: For cloning the repository.
*   **Docker & Docker Compose**: For running Flowise and other services (PostgreSQL, Redis).
*   **Python 3.11+**: For running the agent itself.
*   **pip**: Python package installer.

## 2. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/FlowNice/job-application-agent.git
cd job-application-agent
```

## 3. Environment Setup

### 3.1. Copy Configuration

Copy the example configuration file and rename it to `config.yaml` (or use environment variables):

```bash
cp config.example.yaml config.yaml
```

### 3.2. Set Environment Variables

Create a `.env` file in the root directory of the project to store sensitive information and API keys. This file will be ignored by Git (as per `.gitignore`).

Example `.env` file:

```dotenv
# Flowise Configuration
FLOWISE_API_URL=http://localhost:3000/api
FLOWISE_API_KEY=your_flowise_api_key_here
FLOWISE_USERNAME=admin
FLOWISE_PASSWORD=password

# OpenAI API Key (for LLM if not using Flowise directly, or if Flowise uses it)
OPENAI_API_KEY=your_openai_api_key_here

# Email Configuration (for sending notifications)
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_email_app_password

# Slack Configuration (for sending notifications)
SLACK_WEBHOOK_URL=your_slack_webhook_url_here

# Database Password (if using PostgreSQL)
DB_PASSWORD=your_db_password_here

# Other API keys (e.g., Twilio for SMS, Calendly/Crea if direct API integration)
# TWILIO_ACCOUNT_SID=your_twilio_account_sid
# TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

**Important**: Replace `your_..._here` placeholders with your actual keys and credentials.

## 4. Running Services with Docker Compose

The project uses Docker Compose to manage its services, including Flowise, PostgreSQL, and Redis.

### 4.1. Start Services

To start all services, run:

```bash
docker-compose up -d
```

This will:
*   Build the `agent` service (your job application agent).
*   Start a PostgreSQL database for data storage.
*   Start a Flowise instance for LLM orchestration.
*   Start a Redis instance for caching (optional).

### 4.2. Access Flowise UI

Once Flowise is running (it might take a few minutes to initialize), you can access its UI at `http://localhost:3000`.

*   **Default Credentials**: `username: admin`, `password: password` (or as set in your `.env` file).
    *   **Создание чатфлоу (Create Chatflows)**: Внутри Flowise вам потребуется создать чатфлоу для `vacancy_analysis` (анализ вакансий) и `response_generation` (генерация ответов), как указано в `config.yaml`.
        *   После создания чатфлоу, вы найдете его **Chatflow ID** в пользовательском интерфейсе Flowise. Этот ID необходимо будет обновить в вашем файле `config.yaml` или `.env`.
        *   **Важно**: Убедитесь, что ваш чатфлоу принимает JSON-объект в качестве `question` (вопроса) и возвращает структурированный JSON-ответ, как описано в `docs/flowise_templates/vacancy_analysis_prompt.md`.

### 4.3. Stop Services

To stop all services, run:

```bash
docker-compose down
```

## 5. Installing Python Dependencies

If you plan to run the Python agent directly (outside Docker) or for development purposes, install the dependencies:

```bash
pip install -r requirements.txt
```

## 6. Running the Agent

Once all services are up and configured, you can run the agent. If running via Docker Compose, the `agent` service will automatically start.

Если запускаете напрямую:

```bash
python -m src.main
```

(Примечание: `src/main.py` будет создан на более позднем этапе и станет точкой входа (entry point) для агента.)

### 6.1. Использование FlowiseAPIClient (Using FlowiseAPIClient)

Ваш Python-агент будет использовать `src/flowise_integration/flowise_api_client.py` для взаимодействия с Flowise. Убедитесь, что переменные окружения `FLOWISE_API_URL` и `FLOWISE_API_KEY` корректно установлены в вашем файле `.env`.

