# A2A SDK Demo Projects
This repository contains example projects demonstrating the capabilities of the Agent-to-Agent (A2A) SDK. Each sub-directory is a self-contained project with its own dependencies and instructions.

## 🚀 Projects

### 1. Simple A2A Agent (`a2a_simple/`)

This project provides a basic example of the A2A SDK. It contains a single agent and a test client that invokes it. This is a great starting point for understanding the fundamental concepts of creating and interacting with an A2A agent.

**>> For setup and run instructions, see the [Simple A2A Agent README](./a2a_simple/README.md).**

### 2. Friend Scheduling Multi-Agent Demo (`a2a_friend_scheduling/`)

This is a more advanced example showcasing a multi-agent system. It demonstrates how a "host" agent can orchestrate a conversation between multiple "friend" agents to accomplish a goal—in this case, scheduling a meeting. This project is ideal for learning about multi-agent orchestration and communication.

**>> For setup and run instructions, see the [Friend Scheduling README](./a2a_friend_scheduling/README.md).**

### 3. 🎯 **Multi-Agent Travel Planning System** (`travel_planning_system/`)

**NEW!** A comprehensive multi-agent travel planning system that demonstrates advanced A2A protocol implementation with specialized AI agents for hotel booking and car rental services.

#### 🏗️ **System Architecture**

The Multi-Agent Travel Planning System is a distributed architecture that coordinates specialized AI agents to provide comprehensive travel planning services. The system uses the Agent-to-Agent (A2A) protocol for communication and leverages multiple AI frameworks for different specialized tasks.

**Core Components:**
- **Travel Planner Agent (Orchestrator)**: Google ADK framework, coordinates all travel planning tasks
- **Hotel Booking Agent (Specialist)**: CrewAI framework, specialized in hotel search and recommendations
- **Car Rental Agent (Specialist)**: LangGraph framework, specialized in car rental search and options
- **Streamlit Web Interface**: User-friendly web application for travel planning

**Technology Stack:**
- **LLM**: Groq Llama-3 70B Versatile (high-performance inference)
- **Search API**: SerperAPI (real-time web search)
- **Communication**: A2A Protocol + HTTP REST APIs
- **Frameworks**: Google ADK, CrewAI, LangGraph, Streamlit

#### 📦 **Package Dependencies**

The system uses multiple specialized packages for different components:

**🎯 Travel Planner Agent (Google ADK)**
```txt
google-adk>=1.2.1          # Google Agent Development Kit
nest-asyncio>=1.6.0        # Async event loop management
python-dotenv              # Environment variable management
click                      # Command-line interface toolkit
uvicorn                    # ASGI server for FastAPI
google-generativeai        # Google AI integration
httpx                      # Async HTTP client
requests                   # HTTP library
groq                       # Groq LLM API client
langchain-groq>=0.3.0      # LangChain Groq integration
langchain>=0.2.0           # LangChain core framework
langchain-community>=0.2.0 # LangChain community tools
langchain-core>=0.3.0      # LangChain core components
```

**🏨 Hotel Booking Agent (CrewAI)**
```txt
crewai>=0.70.0             # Multi-agent orchestration framework
python-dotenv              # Environment variable management
requests                   # HTTP library
fastapi                    # Modern web framework
uvicorn                    # ASGI server
pydantic                   # Data validation
groq                       # Groq LLM API client
langchain-groq>=0.3.0      # LangChain Groq integration
langchain>=0.2.0           # LangChain core framework
langchain-community>=0.2.0 # LangChain community tools
langchain-core>=0.3.0      # LangChain core components
```

**🚗 Car Rental Agent (LangGraph)**
```txt
langgraph>=0.5.0           # Graph-based agent framework
langchain-core>=0.3.0      # LangChain core components
langchain-google-genai>=2.0.0 # Google AI integration
python-dotenv              # Environment variable management
requests                   # HTTP library
fastapi                    # Modern web framework
uvicorn                    # ASGI server
pydantic                   # Data validation
groq                       # Groq LLM API client
langchain-groq>=0.3.0      # LangChain Groq integration
langchain>=0.2.0           # LangChain core framework
langchain-community>=0.2.0 # LangChain community tools
```

**🌐 Streamlit Web Interface**
```txt
streamlit>=1.28.0          # Web application framework
requests>=2.31.0           # HTTP library
python-dotenv>=1.0.0       # Environment variable management
langchain-groq>=0.3.0      # LangChain Groq integration
```

