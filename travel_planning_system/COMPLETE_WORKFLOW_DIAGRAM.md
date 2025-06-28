# Complete Multi-Agent Travel Planning System - Mermaid Workflow Diagram

## 🔄 Complete System Workflow with Technical Details

```mermaid
graph TB
    %% User Interface Layer
    subgraph "User Interface Layer"
        UI[Streamlit Web App<br/>localhost:8501<br/>Python + Streamlit]
        USER[👤 User Input<br/>Destination, Dates, Budget, Guests]
    end

    %% Request Processing Layer
    subgraph "Request Processing Layer"
        VALIDATION[Input Validation<br/>Date Logic, Budget Range]
        FORMATTING[Request Formatting<br/>JSON Structure]
        INIT[Travel Planner Init<br/>Load Config, API Keys]
    end

    %% Agent Discovery Layer
    subgraph "Agent Discovery Layer"
        HEALTH_CHECK[Health Check<br/>HTTP GET /health]
        A2A_DISCOVERY[A2A Discovery<br/>GET /.well-known/agent.json]
        AGENT_STATUS[Agent Status<br/>Available/Unavailable]
    end

    %% Specialist Agents Layer
    subgraph "Hotel Agent (CrewAI)"
        HA_RECEIVE[Receive Query<br/>Hotel Search Request]
        HA_CREW[CrewAI Workflow<br/>Specialist Agent]
        HA_TOOL[Hotel Search Tool<br/>SerperAPI Integration]
        HA_LLM[LLM Processing<br/>Groq Llama-3 70B]
        HA_RESPONSE[Structured Response<br/>Hotel Recommendations]
    end

    subgraph "Car Rental Agent (LangGraph)"
        CA_RECEIVE[Receive Query<br/>Car Rental Request]
        CA_GRAPH[LangGraph Workflow<br/>State Machine]
        CA_TOOL[Car Rental Tool<br/>SerperAPI Integration]
        CA_LLM[LLM Processing<br/>Groq Llama-3 70B]
        CA_RESPONSE[Structured Response<br/>Car Rental Options]
    end

    %% External Services Layer
    subgraph "External Services"
        SERPER[SerperAPI<br/>Real-time Web Search<br/>Hotels & Car Rentals]
        GROQ[Groq API<br/>Llama-3 70B Versatile<br/>High-performance LLM]
    end

    %% Response Aggregation Layer
    subgraph "Response Aggregation"
        COLLECT[Parallel Response Collection<br/>Async HTTP Requests]
        PARSE[Response Parsing<br/>JSON Validation]
        INTEGRATE[Data Integration<br/>Merge Hotel & Car Data]
    end

    %% Plan Generation Layer
    subgraph "Final Plan Generation"
        PROMPT_CONSTRUCTION[Prompt Construction<br/>User Req + Agent Data]
        LLM_GENERATION[LLM Processing<br/>Comprehensive Plan]
        FORMATTING[Response Formatting<br/>Markdown Structure]
    end

    %% Response Delivery Layer
    subgraph "Response Delivery"
        UI_UPDATE[UI Update<br/>Display Results]
        DOWNLOAD[Download Option<br/>Markdown File]
        STATUS_DISPLAY[Agent Status Display<br/>Success/Failure]
    end

    %% User Input Flow
    USER -->|"1. Travel Details"| UI
    UI -->|"2. Validate Input"| VALIDATION
    VALIDATION -->|"3. Format Request"| FORMATTING
    FORMATTING -->|"4. Initialize Planner"| INIT

    %% Agent Discovery Flow
    INIT -->|"5. Check Agent Health"| HEALTH_CHECK
    HEALTH_CHECK -->|"6. Discover Capabilities"| A2A_DISCOVERY
    A2A_DISCOVERY -->|"7. Store Agent Status"| AGENT_STATUS

    %% Parallel Agent Execution
    AGENT_STATUS -->|"8a. Hotel Query"| HA_RECEIVE
    AGENT_STATUS -->|"8b. Car Rental Query"| CA_RECEIVE

    %% Hotel Agent Flow
    HA_RECEIVE -->|"9a. CrewAI Process"| HA_CREW
    HA_CREW -->|"10a. Execute Tool"| HA_TOOL
    HA_TOOL -->|"11a. Search Hotels"| SERPER
    SERPER -->|"12a. Hotel Results"| HA_TOOL
    HA_TOOL -->|"13a. Process with LLM"| HA_LLM
    HA_LLM -->|"14a. Generate Response"| HA_RESPONSE

    %% Car Rental Agent Flow
    CA_RECEIVE -->|"9b. LangGraph Process"| CA_GRAPH
    CA_GRAPH -->|"10b. Execute Tool"| CA_TOOL
    CA_TOOL -->|"11b. Search Car Rentals"| SERPER
    SERPER -->|"12b. Car Rental Results"| CA_TOOL
    CA_TOOL -->|"13b. Process with LLM"| CA_LLM
    CA_LLM -->|"14b. Generate Response"| CA_RESPONSE

    %% Response Collection
    HA_RESPONSE -->|"15a. Hotel Data"| COLLECT
    CA_RESPONSE -->|"15b. Car Rental Data"| COLLECT
    COLLECT -->|"16. Parse Responses"| PARSE
    PARSE -->|"17. Integrate Data"| INTEGRATE

    %% Final Plan Generation
    INTEGRATE -->|"18. Build Prompt"| PROMPT_CONSTRUCTION
    PROMPT_CONSTRUCTION -->|"19. Generate Plan"| LLM_GENERATION
    LLM_GENERATION -->|"20. Format Response"| FORMATTING

    %% Response Delivery
    FORMATTING -->|"21. Update UI"| UI_UPDATE
    UI_UPDATE -->|"22. Show Status"| STATUS_DISPLAY
    UI_UPDATE -->|"23. Enable Download"| DOWNLOAD

    %% Styling
    classDef userLayer fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef processingLayer fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef discoveryLayer fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef agentLayer fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef serviceLayer fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef aggregationLayer fill:#e0f2f1,stroke:#004d40,stroke-width:2px
    classDef generationLayer fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef deliveryLayer fill:#e8eaf6,stroke:#1a237e,stroke-width:2px

    class UI,USER userLayer
    class VALIDATION,FORMATTING,INIT processingLayer
    class HEALTH_CHECK,A2A_DISCOVERY,AGENT_STATUS discoveryLayer
    class HA_RECEIVE,HA_CREW,HA_TOOL,HA_LLM,HA_RESPONSE,CA_RECEIVE,CA_GRAPH,CA_TOOL,CA_LLM,CA_RESPONSE agentLayer
    class SERPER,GROQ serviceLayer
    class COLLECT,PARSE,INTEGRATE aggregationLayer
    class PROMPT_CONSTRUCTION,LLM_GENERATION,FORMATTING generationLayer
    class UI_UPDATE,DOWNLOAD,STATUS_DISPLAY deliveryLayer
```

