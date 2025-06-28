# Multi-Agent Travel Planning System - Mermaid Architecture Diagram

## 🔄 Complete System Workflow

```mermaid
graph TB
    %% User Interface Layer
    subgraph "User Interface Layer"
        UI[Streamlit Web App<br/>localhost:8501]
        USER[👤 User]
    end

    %% Orchestration Layer
    subgraph "Orchestration Layer"
        TP[Travel Planner Agent<br/>Google ADK<br/>localhost:10001<br/>Groq Llama-3 70B]
    end

    %% Agent Layer
    subgraph "Specialist Agents Layer"
        HA[Hotel Booking Agent<br/>CrewAI<br/>localhost:10002<br/>Groq Llama-3 70B]
        CA[Car Rental Agent<br/>LangGraph<br/>localhost:10003<br/>Groq Llama-3 70B]
    end

    %% External Services Layer
    subgraph "External Services Layer"
        SERPER[SerperAPI<br/>Real-time Web Search]
        GROQ[Groq API<br/>LLM Inference]
    end

    %% User Input Flow
    USER -->|"Travel Request<br/>(Destination, Dates, Budget)"| UI
    
    %% Request Processing
    UI -->|"1. Validate & Format Request"| TP
    
    %% Agent Discovery
    TP -->|"2. Health Check"| HA
    TP -->|"2. Health Check"| CA
    HA -->|"✅ Available"| TP
    CA -->|"✅ Available"| TP
    
    %% Parallel Agent Execution
    TP -->|"3a. Hotel Query<br/>'Find budget hotels in Paris'"| HA
    TP -->|"3b. Car Rental Query<br/>'Find car rentals in Paris'"| CA
    
    %% Agent Tool Execution
    HA -->|"4a. Hotel Search Tool"| SERPER
    CA -->|"4b. Car Rental Search Tool"| SERPER
    SERPER -->|"Search Results"| HA
    SERPER -->|"Search Results"| CA
    
    %% LLM Processing
    HA -->|"5a. Process with LLM"| GROQ
    CA -->|"5b. Process with LLM"| GROQ
    GROQ -->|"Structured Recommendations"| HA
    GROQ -->|"Structured Recommendations"| CA
    
    %% Response Collection
    HA -->|"6a. Hotel Recommendations"| TP
    CA -->|"6b. Car Rental Options"| TP
    
    %% Final Plan Generation
    TP -->|"7. Generate Comprehensive Plan"| GROQ
    GROQ -->|"Final Travel Plan"| TP
    
    %% Response Delivery
    TP -->|"8. Complete Travel Plan"| UI
    UI -->|"Display Results"| USER

    %% Styling
    classDef userLayer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef orchestrationLayer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef agentLayer fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef serviceLayer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    class UI,USER userLayer
    class TP orchestrationLayer
    class HA,CA agentLayer
    class SERPER,GROQ serviceLayer
```

## 🔍 Detailed Agent Communication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit App
    participant TP as Travel Planner
    participant HA as Hotel Agent
    participant CA as Car Rental Agent
    participant S as SerperAPI
    participant G as Groq API

    U->>UI: Enter travel details
    UI->>TP: Send formatted request
    
    Note over TP: Phase 1: Agent Discovery
    TP->>HA: GET /health
    HA-->>TP: 200 OK
    TP->>CA: GET /health
    CA-->>TP: 200 OK
    
    Note over TP: Phase 2: Parallel Execution
    par Hotel Search
        TP->>HA: POST /chat (hotel query)
        HA->>S: Search hotels
        S-->>HA: Hotel results
        HA->>G: Process with LLM
        G-->>HA: Structured recommendations
        HA-->>TP: Hotel recommendations
    and Car Rental Search
        TP->>CA: POST /chat (car rental query)
        CA->>S: Search car rentals
        S-->>CA: Car rental results
        CA->>G: Process with LLM
        G-->>CA: Structured recommendations
        CA-->>TP: Car rental options
    end
    
    Note over TP: Phase 3: Plan Generation
    TP->>G: Generate comprehensive plan
    G-->>TP: Final travel plan
    TP-->>UI: Complete response
    UI-->>U: Display travel plan
```

## 🏗️ System Architecture Overview

```mermaid
graph LR
    subgraph "Frontend Layer"
        STREAMLIT[Streamlit Web App]
    end
    
    subgraph "API Gateway Layer"
        GATEWAY[API Gateway<br/>Load Balancer]
    end
    
    subgraph "Orchestration Layer"
        TP1[Travel Planner 1]
        TP2[Travel Planner 2]
        TP3[Travel Planner N]
    end
    
    subgraph "Agent Layer"
        HA1[Hotel Agent 1]
        HA2[Hotel Agent 2]
        CA1[Car Agent 1]
        CA2[Car Agent 2]
    end
    
    subgraph "External Services"
        SERPER[SerperAPI]
        GROQ[Groq API]
    end
    
    subgraph "Data Layer"
        CACHE[Redis Cache]
        DB[(PostgreSQL)]
        LOGS[Logging System]
    end
    
    STREAMLIT --> GATEWAY
    GATEWAY --> TP1
    GATEWAY --> TP2
    GATEWAY --> TP3
    
    TP1 --> HA1
    TP1 --> CA1
    TP2 --> HA2
    TP2 --> CA2
    
    HA1 --> SERPER
    HA2 --> SERPER
    CA1 --> SERPER
    CA2 --> SERPER
    
    TP1 --> GROQ
    TP2 --> GROQ
    TP3 --> GROQ
    HA1 --> GROQ
    HA2 --> GROQ
    CA1 --> GROQ
    CA2 --> GROQ
    
    TP1 --> CACHE
    TP2 --> CACHE
    TP3 --> CACHE
    HA1 --> CACHE
    HA2 --> CACHE
    CA1 --> CACHE
    CA2 --> CACHE
    
    TP1 --> DB
    TP2 --> DB
    TP3 --> DB
    
    TP1 --> LOGS
    TP2 --> LOGS
    TP3 --> LOGS
    HA1 --> LOGS
    HA2 --> LOGS
    CA1 --> LOGS
    CA2 --> LOGS