**🔧 Package Purposes:**

- **Agent Frameworks**: `google-adk`, `crewai`, `langgraph` - Core agent orchestration
- **LLM Integration**: `groq`, `langchain-groq` - High-performance LLM inference
- **Web Services**: `fastapi`, `uvicorn`, `streamlit` - API and UI servers
- **HTTP Communication**: `requests`, `httpx` - Agent-to-agent communication
- **Data Handling**: `pydantic` - Request/response validation
- **Configuration**: `python-dotenv` - Environment variable management
- **Async Support**: `nest-asyncio` - Event loop management
- **CLI Tools**: `click` - Command-line interface

#### 🔄 **Workflow Overview**

1. **User Input**: Travel details via Streamlit interface
2. **Agent Discovery**: Health checks and capability discovery
3. **Parallel Execution**: Hotel and car rental agents run simultaneously
4. **Response Aggregation**: Collect and integrate agent responses
5. **Plan Generation**: Comprehensive travel plan creation
6. **Response Delivery**: Display results with agent status

#### 📊 **Performance Characteristics**

- **Response Time**: 7-18 seconds total
- **Concurrency**: Parallel agent execution
- **Reliability**: Graceful error handling and fallback mechanisms
- **Scalability**: Horizontal scaling support for production deployment

#### 🚀 **Quick Start**

```bash
# Navigate to the travel planning system
cd travel_planning_system

# Install dependencies for each agent
cd hotel_booking_agent_crewai
pip install -r requirements.txt

cd ../car_rental_agent_langgraph
pip install -r requirements.txt

cd ../travel_planner_agent_adk
pip install -r requirements.txt

# Install Streamlit dependencies
cd ..
pip install -r streamlit_requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys:
# GROQ_API_KEY=your_groq_api_key
# SERPER_API_KEY=your_serper_api_key
# GOOGLE_API_KEY=your_google_api_key

# Start the agents (in separate terminals)
cd hotel_booking_agent_crewai
python hotel_agent.py          # Port 10002

cd ../car_rental_agent_langgraph
python car_rental_agent.py     # Port 10003

cd ../travel_planner_agent_adk
python travel_planner.py       # Port 10001

# Start the Streamlit web interface
cd ..
streamlit run streamlit_travel_app.py  # Port 8501
```

#### 📁 **Project Structure**

```
travel_planning_system/
├── hotel_booking_agent_crewai/
│   ├── hotel_agent.py          # CrewAI-based hotel booking agent
│   ├── hotel_tools.py          # Hotel search and booking tools
│   ├── requirements.txt        # Hotel agent dependencies
│   └── test_hotel_agent.py     # Hotel agent test script
├── car_rental_agent_langgraph/
│   ├── car_rental_agent.py     # LangGraph-based car rental agent
│   ├── car_rental_tools.py     # Car rental search and booking tools
│   ├── requirements.txt        # Car rental agent dependencies
│   └── test_car_rental_agent.py # Car rental agent test script
├── travel_planner_agent_adk/
│   ├── travel_planner.py       # Google ADK-based orchestrator
│   ├── requirements.txt        # Travel planner dependencies
│   └── test_travel_planner.py  # Travel planner test script
├── streamlit_travel_app.py     # Streamlit web interface
├── streamlit_requirements.txt  # Streamlit dependencies
├── .env.example               # Environment variables template
├── ARCHITECTURE.md            # Detailed system architecture
├── COMPLETE_WORKFLOW_DIAGRAM.md # Mermaid workflow diagrams
└── README.md                  # Project-specific documentation
```

#### 🎯 **Key Features**

- **Multi-Agent Coordination**: Seamless communication between specialized agents
- **Real-time Search**: Current hotel and car rental information via SerperAPI
- **AI-Powered Recommendations**: Intelligent analysis using Groq Llama-3 70B
- **User-Friendly Interface**: Streamlit web app with real-time status monitoring
- **Comprehensive Planning**: Detailed travel plans with cost breakdowns
- **Error Resilience**: Graceful handling of agent failures and API issues
- **A2A Protocol Support**: Full Agent-to-Agent communication compliance

#### 🔧 **Advanced Configuration**

**Agent Communication:**
- **HTTP REST API**: Simple communication for development
- **A2A Protocol**: Advanced agent discovery and message exchange
- **Health Monitoring**: Real-time agent status checking