## 🔍 Detailed Agent Communication Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit App
    participant TP as Travel Planner
    participant HA as Hotel Agent (CrewAI)
    participant CA as Car Rental Agent (LangGraph)
    participant S as SerperAPI
    participant G as Groq API

    Note over U,G: Phase 1: User Input & Validation
    U->>UI: Enter travel details
    UI->>UI: Validate input (dates, budget, guests)
    UI->>TP: POST /plan_travel (formatted request)

    Note over TP: Phase 2: Agent Discovery
    TP->>HA: GET /health
    HA-->>TP: 200 OK
    TP->>CA: GET /health
    CA-->>TP: 200 OK
    TP->>HA: GET /.well-known/agent.json
    HA-->>TP: Agent capabilities
    TP->>CA: GET /.well-known/agent.json
    CA-->>TP: Agent capabilities

    Note over TP: Phase 3: Parallel Agent Execution
    par Hotel Search Workflow
        TP->>HA: POST /chat (hotel query)
        HA->>HA: Initialize CrewAI workflow
        HA->>HA: Create Hotel Booking Specialist
        HA->>S: Search hotels (SerperAPI)
        S-->>HA: Hotel search results
        HA->>G: Process with Llama-3 70B
        G-->>HA: Structured hotel recommendations
        HA-->>TP: Hotel recommendations (JSON)
    and Car Rental Search Workflow
        TP->>CA: POST /chat (car rental query)
        CA->>CA: Initialize LangGraph workflow
        CA->>CA: Create React agent with tools
        CA->>S: Search car rentals (SerperAPI)
        S-->>CA: Car rental search results
        CA->>G: Process with Llama-3 70B
        G-->>CA: Structured car rental recommendations
        CA-->>TP: Car rental options (JSON)
    end

    Note over TP: Phase 4: Response Aggregation
    TP->>TP: Parse hotel response
    TP->>TP: Parse car rental response
    TP->>TP: Integrate data from both agents

    Note over TP: Phase 5: Final Plan Generation
    TP->>TP: Construct comprehensive prompt
    TP->>G: Generate final travel plan
    G-->>TP: Comprehensive travel plan
    TP->>TP: Format response with markdown

    Note over TP: Phase 6: Response Delivery
    TP-->>UI: Complete travel plan
    UI->>UI: Update interface
    UI-->>U: Display results with agent status
