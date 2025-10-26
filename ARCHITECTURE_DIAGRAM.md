# TalentFlow Agent - Architecture Diagram

## System Architecture Overview

```mermaid
graph TD
    subgraph "Job Platforms"
        Djinni["Djinni.co"]
        LinkedIn["LinkedIn"]
    end
    
    subgraph "Parsing Layer"
        ParsingScheduler["Parsing Scheduler<br/>5-min intervals"]
        DjinniParser["Djinni Parser"]
        LinkedInParser["LinkedIn Parser"]
    end
    
    subgraph "Core Agent Services"
        VacancyAnalyzer["Vacancy Analyzer<br/>NLP-based"]
        AIPlatform["AI Platform<br/>LLM Orchestration"]
        VectorDB["Vector DB<br/>(Supabase/Pinecone)"]
        CacheManager["Cache Manager<br/>(Redis/Kafka)"]
        LeadManager["Lead Manager<br/>(CRM-like)"]
        
        VacancyDB["Vacancy DB<br/>(PostgreSQL)"]
        
        AIPlatform --> VectorDB
        AIPlatform --> CacheManager
    end
    
    subgraph "Lead Generation & Interaction"
        ResponseGenerator["Response Generator<br/>Personalized Proposals"]
        ResponseSender["Response Sender"]
        MeetingScheduler["Meeting Scheduler<br/>Calendly/Crea"]
        NotificationService["Notification Service"]
    end
    
    subgraph "Profiles & Configuration"
        ProfileData["4 Target Profiles<br/>(A/B Testing)"]
        Config["Configuration (YAML)"]
    end
    
    subgraph "External Services"
        Calendly["Calendly API"]
        OpenAI["OpenAI/LLM API"]
        Slack["Slack API"]
    end
    
    %% Connections
    ParsingScheduler --> DjinniParser
    ParsingScheduler --> LinkedInParser
    DjinniParser --> VacancyDB
    LinkedInParser --> VacancyDB
    
    VacancyDB --> VacancyAnalyzer
    ProfileData --> VacancyAnalyzer
    
    VacancyAnalyzer --> AIPlatform
    AIPlatform --> OpenAI
    
    AIPlatform --> ResponseGenerator
    
    ResponseGenerator --> ResponseSender
    ResponseSender --> LeadManager
    LeadManager --> NotificationService
    LeadManager --> MeetingScheduler
    
    MeetingScheduler --> Calendly
    
    NotificationService --> Slack
    
    CacheManager --> VacancyAnalyzer
    CacheManager --> AIPlatform
    
    style AIPlatform fill:#fff3e0
    style VectorDB fill:#e6ee9c
    style CacheManager fill:#ffcc80
    style ProfileData fill:#bbdefb
    
    %% Data Flow
    VacancyAnalyzer --> VectorDB
    VectorDB --> VacancyAnalyzer
    
    %% Orchestration Flow
    LeadManager --> LeadManager
    
```

## Data Flow Sequence (Lead Processing)

```mermaid
sequenceDiagram
    participant Scheduler as Parsing Scheduler
    participant Parser as Job Parser
    participant VacancyDB as Vacancy DB
    participant Analyzer as Vacancy Analyzer
    participant VectorDB as Vector DB
    participant AIPlatform as AI Platform
    participant LeadManager as Lead Manager
    participant Sender as Response Sender
    participant Recruiter as Recruiter Platform
    
    Scheduler->>Parser: Fetch new vacancies
    Parser->>VacancyDB: Save new vacancies
    
    loop New Vacancies
        Analyzer->>VacancyDB: Get new vacancy
        Analyzer->>VectorDB: Find top 2 relevant portfolio projects (RAG)
        Analyzer->>AIPlatform: Send Vacancy + Profile Data + Projects (Prompt)
        
        AIPlatform->>AIPlatform: Analyze & Generate Response (LLM Chain)
        
        AIPlatform->>Analyzer: Return Response & Analysis
        
        LeadManager->>LeadManager: Create Lead Record
        LeadManager->>Sender: Send Response
        Sender->>Recruiter: Send Personalized Proposal
        
        LeadManager->>LeadManager: Update Status: Sent
    end
    
    Recruiter->>LeadManager: Recruiter Reply/Meeting Request
    LeadManager->>LeadManager: Update Status: Engaged
    LeadManager->>Maxim: Notify Maxim (Lead Handoff)
```

## Component Details

### 1. Core Agent Services

- **Vacancy Analyzer**: Uses NLP to extract requirements, responsibilities, and KPIs. **Now uses VectorDB for RAG.**
- **AI Platform (Orchestration)**: Central platform for creating and managing LLM chains (chatflows). **Replaces explicit mention of Flowise.**
- **Vector DB (Supabase/Pinecone)**: Stores vectorized portfolio projects and vacancy data for **Retrieval-Augmented Generation (RAG)**.
- **Cache Manager (Redis/Kafka)**: Caches expensive LLM responses and parsing results to reduce costs and latency.
- **Lead Manager (CRM-like)**: Creates, tracks, and manages the status of all leads and interaction history.

### 2. Profiles & Configuration

- **4 Target Profiles**: Separate Git branches (`profile-swe-focused`, etc.) with unique `profile_data.json` for A/B testing and precise targeting.
- **Configuration (YAML)**: Centralized configuration for all API keys, search parameters, and chatflow IDs.

### 3. Lead Generation & Interaction

- **Response Generator**: Creates highly personalized proposals by integrating analysis from the AI Platform and relevant portfolio projects from the Vector DB.
- **Response Sender**: Handles the technical sending of the personalized response to the job platform.
- **Meeting Scheduler**: Integrates with Calendly API for automated scheduling of the "hand-off" call with Maxim.
- **Notification Service**: Alerts Maxim via Slack/Email upon lead generation or recruiter engagement.

### 4. Scalability & Optimization

- **RAG (Retrieval-Augmented Generation)**: Implemented via Vector DB to ensure responses are grounded in the user's actual portfolio data.
- **Caching**: Reduces reliance on external APIs and speeds up the process.
- **A/B Testing**: Enabled by the 4 distinct Git branches/profiles.
- **Future: Message Brokers (Kafka/RabbitMQ)**: Planned for high-volume scaling.

