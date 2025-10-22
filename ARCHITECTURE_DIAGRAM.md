# Job Application Agent - Architecture Diagram

## System Architecture Overview

```mermaid
graph TB
    subgraph "Job Platforms"
        Djinni["Djinni.co"]
        LinkedIn["LinkedIn"]
    end
    
    subgraph "Parsing Layer"
        DjinniParser["Djinni Parser"]
        LinkedInParser["LinkedIn Parser"]
        ParsingScheduler["Parsing Scheduler<br/>5-min intervals"]
    end
    
    subgraph "Analysis & Processing"
        VacancyAnalyzer["Vacancy Analyzer<br/>NLP-based"]
        FloWise["Flowise<br/>LLM Orchestration"]
        ResponseGenerator["Response Generator<br/>Personalized Proposals"]
    end
    
    subgraph "Lead Management"
        LeadGenerator["Lead Generator"]
        LeadDB["Lead Database"]
        StatusTracker["Status Tracker"]
    end
    
    subgraph "Recruiter Interaction"
        ResponseSender["Response Sender"]
        MeetingScheduler["Meeting Scheduler<br/>Calendly/Crea"]
        NotificationService["Notification Service"]
    end
    
    subgraph "Notification Channels"
        MaximEmail["Email to Maxim"]
        MaximSlack["Slack Notification"]
        MaximSMS["SMS Notification"]
    end
    
    subgraph "External Services"
        Calendly["Calendly API"]
        Crea["Crea API"]
        OpenAI["OpenAI/LLM API"]
    end
    
    subgraph "Storage"
        VacancyDB["Vacancy Database"]
        ConfigDB["Configuration DB"]
        LogsStorage["Logs & Metrics"]
    end
    
    %% Parsing connections
    Djinni --> DjinniParser
    LinkedIn --> LinkedInParser
    ParsingScheduler --> DjinniParser
    ParsingScheduler --> LinkedInParser
    
    %% Data flow
    DjinniParser --> VacancyDB
    LinkedInParser --> VacancyDB
    
    VacancyDB --> VacancyAnalyzer
    VacancyAnalyzer --> FloWise
    FloWise --> OpenAI
    FloWise --> ResponseGenerator
    
    ResponseGenerator --> LeadGenerator
    LeadGenerator --> LeadDB
    LeadDB --> StatusTracker
    
    %% Recruiter interaction
    LeadGenerator --> ResponseSender
    ResponseSender --> Djinni
    ResponseSender --> LinkedIn
    
    LeadGenerator --> MeetingScheduler
    MeetingScheduler --> Calendly
    MeetingScheduler --> Crea
    
    %% Notifications
    LeadGenerator --> NotificationService
    NotificationService --> MaximEmail
    NotificationService --> MaximSlack
    NotificationService --> MaximSMS
    
    %% Logging
    VacancyAnalyzer --> LogsStorage
    LeadGenerator --> LogsStorage
    ResponseSender --> LogsStorage
    
    style Djinni fill:#e1f5ff
    style LinkedIn fill:#e1f5ff
    style FloWise fill:#fff3e0
    style OpenAI fill:#fff3e0
    style Calendly fill:#f3e5f5
    style Crea fill:#f3e5f5
```

## Data Flow Sequence

```mermaid
sequenceDiagram
    participant Scheduler as Parsing Scheduler
    participant Parser as Job Parser
    participant Analyzer as Vacancy Analyzer
    participant Flowise as Flowise/LLM
    participant LeadGen as Lead Generator
    participant Recruiter as Recruiter Platform
    participant Maxim as Maxim (Notification)
    
    Scheduler->>Parser: Fetch new vacancies
    Parser->>Parser: Extract job details
    Parser->>Analyzer: Send vacancy data
    
    Analyzer->>Analyzer: Extract requirements & KPIs
    Analyzer->>Flowise: Analyze vacancy & generate response
    Flowise->>Flowise: Process with LLM
    Flowise->>Analyzer: Return generated response
    
    Analyzer->>LeadGen: Create lead record
    LeadGen->>LeadGen: Prepare recruiter message
    LeadGen->>Recruiter: Send response + meeting link
    
    LeadGen->>Maxim: Notify about new lead
    Maxim->>Recruiter: Follow up (manual)
    Recruiter->>Maxim: Respond to proposal
    
    Maxim->>LeadGen: Update lead status
    LeadGen->>LeadGen: Track interaction
```

## Component Details

### 1. Parsing Layer
- **Djinni Parser**: Scrapes vacancies from Djinni.co using BeautifulSoup/Selenium
- **LinkedIn Parser**: Integrates with LinkedIn API or uses authorized scraping
- **Parsing Scheduler**: Runs every 5 minutes to check for new vacancies

### 2. Analysis & Processing
- **Vacancy Analyzer**: Uses NLP to extract requirements, responsibilities, and KPIs
- **Flowise**: Visual LLM orchestration platform for creating intelligent chains
- **Response Generator**: Creates personalized proposals based on analysis

### 3. Lead Management
- **Lead Generator**: Creates and manages lead records
- **Lead Database**: Stores all lead information and history
- **Status Tracker**: Monitors lead progression through the pipeline

### 4. Recruiter Interaction
- **Response Sender**: Sends generated responses to recruiters
- **Meeting Scheduler**: Integrates with Calendly/Crea for automatic scheduling
- **Notification Service**: Alerts Maxim about new leads via multiple channels

### 5. Storage & Logging
- **Vacancy Database**: Stores parsed job vacancies
- **Configuration Database**: Manages agent settings and preferences
- **Logs & Metrics**: Tracks all actions for monitoring and optimization

## Integration Points

### External APIs
- **OpenAI API**: For LLM-based analysis and response generation
- **Calendly API**: For meeting scheduling
- **Crea API**: Alternative meeting scheduling platform
- **Slack API**: For notifications to Maxim
- **Email Service**: SMTP for email notifications

### Flowise Integration
Flowise serves as the central orchestration platform for:
- Creating reusable LLM chains for vacancy analysis
- Building self-learning agents that improve over time
- Managing complex workflows with multiple AI steps
- Providing a visual interface for non-technical configuration

## Scalability Considerations

1. **Horizontal Scaling**: Multiple parser instances can run in parallel
2. **Caching**: Redis can cache frequently accessed data
3. **Database Optimization**: PostgreSQL for production deployment
4. **Async Processing**: Use APScheduler for non-blocking operations
5. **Load Balancing**: FastAPI with multiple workers for API endpoints

## Security Considerations

1. **API Keys**: Stored in environment variables, not in code
2. **Database**: Encrypted connections with PostgreSQL
3. **Authentication**: Flowise authentication for API access
4. **Rate Limiting**: Respect platform rate limits and robots.txt
5. **Data Privacy**: Secure storage of recruiter contact information