```

## 🏗️ System Architecture with Data Flow

```mermaid
graph LR
    subgraph "Frontend Layer"
        STREAMLIT[Streamlit Web App<br/>Port: 8501<br/>User Interface]
    end

    subgraph "Orchestration Layer"
        TRAVEL_PLANNER[Travel Planner Agent<br/>Google ADK<br/>Port: 10001<br/>Master Coordinator]
    end

    subgraph "Specialist Agents Layer"
        HOTEL_AGENT[Hotel Booking Agent<br/>CrewAI<br/>Port: 10002<br/>Hotel Specialist]
        CAR_AGENT[Car Rental Agent<br/>LangGraph<br/>Port: 10003<br/>Car Rental Specialist]
    end

    subgraph "External Services Layer"
        SERPER_API[SerperAPI<br/>Real-time Web Search<br/>Hotels & Car Rentals]
        GROQ_API[Groq API<br/>Llama-3 70B Versatile<br/>High-performance LLM]
    end

    subgraph "Data Flow"
        USER_DATA[User Travel Preferences<br/>Destination, Dates, Budget]
        HOTEL_DATA[Hotel Recommendations<br/>Names, Prices, Features]
        CAR_DATA[Car Rental Options<br/>Companies, Prices, Types]
        FINAL_PLAN[Comprehensive Travel Plan<br/>Itinerary, Costs, Tips]
    end

    %% Data Flow Connections
    USER_DATA --> STREAMLIT
    STREAMLIT --> TRAVEL_PLANNER
    TRAVEL_PLANNER --> HOTEL_AGENT
    TRAVEL_PLANNER --> CAR_AGENT
    HOTEL_AGENT --> SERPER_API
    CAR_AGENT --> SERPER_API
    HOTEL_AGENT --> GROQ_API
    CAR_AGENT --> GROQ_API
    TRAVEL_PLANNER --> GROQ_API
    SERPER_API --> HOTEL_DATA
    SERPER_API --> CAR_DATA
    HOTEL_DATA --> TRAVEL_PLANNER
    CAR_DATA --> TRAVEL_PLANNER
    TRAVEL_PLANNER --> FINAL_PLAN
    FINAL_PLAN --> STREAMLIT

    %% Styling
    classDef frontend fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef orchestration fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef agents fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef services fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class STREAMLIT frontend
    class TRAVEL_PLANNER orchestration
    class HOTEL_AGENT,CAR_AGENT agents
    class SERPER_API,GROQ_API services
    class USER_DATA,HOTEL_DATA,CAR_DATA,FINAL_PLAN data
