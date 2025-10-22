-- Инициализация базы данных (Database Initialization Script)
-- Создание таблиц для агента автоматического отклика на вакансии

-- Таблица вакансий (Vacancies table)
CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    description LONGTEXT,
    requirements LONGTEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    currency VARCHAR(10) DEFAULT 'USD',
    location VARCHAR(255),
    job_type VARCHAR(50),
    experience_level VARCHAR(50),
    recruiter_name VARCHAR(255),
    recruiter_email VARCHAR(255),
    recruiter_phone VARCHAR(20),
    vacancy_url VARCHAR(500) UNIQUE,
    source_platform VARCHAR(50) NOT NULL,
    posted_date TIMESTAMP,
    parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_source_platform (source_platform),
    INDEX idx_posted_date (posted_date),
    INDEX idx_experience_level (experience_level)
);

-- Таблица лидов (Leads table)
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    lead_id VARCHAR(50) UNIQUE NOT NULL,
    vacancy_id INTEGER NOT NULL,
    company VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    recruiter_name VARCHAR(255),
    recruiter_email VARCHAR(255),
    recruiter_phone VARCHAR(20),
    generated_response LONGTEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP NULL,
    response_received_at TIMESTAMP NULL,
    meeting_scheduled BOOLEAN DEFAULT FALSE,
    meeting_url VARCHAR(500),
    notes LONGTEXT,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_lead_id (lead_id)
);

-- Таблица взаимодействий (Interactions table)
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    lead_id INTEGER NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,
    message LONGTEXT,
    direction VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    INDEX idx_lead_id (lead_id),
    INDEX idx_interaction_type (interaction_type),
    INDEX idx_created_at (created_at)
);

-- Таблица результатов анализа (Analysis Results table)
CREATE TABLE IF NOT EXISTS analysis_results (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    vacancy_id INTEGER NOT NULL,
    key_responsibilities JSON,
    technical_requirements JSON,
    kpis JSON,
    seniority_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vacancy_id) REFERENCES vacancies(id),
    INDEX idx_vacancy_id (vacancy_id)
);

-- Таблица логов агента (Agent Logs table)
CREATE TABLE IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    action_type VARCHAR(100) NOT NULL,
    description LONGTEXT,
    status VARCHAR(50),
    error_message LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_action_type (action_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Таблица конфигурации (Configuration table) - для хранения настроек
CREATE TABLE IF NOT EXISTS configuration (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    key_name VARCHAR(255) UNIQUE NOT NULL,
    value LONGTEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_key_name (key_name)
);

-- Таблица статистики (Statistics table) - для отслеживания метрик
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    metric_name VARCHAR(100) NOT NULL,
    metric_value INTEGER DEFAULT 0,
    metric_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_metric (metric_name, metric_date),
    INDEX idx_metric_date (metric_date)
);

-- Создание индексов для оптимизации (Create indexes for optimization)
CREATE INDEX IF NOT EXISTS idx_vacancies_company ON vacancies(company);
CREATE INDEX IF NOT EXISTS idx_leads_vacancy_id ON leads(vacancy_id);
CREATE INDEX IF NOT EXISTS idx_interactions_created_at ON interactions(created_at);

-- Вставка начальной конфигурации (Insert initial configuration)
INSERT IGNORE INTO configuration (key_name, value, description) VALUES
('last_scan_time', '2024-01-01 00:00:00', 'Время последнего сканирования вакансий (Last vacancy scan time)'),
('total_vacancies_parsed', '0', 'Общее количество спарсенных вакансий (Total vacancies parsed)'),
('total_leads_generated', '0', 'Общее количество сгенерированных лидов (Total leads generated)'),
('total_responses_sent', '0', 'Общее количество отправленных ответов (Total responses sent)');

-- Вставка начальной статистики (Insert initial statistics)
INSERT IGNORE INTO statistics (metric_name, metric_value, metric_date) VALUES
('vacancies_parsed_today', 0, CURDATE()),
('leads_generated_today', 0, CURDATE()),
('responses_sent_today', 0, CURDATE());

-- Подтверждение создания таблиц (Confirmation message)
SELECT 'Database initialization completed successfully!' as status;

