# Multi-Agent Travel Planning System - Quick Reference

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Navigate to the travel planning system directory
cd travel_planning_system

# Option 1: Use the automated installation script (Recommended)
python install_dependencies.py

# Option 2: Use the Windows batch script
install_dependencies.bat

# Option 3: Manual installation (if above methods fail)
# For each agent directory, run:
pip install python-dotenv requests fastapi uvicorn pydantic groq
pip install langchain>=0.2.0 langchain-core>=0.3.0 langchain-community>=0.2.0 langchain-groq>=0.3.0
# Then install agent-specific dependencies (see individual agent sections below)
```

### 2. API Keys Setup
Create `.env` files in each agent directory:

**Car Rental Agent** (`car_rental_agent_langgraph/.env`):
```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**Hotel Booking Agent** (`hotel_booking_agent_crewai/.env`):
```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**Travel Planner Agent** (`travel_planner_agent_adk/.env`):
```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 3. Test Individual Agents

#### Car Rental Agent (LangGraph)
```bash
cd car_rental_agent_langgraph
python app/simple_executor.py
```

#### Hotel Booking Agent (CrewAI)
```bash
cd hotel_booking_agent_crewai
python simple_executor.py
```

#### Travel Planner Agent (ADK)
```bash
cd travel_planner_agent_adk
python simple_executor.py
```

### 4. Run Multi-Agent System
```bash
# Start the hotel booking agent
cd hotel_booking_agent_crewai
python app/__main__.py

# In another terminal, start the car rental agent
cd car_rental_agent_langgraph
python app/__main__.py

# In a third terminal, start the travel planner agent
cd travel_planner_agent_adk
python simple_executor.py
```

## 🔧 Troubleshooting

### Dependency Conflicts
If you encounter dependency conflicts:
1. Use the automated installation script: `python install_dependencies.py`
2. Or manually install with `--force-reinstall` flag:
   ```bash
   pip install --force-reinstall langchain>=0.2.0 langchain-core>=0.3.0
   ```

### Missing Modules
If you get "No module named 'uvicorn'" errors:
1. Ensure you're in the correct virtual environment
2. Install uvicorn: `pip install uvicorn`
3. Check that all dependencies are installed: `pip list`

### API Key Issues
- Verify all API keys are correctly set in `.env` files
- Ensure no extra spaces or quotes around the API keys
- Test API keys individually using the simple executors

## 📋 Agent Details

### Car Rental Agent (LangGraph)
- **Framework**: LangGraph
- **LLM**: Groq Llama-3 70B
- **Port**: 8001
- **Features**: Car search, booking simulation
- **Dependencies**: langgraph, langchain-core, langchain-groq

### Hotel Booking Agent (CrewAI)
- **Framework**: CrewAI
- **LLM**: Groq Llama-3 70B
- **Port**: 8002
- **Features**: Hotel search, booking simulation
- **Dependencies**: crewai, langchain-groq

### Travel Planner Agent (ADK)
- **Framework**: Google ADK
- **LLM**: Groq Llama-3 70B
- **Features**: Orchestration, A2A communication
- **Dependencies**: google-adk, langchain-groq

## 🔄 A2A Protocol

The system uses Agent-to-Agent (A2A) protocol for communication:

### Message Format
```json
{
  "message": "string",
  "sender": "agent_name",
  "recipient": "agent_name",
  "timestamp": "ISO-8601",
  "message_type": "request|response|error"
}
```

### Response Format
```json
{
  "status": "success|error",
  "data": {},
  "message": "string"
}
```

## 🎯 Usage Examples

### Simple Travel Planning Request
```python
# Example request to travel planner
{
  "destination": "Paris, France",
  "dates": "2024-06-15 to 2024-06-22",
  "travelers": 2,
  "budget": "mid-range"
}
```

### Car Rental Request
```python
# Example request to car rental agent
{
  "location": "Paris, France",
  "pickup_date": "2024-06-15",
  "return_date": "2024-06-22",
  "car_type": "economy"
}
```

### Hotel Booking Request
```python
# Example request to hotel booking agent
{
  "location": "Paris, France",
  "check_in": "2024-06-15",
  "check_out": "2024-06-22",
  "guests": 2,
  "budget": "mid-range"
}
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure API keys are valid and properly configured
4. Test individual agents before running the full system 