```

## 🔄 Agent Internal Workflow Details

```mermaid
graph TD
    subgraph "Hotel Agent (CrewAI) Internal Flow"
        HA_IN[Input: Hotel Search Query]
        HA_CREW[CrewAI Workflow Initialization]
        HA_SPECIALIST[Create Hotel Booking Specialist]
        HA_TASK[Define Task: Search & Recommend Hotels]
        HA_EXECUTE[Execute Sequential Process]
        HA_TOOL[Hotel Search Tool Execution]
        HA_SERPER[SerperAPI Search]
        HA_PARSE[Parse Search Results]
        HA_LLM[LLM Analysis & Ranking]
        HA_RECOMMEND[Generate Hotel Recommendations]
        HA_OUT[Output: Structured Hotel Data]
        
        HA_IN --> HA_CREW
        HA_CREW --> HA_SPECIALIST
        HA_SPECIALIST --> HA_TASK
        HA_TASK --> HA_EXECUTE
        HA_EXECUTE --> HA_TOOL
        HA_TOOL --> HA_SERPER
        HA_SERPER --> HA_PARSE
        HA_PARSE --> HA_LLM
        HA_LLM --> HA_RECOMMEND
        HA_RECOMMEND --> HA_OUT
    end

    subgraph "Car Rental Agent (LangGraph) Internal Flow"
        CA_IN[Input: Car Rental Query]
        CA_GRAPH[LangGraph State Machine]
        CA_REACT[Create React Agent with Tools]
        CA_STATE[Define State Schema]
        CA_EXECUTE[Execute Graph-based Reasoning]
        CA_TOOL[Car Rental Tool Execution]
        CA_SERPER[SerperAPI Search]
        CA_PARSE[Parse Search Results]
        CA_LLM[LLM Analysis & Comparison]
        CA_RECOMMEND[Generate Car Rental Recommendations]
        CA_OUT[Output: Structured Car Rental Data]
        
        CA_IN --> CA_GRAPH
        CA_GRAPH --> CA_REACT
        CA_REACT --> CA_STATE
        CA_STATE --> CA_EXECUTE
        CA_EXECUTE --> CA_TOOL
        CA_TOOL --> CA_SERPER
        CA_SERPER --> CA_PARSE
        CA_PARSE --> CA_LLM
        CA_LLM --> CA_RECOMMEND
        CA_RECOMMEND --> CA_OUT
    end

    subgraph "Travel Planner (Google ADK) Internal Flow"
        TP_IN[Input: User Travel Request]
        TP_INIT[Initialize Configuration]
        TP_DISCOVER[Agent Discovery & Health Check]
        TP_COORD[Coordinate Parallel Execution]
        TP_COLLECT[Collect Agent Responses]
        TP_PARSE[Parse & Validate Responses]
        TP_INTEGRATE[Integrate Hotel & Car Data]
        TP_PROMPT[Construct Comprehensive Prompt]
        TP_GENERATE[Generate Final Travel Plan]
        TP_FORMAT[Format Response]
        TP_OUT[Output: Complete Travel Plan]
        
        TP_IN --> TP_INIT
        TP_INIT --> TP_DISCOVER
        TP_DISCOVER --> TP_COORD
        TP_COORD --> TP_COLLECT
        TP_COLLECT --> TP_PARSE
        TP_PARSE --> TP_INTEGRATE
        TP_INTEGRATE --> TP_PROMPT
        TP_PROMPT --> TP_GENERATE
        TP_GENERATE --> TP_FORMAT
        TP_FORMAT --> TP_OUT
    end
