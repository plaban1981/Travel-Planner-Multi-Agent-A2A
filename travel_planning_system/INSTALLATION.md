# Installation Guide for Travel Planning Multi-Agent System

## Prerequisites

1. **Python 3.10+** (required for a2a-sdk)
2. **Git** (for cloning Google's a2a-sdk)
3. **API Keys**:
   - Groq API Key: https://console.groq.com/
   - Serper API Key: https://serper.dev/

## Step 1: Install a2a-sdk

The a2a-sdk needs to be installed from Google's repository:

```bash
# Clone the a2a-sdk repository
git clone https://github.com/google/a2a-python.git
cd a2a-python

# Install the SDK
pip install -e .
cd ..
```

## Step 2: Install Other Dependencies

```bash
# Install core dependencies
pip install groq langchain_groq
pip install crewai langgraph langchain-core
pip install fastapi uvicorn pydantic
pip install python-dotenv requests serper-python
pip install google-adk google-generativeai
```

## Step 3: Set Up Environment Variables

Create a `.env` file in the `travel_planning_system` directory:

```
GROQ_API_KEY="your_groq_api_key_here"
SERPER_API_KEY="your_serper_api_key_here"
```

## Step 4: Run the Agents

### Terminal 1: Car Rental Agent (LangGraph)
```bash
cd travel_planning_system/car_rental_agent_langgraph
python app/__main__.py
```

### Terminal 2: Hotel Booking Agent (CrewAI)
```bash
cd travel_planning_system/hotel_booking_agent_crewai
python __main__.py
```

### Terminal 3: Travel Planner Agent (ADK)
```bash
cd travel_planning_system/travel_planner_agent_adk
adk web
```

## Step 5: Test the System

Once all agents are running, you can interact with the Travel Planner Agent at:
- **Web Interface**: http://localhost:10001
- **API Endpoint**: http://localhost:10001/chat

### Example Queries:
- "Plan a trip to Paris for next week"
- "Find me a hotel in Tokyo for the weekend"
- "Book a car rental in New York for 3 days"

## Troubleshooting

### If a2a-sdk installation fails:
```bash
# Alternative installation method
pip install git+https://github.com/google/a2a-python.git
```

### If you get import errors:
```bash
# Make sure you're using Python 3.10+
python --version

# Install missing dependencies
pip install -r requirements.txt
```

### Port conflicts:
- Car Rental Agent: Port 10003
- Hotel Booking Agent: Port 10002  
- Travel Planner Agent: Port 10001

Change ports in the respective `__main__.py` files if needed. 