**External Services:**
- **Groq API**: High-performance LLM inference
- **SerperAPI**: Real-time web search capabilities
- **Rate Limiting**: Respectful API usage with retry logic

**Deployment Options:**
- **Development**: Local environment with all agents on localhost
- **Production**: Distributed deployment with load balancing
- **Docker**: Containerized deployment for easy scaling

#### 📈 **Monitoring & Observability**

- **Agent Health Checks**: Real-time status monitoring
- **Response Time Tracking**: Performance metrics collection
- **Error Logging**: Comprehensive error tracking and debugging
- **User Analytics**: Usage patterns and system performance

#### 🔒 **Security & Privacy**

- **API Key Management**: Secure environment variable handling
- **Input Validation**: Comprehensive request sanitization
- **Response Filtering**: Privacy-conscious data handling
- **Access Control**: Agent authentication and authorization

#### 🚀 **Getting Started**

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd agent2agent-main/travel_planning_system
   ```

2. **Install Dependencies**
   ```bash
   # Install each agent's dependencies
   cd hotel_booking_agent_crewai && pip install -r requirements.txt
   cd ../car_rental_agent_langgraph && pip install -r requirements.txt
   cd ../travel_planner_agent_adk && pip install -r requirements.txt
   cd .. && pip install -r streamlit_requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add your API keys:
   # GROQ_API_KEY=your_groq_api_key
   # SERPER_API_KEY=your_serper_api_key
   # GOOGLE_API_KEY=your_google_api_key
   ```

4. **Start the Agents**
   ```bash
   # Terminal 1: Hotel Agent
   cd hotel_booking_agent_crewai
   python hotel_agent.py
   
   # Terminal 2: Car Rental Agent
   cd ../car_rental_agent_langgraph
   python car_rental_agent.py
   
   # Terminal 3: Travel Planner
   cd ../travel_planner_agent_adk
   python travel_planner.py
   ```

5. **Launch Web Interface**
   ```bash
   cd ..
   streamlit run streamlit_travel_app.py
   ```

6. **Test the System**
   ```bash
   # Test individual agents
   cd hotel_booking_agent_crewai && python test_hotel_agent.py
   cd ../car_rental_agent_langgraph && python test_car_rental_agent.py
   cd ../travel_planner_agent_adk && python test_travel_planner.py
   ```

#### 📚 **Documentation**

- **[Architecture Documentation](./travel_planning_system/ARCHITECTURE.md)**: Detailed system architecture and workflow
- **[Workflow Diagrams](./travel_planning_system/COMPLETE_WORKFLOW_DIAGRAM.md)**: Visual Mermaid diagrams of the complete workflow
- **[Agent Documentation](./travel_planning_system/README.md)**: Agent-specific setup and usage instructions

#### 🤝 **Contributing**

The Multi-Agent Travel Planning System is designed to be extensible and modular. Contributions are welcome for:

- **New Agent Types**: Additional specialized agents (flights, activities, etc.)
- **Enhanced Tools**: Improved search and booking capabilities
- **UI Improvements**: Better user experience and interface design
- **Performance Optimization**: Faster response times and better resource usage
- **Documentation**: Improved guides and examples

#### 🐛 **Troubleshooting**

**Common Issues:**
- **Agent Connection Failures**: Check if all agents are running on correct ports
- **API Key Errors**: Verify environment variables are properly set
- **LLM Failures**: Ensure Groq API key is valid and has sufficient credits
- **Search Failures**: Check SerperAPI key and rate limits
- **Package Conflicts**: Ensure each agent uses its own virtual environment

**Debug Mode:**
```bash
# Enable debug logging
export DEBUG=1
cd travel_planner_agent_adk
python travel_planner.py
```

#### 📄 **License**

This project is part of the A2A SDK demo collection and follows the same licensing terms as the parent repository.

---

**>> For detailed setup and run instructions, see the [Travel Planning System README](./travel_planning_system/README.md).**

## 📚 References
- [A2A Python SDK](https://github.com/google/a2a-python)
- [A2A Samples](https://github.com/google-a2a/a2a-samples/tree/main)
- [Groq API Documentation](https://console.groq.com/docs)
- [SerperAPI Documentation](https://serper.dev/api-docs)
- [CrewAI Framework](https://github.com/joaomdmoura/crewAI)
- [LangGraph Framework](https://github.com/langchain-ai/langgraph)
- [Google ADK Documentation](https://ai.google.dev/docs)