```

## 🔄 Agent Internal Workflow

```mermaid
graph TD
    subgraph "Hotel Agent (CrewAI) Internal Flow"
        HA_IN[Input Query]
        HA_CREW[CrewAI Workflow]
        HA_TOOL[Hotel Search Tool]
        HA_LLM[LLM Processing]
        HA_OUT[Structured Output]
        
        HA_IN --> HA_CREW
        HA_CREW --> HA_TOOL
        HA_TOOL --> HA_LLM
        HA_LLM --> HA_OUT
    end
    
    subgraph "Car Rental Agent (LangGraph) Internal Flow"
        CA_IN[Input Query]
        CA_GRAPH[LangGraph State Machine]
        CA_TOOL[Car Rental Tool]
        CA_LLM[LLM Processing]
        CA_OUT[Structured Output]
        
        CA_IN --> CA_GRAPH
        CA_GRAPH --> CA_TOOL
        CA_TOOL --> CA_LLM
        CA_LLM --> CA_OUT
    end
    
    subgraph "Travel Planner (Google ADK) Internal Flow"
        TP_IN[User Request]
        TP_DISCOVER[Agent Discovery]
        TP_COORD[Coordinate Agents]
        TP_AGGREGATE[Aggregate Responses]
        TP_GENERATE[Generate Final Plan]
        TP_OUT[Complete Travel Plan]
        
        TP_IN --> TP_DISCOVER
        TP_DISCOVER --> TP_COORD
        TP_COORD --> TP_AGGREGATE
        TP_AGGREGATE --> TP_GENERATE
        TP_GENERATE --> TP_OUT
    end
```

## 📊 Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Input Data"
        USER_DATA[User Travel Preferences]
        AGENT_DATA[Agent Capabilities]
    end
    
    subgraph "Processing Pipeline"
        VALIDATION[Input Validation]
        DISCOVERY[Agent Discovery]
        EXECUTION[Parallel Execution]
        AGGREGATION[Response Aggregation]
        GENERATION[Plan Generation]
    end
    
    subgraph "Output Data"
        HOTEL_DATA[Hotel Recommendations]
        CAR_DATA[Car Rental Options]
        FINAL_PLAN[Comprehensive Travel Plan]
    end
    
    USER_DATA --> VALIDATION
    AGENT_DATA --> DISCOVERY
    
    VALIDATION --> DISCOVERY
    DISCOVERY --> EXECUTION
    EXECUTION --> AGGREGATION
    AGGREGATION --> GENERATION
    
    EXECUTION --> HOTEL_DATA
    EXECUTION --> CAR_DATA
    GENERATION --> FINAL_PLAN
```

## 🚨 Error Handling Flow

```mermaid
graph TD
    START[Request Received]
    START --> CHECK_AGENTS{Check Agent Health}
    
    CHECK_AGENTS -->|All Available| NORMAL_FLOW[Normal Execution Flow]
    CHECK_AGENTS -->|Some Unavailable| PARTIAL_FLOW[Partial Execution]
    CHECK_AGENTS -->|All Unavailable| ERROR_FLOW[Error Handling]
    
    NORMAL_FLOW --> SUCCESS[Success Response]
    PARTIAL_FLOW --> PARTIAL_SUCCESS[Partial Success Response]
    ERROR_FLOW --> ERROR_RESPONSE[Error Response]
    
    subgraph "Error Recovery"
        RETRY[Retry Logic]
        FALLBACK[Fallback Data]
        DEGRADED[Degraded Service]
    end
    
    ERROR_FLOW --> RETRY
    RETRY --> CHECK_AGENTS
    ERROR_FLOW --> FALLBACK
    FALLBACK --> DEGRADED
    DEGRADED --> PARTIAL_SUCCESS
```

## 📈 Performance Monitoring

```mermaid
graph LR
    subgraph "Metrics Collection"
        RESPONSE_TIME[Response Time]
        SUCCESS_RATE[Success Rate]
        AGENT_HEALTH[Agent Health]
        USER_SATISFACTION[User Satisfaction]
    end
    
    subgraph "Monitoring System"
        ALERTS[Alert System]
        DASHBOARD[Performance Dashboard]
        LOGS[Logging System]
    end
    
    subgraph "Optimization"
        CACHING[Caching Strategy]
        LOAD_BALANCING[Load Balancing]
        SCALING[Auto Scaling]
    end
    
    RESPONSE_TIME --> ALERTS
    SUCCESS_RATE --> DASHBOARD
    AGENT_HEALTH --> LOGS
    USER_SATISFACTION --> DASHBOARD
    
    ALERTS --> CACHING
    DASHBOARD --> LOAD_BALANCING
    LOGS --> SCALING
```

These diagrams provide a comprehensive view of the multi-agent travel planning system architecture, showing the complete workflow from user input to final response, including agent communication, error handling, and system monitoring. 