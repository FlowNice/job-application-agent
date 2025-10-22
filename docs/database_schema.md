# Схема базы данных (Database Schema)

## 1. Обзор (Overview)

Этот документ описывает структуру базы данных (database structure) для агента автоматического отклика на вакансии. База данных хранит информацию о вакансиях (vacancies), лидах (leads), взаимодействиях (interactions) и истории действий (action history).

## 2. Таблицы (Tables)

### 2.1. Таблица `vacancies` - Вакансии

Хранит информацию о спарсенных вакансиях (parsed vacancies).

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | INTEGER PRIMARY KEY | Уникальный идентификатор (Unique identifier) |
| `title` | VARCHAR(255) | Название вакансии (Job title) |
| `company` | VARCHAR(255) | Название компании (Company name) |
| `description` | TEXT | Описание вакансии (Job description) |
| `requirements` | TEXT | Требования (Requirements) |
| `salary_min` | INTEGER | Минимальная зарплата (Minimum salary) |
| `salary_max` | INTEGER | Максимальная зарплата (Maximum salary) |
| `currency` | VARCHAR(10) | Валюта (Currency) - USD, EUR, UAH |
| `location` | VARCHAR(255) | Локация (Location) |
| `job_type` | VARCHAR(50) | Тип занятости (Job type) - Full-time, Part-time |
| `experience_level` | VARCHAR(50) | Уровень опыта (Experience level) - Junior, Middle, Senior |
| `recruiter_name` | VARCHAR(255) | Имя рекрутера (Recruiter name) |
| `recruiter_email` | VARCHAR(255) | Email рекрутера (Recruiter email) |
| `recruiter_phone` | VARCHAR(20) | Телефон рекрутера (Recruiter phone) |
| `vacancy_url` | VARCHAR(500) | URL вакансии (Vacancy URL) |
| `source_platform` | VARCHAR(50) | Источник (Source platform) - djinni, linkedin |
| `posted_date` | TIMESTAMP | Дата публикации (Posted date) |
| `parsed_at` | TIMESTAMP | Дата парсинга (Parsed date) |
| `created_at` | TIMESTAMP | Дата создания записи (Created at) |

### 2.2. Таблица `leads` - Лиды

Хранит информацию о потенциальных клиентах (potential clients/leads).

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | INTEGER PRIMARY KEY | Уникальный идентификатор (Unique identifier) |
| `lead_id` | VARCHAR(50) UNIQUE | Уникальный ID лида (Lead ID) - LEAD_YYYYMMDDHHMMSS_XXXX |
| `vacancy_id` | INTEGER FOREIGN KEY | Ссылка на вакансию (Reference to vacancy) |
| `company` | VARCHAR(255) | Название компании (Company name) |
| `position` | VARCHAR(255) | Должность (Position) |
| `recruiter_name` | VARCHAR(255) | Имя рекрутера (Recruiter name) |
| `recruiter_email` | VARCHAR(255) | Email рекрутера (Recruiter email) |
| `recruiter_phone` | VARCHAR(20) | Телефон рекрутера (Recruiter phone) |
| `generated_response` | TEXT | Сгенерированный ответ (Generated response) |
| `status` | VARCHAR(50) | Статус лида (Lead status) - pending, sent, responded, qualified, closed |
| `created_at` | TIMESTAMP | Дата создания (Created at) |
| `sent_at` | TIMESTAMP | Дата отправки ответа (Sent at) |
| `response_received_at` | TIMESTAMP | Дата получения ответа (Response received at) |
| `meeting_scheduled` | BOOLEAN | Встреча запланирована? (Meeting scheduled?) |
| `meeting_url` | VARCHAR(500) | URL встречи (Meeting URL) |
| `notes` | TEXT | Заметки (Notes) |

### 2.3. Таблица `interactions` - Взаимодействия

