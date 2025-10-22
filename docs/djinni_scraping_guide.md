# Руководство по парсингу Djinni.co (Djinni.co Scraping Guide)

## 1. Введение (Introduction)

Этот документ описывает процесс парсинга (scraping) вакансий с сайта Djinni.co. Djinni.co - это популярная платформа для поиска IT-вакансий в Украине и других странах. Поскольку официального публичного API нет, мы используем веб-скрейпинг (web scraping) с помощью библиотек `requests` и `BeautifulSoup`.

## 2. Структура HTML Djinni.co (HTML Structure)

### 2.1. Главная страница поиска (Search Results Page)

Страница поиска вакансий находится по адресу: `https://djinni.co/jobs/`

**Параметры URL (URL Parameters):**
*   `q` - поисковый запрос (search query), например: `https://djinni.co/jobs/?q=Python`
*   `experience_level` - уровень опыта (experience level): `junior`, `middle`, `senior`
*   `location` - локация (location), например: `kyiv`, `lviv`, `remote`

**Пример поискового URL:**
```
https://djinni.co/jobs/?q=Python&experience_level=middle&location=remote
```

### 2.2. Селекторы для извлечения данных (CSS Selectors for Data Extraction)

Основные CSS-селекторы (CSS selectors) для извлечения информации о вакансиях:

| Элемент | Селектор | Описание |
|---------|----------|---------|
| Контейнер вакансии | `div.job-list-item` | Основной контейнер для каждой вакансии |
| Название вакансии | `a.job-list-item__link` | Ссылка на вакансию с названием |
| Компания | `div.text-muted` | Название компании |
| Дата публикации | `div.text-date` | Когда была опубликована вакансия |
| Локация | `span.location` | Место работы |
| Зарплата | `span.salary` | Размер зарплаты (если указана) |

**Примечание:** Селекторы могут измениться, если Djinni.co обновит свой HTML-код. В таком случае необходимо обновить селекторы в коде парсера.

## 3. Процесс парсинга (Scraping Process)

### 3.1. Шаг 1: Получение HTML-страницы (Fetch HTML Page)

```python
import requests
from bs4 import BeautifulSoup

url = "https://djinni.co/jobs/?q=Python&experience_level=middle"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Проверить наличие ошибок HTTP (Check for HTTP errors)
```

### 3.2. Шаг 2: Парсинг HTML (Parse HTML)

```python
soup = BeautifulSoup(response.text, 'html.parser')
job_cards = soup.find_all('div', class_='job-list-item')
```

### 3.3. Шаг 3: Извлечение данных из каждой вакансии (Extract Data from Each Vacancy)

```python
vacancies = []

for card in job_cards:
    # Название вакансии (Job title)
    title_tag = card.find('a', class_='job-list-item__link')
    title = title_tag.text.strip() if title_tag else None
    
    # URL вакансии (Vacancy URL)
    vacancy_url = "https://djinni.co" + title_tag['href'] if title_tag else None
    
    # Компания (Company)
    company_tag = card.find('div', class_='text-muted')
    company = company_tag.text.strip() if company_tag else None
    
    # Дата публикации (Posted date)
    date_tag = card.find('div', class_='text-date')
    posted_date = date_tag.text.strip() if date_tag else None
    
    vacancy = {
        'title': title,
        'company': company,
        'vacancy_url': vacancy_url,
        'posted_date': posted_date
    }
    
    vacancies.append(vacancy)
```

## 4. Обработка ошибок (Error Handling)

### 4.1. Сетевые ошибки (Network Errors)

```python
import requests

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.ConnectionError:
    print("Ошибка подключения (Connection error)")
except requests.exceptions.Timeout:
    print("Время ожидания истекло (Timeout)")
except requests.exceptions.HTTPError as e:
    print(f"HTTP ошибка: {e}")
```

### 4.2. Парсинг ошибок (Parsing Errors)

```python
try:
    soup = BeautifulSoup(response.text, 'html.parser')
    job_cards = soup.find_all('div', class_='job-list-item')
except Exception as e:
    print(f"Ошибка парсинга: {e}")
```

## 5. Лучшие практики (Best Practices)

### 5.1. Уважение к серверу (Respect the Server)
*   **Задержки между запросами (Delays between requests)**: Добавить задержку (delay) между запросами, чтобы не перегружать сервер.
    ```python
    import time
    time.sleep(2)  # Ждать 2 секунды (Wait 2 seconds)
    ```

### 5.2. User-Agent (User-Agent Header)
*   Всегда указывать `User-Agent` в заголовках (headers), чтобы выглядеть как обычный браузер (browser).

### 5.3. Обработка динамического контента (Dynamic Content)
*   Если Djinni.co использует JavaScript для загрузки контента, может потребоваться использовать `Selenium` или `Playwright` вместо простого `requests`.

### 5.4. Логирование (Logging)
*   Логировать все действия парсера для отладки (debugging) и мониторинга (monitoring).

## 6. Примеры использования (Usage Examples)

### 6.1. Парсинг вакансий Python разработчиков (Parse Python Developer Vacancies)

```python
from src.parsers import DjinniParser

parser = DjinniParser()
vacancies = parser.fetch_vacancies(
    keywords=['Python', 'Django'],
    limit=10
)

for vacancy in vacancies:
    print(f"Title: {vacancy['title']}")
    print(f"Company: {vacancy['company']}")
    print(f"URL: {vacancy['vacancy_url']}")
    print("---")
```

### 6.2. Фильтрация вакансий (Filter Vacancies)

```python
filtered = parser.filter_vacancies(
    vacancies,
    keywords=['Python', 'FastAPI'],
    locations=['Remote', 'Kyiv']
)
```

## 7. Решение проблем (Troubleshooting)

| Проблема | Решение |
|----------|---------|
| Селекторы не работают | Проверить HTML-структуру сайта в DevTools (F12) |
| Сервер блокирует запросы | Добавить задержки, использовать прокси (proxy), изменить User-Agent |
| Динамический контент не загружается | Использовать Selenium или Playwright вместо requests |
| Кодировка текста неправильная | Убедиться, что используется `encoding='utf-8'` |

## 8. Заключение (Conclusion)

Парсинг Djinni.co требует внимательного подхода к структуре HTML и соблюдению лучших практик. При изменении структуры сайта селекторы необходимо обновлять.

