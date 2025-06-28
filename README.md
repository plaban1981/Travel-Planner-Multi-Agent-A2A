# Travel-Planner-Multi-Agent-A2A
Develop a multiagent travel planner using Agent 2 Agent protocol framework

<img width="1278" alt="image" src="https://github.com/user-attachments/assets/29c15ea7-34da-4e4c-bbf3-6f356fb08c52" />

# Multi-Agent Travel Planning System - Quick Reference

<img width="798" alt="image" src="https://github.com/user-attachments/assets/4d7bfebb-8271-42f4-9d1e-0a63ae56496a" />


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

# Quick Start Guide (Without A2A Protocol)

## For Testing Individual Agents

If you want to test the agents individually without the A2A protocol, follow this guide:

## Step 1: Install Dependencies

```bash
# Install core dependencies
pip install groq langchain_groq
pip install crewai langgraph langchain-core
pip install fastapi uvicorn pydantic
pip install python-dotenv requests serper-python
```

## Step 2: Set Up Environment Variables

Create a `.env` file in the `travel_planning_system` directory:

```
GROQ_API_KEY="your_groq_api_key_here"
SERPER_API_KEY="your_serper_api_key_here"
```

## Step 3: Test Individual Agents

### Test Hotel Booking Agent
```bash
cd travel_planning_system/hotel_booking_agent_crewai
python test_hotel_agent.py
```

### Test Car Rental Agent
```bash
cd travel_planning_system/car_rental_agent_langgraph
python test_car_agent.py
```

## Step 4: Create Test Scripts

Let me create simple test scripts for each agent:

### Hotel Booking Agent Test
```python
# test_hotel_agent.py
import os
from dotenv import load_dotenv
from agent import HotelBookingAgent

load_dotenv()

def test_hotel_agent():
    agent = HotelBookingAgent()
    
    # Test queries
    queries = [
        "Find hotels in Paris for next week",
        "Book a hotel in Tokyo for 3 nights",
        "What are the best hotels in New York?"
    ]
    
    for query in queries:
        print(f"\n--- Testing: {query} ---")
        try:
            response = agent.invoke(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_hotel_agent()
```

### Car Rental Agent Test
```python
# test_car_agent.py
import os
from dotenv import load_dotenv
from app.agent import CarRentalAgent

load_dotenv()

def test_car_agent():
    agent = CarRentalAgent()
    
    # Test queries
    queries = [
        "Find car rentals in Paris for next week",
        "Book a luxury car in Tokyo for 3 days",
        "What are the cheapest car rental options in New York?"
    ]
    
    for query in queries:
        print(f"\n--- Testing: {query} ---")
        try:
            response = agent.invoke(query, "test_context")
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_car_agent()
```

## Step 5: Run Tests

```bash
# Test Hotel Agent
cd travel_planning_system/hotel_booking_agent_crewai
python test_hotel_agent.py

# Test Car Rental Agent  
cd ../car_rental_agent_langgraph
python test_car_agent.py
```

## Expected Output

You should see responses from each agent using Groq Llama-3 70B, including:
- Hotel search results with SerperAPI data
- Car rental options with pricing information
- Booking confirmations

## Next Steps

Once individual agents work, you can:
1. Install a2a-sdk for full multi-agent coordination
2. Run the complete system with A2A protocol
3. Test the Travel Planner Agent orchestration 

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure API keys are valid and properly configured
4. Test individual agents before running the full system 