Хранит историю взаимодействия с рекрутерами (interaction history with recruiters).

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | INTEGER PRIMARY KEY | Уникальный идентификатор (Unique identifier) |
| `lead_id` | INTEGER FOREIGN KEY | Ссылка на лид (Reference to lead) |
| `interaction_type` | VARCHAR(50) | Тип взаимодействия (Interaction type) - email_sent, response_received, meeting_scheduled, call_made |
| `message` | TEXT | Сообщение (Message) |
| `direction` | VARCHAR(20) | Направление (Direction) - outbound, inbound |
| `created_at` | TIMESTAMP | Дата взаимодействия (Interaction date) |

### 2.4. Таблица `analysis_results` - Результаты анализа

Хранит результаты анализа вакансий (vacancy analysis results).

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | INTEGER PRIMARY KEY | Уникальный идентификатор (Unique identifier) |
| `vacancy_id` | INTEGER FOREIGN KEY | Ссылка на вакансию (Reference to vacancy) |
| `key_responsibilities` | TEXT | Ключевые обязанности (Key responsibilities) - JSON |
| `technical_requirements` | TEXT | Технические требования (Technical requirements) - JSON |
| `kpis` | TEXT | KPI и метрики (KPIs and metrics) - JSON |
| `seniority_level` | VARCHAR(50) | Уровень опыта (Seniority level) |
| `created_at` | TIMESTAMP | Дата анализа (Analysis date) |

### 2.5. Таблица `agent_logs` - Логи агента

Хранит логи действий агента (agent action logs).

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | INTEGER PRIMARY KEY | Уникальный идентификатор (Unique identifier) |
| `action_type` | VARCHAR(100) | Тип действия (Action type) - vacancy_parsed, lead_created, response_sent |
| `description` | TEXT | Описание (Description) |
| `status` | VARCHAR(50) | Статус (Status) - success, error, warning |
| `error_message` | TEXT | Сообщение об ошибке (Error message) |
| `created_at` | TIMESTAMP | Дата действия (Action date) |

## 3. Связи между таблицами (Relationships)

```
vacancies (1) ---- (N) leads
vacancies (1) ---- (N) analysis_results
leads (1) ---- (N) interactions
```

## 4. Индексы (Indexes)

Для оптимизации производительности (performance optimization) рекомендуется создать индексы на следующих полях:

```sql
-- Индексы для быстрого поиска (Indexes for fast lookup)
CREATE INDEX idx_vacancies_source_platform ON vacancies(source_platform);
CREATE INDEX idx_vacancies_posted_date ON vacancies(posted_date);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created_at ON leads(created_at);
CREATE INDEX idx_interactions_lead_id ON interactions(lead_id);
CREATE INDEX idx_agent_logs_action_type ON agent_logs(action_type);
```

## 5. Примеры запросов (Query Examples)

### 5.1. Получить все активные лиды (Get all active leads)

```sql
SELECT * FROM leads 
WHERE status IN ('pending', 'sent', 'responded') 
ORDER BY created_at DESC;
```

### 5.2. Получить статистику по вакансиям (Get vacancy statistics)

```sql
SELECT 
    source_platform,
    experience_level,
    COUNT(*) as total_vacancies,
    COUNT(DISTINCT company) as unique_companies
FROM vacancies
WHERE parsed_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY source_platform, experience_level;
```

### 5.3. Получить историю взаимодействия с лидом (Get interaction history for a lead)

```sql
SELECT 
    l.lead_id,
    l.company,
    l.recruiter_name,
    i.interaction_type,
    i.message,
    i.created_at
FROM leads l
LEFT JOIN interactions i ON l.id = i.lead_id
WHERE l.id = ?
ORDER BY i.created_at DESC;
```

## 6. Заключение (Conclusion)

Эта схема базы данных обеспечивает полное отслеживание вакансий, лидов и взаимодействий. При необходимости она может быть расширена дополнительными таблицами для хранения информации о клиентах (customers), проектах (projects) и доходах (revenue).