```

## 📊 Performance & Error Handling Flow

```mermaid
graph TD
    START[User Request Received]
    START --> VALIDATE{Input Validation}
    
    VALIDATE -->|Valid| DISCOVER[Agent Discovery]
    VALIDATE -->|Invalid| ERROR_INPUT[Return Input Error]
    
    DISCOVER --> CHECK_AGENTS{Check Agent Health}
    
    CHECK_AGENTS -->|All Available| PARALLEL_EXEC[Parallel Agent Execution]
    CHECK_AGENTS -->|Some Available| PARTIAL_EXEC[Partial Execution]
    CHECK_AGENTS -->|None Available| ERROR_AGENTS[Return Agent Error]
    
    PARALLEL_EXEC --> COLLECT_RESPONSES[Collect Agent Responses]
    PARTIAL_EXEC --> COLLECT_RESPONSES
    
    COLLECT_RESPONSES --> VALIDATE_RESPONSES{Validate Responses}
    
    VALIDATE_RESPONSES -->|Valid| GENERATE_PLAN[Generate Final Plan]
    VALIDATE_RESPONSES -->|Invalid| FALLBACK[Use Fallback Data]
    
    GENERATE_PLAN --> SUCCESS[Return Success Response]
    FALLBACK --> DEGRADED[Return Degraded Response]
    
    ERROR_INPUT --> ERROR_HANDLER[Error Handler]
    ERROR_AGENTS --> ERROR_HANDLER
    ERROR_HANDLER --> ERROR_RESPONSE[Return Error Response]
    
    subgraph "Error Recovery"
        RETRY[Retry Logic]
        CACHE[Use Cached Data]
        GENERIC[Generate Generic Recommendations]
    end
    
    ERROR_HANDLER --> RETRY
    RETRY --> DISCOVER
    ERROR_HANDLER --> CACHE
    CACHE --> DEGRADED
    ERROR_HANDLER --> GENERIC
    GENERIC --> DEGRADED
```

## 🔧 Technical Implementation Details

### **Agent Communication Protocols**

#### **HTTP REST API (Current Implementation)**
```mermaid
graph LR
    subgraph "Travel Planner"
        TP[Travel Planner Agent<br/>Port 10001]
    end
    
    subgraph "Hotel Agent"
        HA[Hotel Agent<br/>Port 10002<br/>CrewAI]
    end
    
    subgraph "Car Rental Agent"
        CA[Car Rental Agent<br/>Port 10003<br/>LangGraph]
    end
    
    TP -->|"POST /chat"| HA
    TP -->|"POST /chat"| CA
    TP -->|"GET /health"| HA
    TP -->|"GET /health"| CA
    
    HA -->|"JSON Response"| TP
    CA -->|"JSON Response"| TP
```

#### **A2A Protocol (Advanced Implementation)**
```mermaid
graph LR
    subgraph "A2A Discovery"
        DISCOVERY[GET /.well-known/agent.json]
        CAPABILITIES[Parse Agent Capabilities]
        METADATA[Store Agent Metadata]
    end
    
    subgraph "A2A Communication"
        MESSAGE[POST /a2a/message]
        MESSAGE_STRUCTURE[Message Structure]
        RESPONSE[Structured Response]
    end
    
    DISCOVERY --> CAPABILITIES
    CAPABILITIES --> METADATA
    MESSAGE --> MESSAGE_STRUCTURE
    MESSAGE_STRUCTURE --> RESPONSE
```

### **Data Transformation Pipeline**

```mermaid
graph LR
    subgraph "Input Data"
        USER_INPUT[User Travel Preferences]
        AGENT_CAPABILITIES[Agent Capabilities]
    end
    
    subgraph "Processing Pipeline"
        VALIDATION[Input Validation]
        DISCOVERY[Agent Discovery]
        EXECUTION[Parallel Execution]
        AGGREGATION[Response Aggregation]
        GENERATION[Plan Generation]
    end
    
    subgraph "Output Data"
        HOTEL_RECOMMENDATIONS[Hotel Recommendations]
        CAR_RENTAL_OPTIONS[Car Rental Options]
        COMPREHENSIVE_PLAN[Comprehensive Travel Plan]
    end
    
    USER_INPUT --> VALIDATION
    AGENT_CAPABILITIES --> DISCOVERY
    
    VALIDATION --> DISCOVERY
    DISCOVERY --> EXECUTION
    EXECUTION --> AGGREGATION
    AGGREGATION --> GENERATION
    
    EXECUTION --> HOTEL_RECOMMENDATIONS
    EXECUTION --> CAR_RENTAL_OPTIONS
    GENERATION --> COMPREHENSIVE_PLAN
```

This comprehensive Mermaid diagram provides a complete visual representation of the multi-agent travel planning system workflow, including all technical details, data flows, error handling, and performance characteristics. 