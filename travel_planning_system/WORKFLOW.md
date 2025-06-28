# Multi-Agent Travel Planning System - Step-by-Step Workflow

## 🎯 **System Overview**

This workflow demonstrates how to set up, test, and run a complete multi-agent travel planning system using:
- **Groq Llama-3 70B Versatile** as the LLM
- **SerperAPI** for real-time search
- **Agent-to-Agent (A2A) protocol** for coordination
- **Three specialized agents**: Travel Planner, Hotel Booking, Car Rental

---

## 📋 **Phase 1: Environment Setup**

### Step 1.1: Prerequisites Check
```bash
# Check Python version (needs 3.10+)
python --version

# Check if pip is available
pip --version

# Check if git is available
git --version
```

### Step 1.2: Create Project Structure
```bash
# Navigate to project directory
cd travel_planning_system

# Verify directory structure
ls -la
# Should show:
# - travel_planner_agent_adk/
# - hotel_booking_agent_crewai/
# - car_rental_agent_langgraph/
# - README.md
# - INSTALLATION.md
# - QUICK_START.md
```

### Step 1.3: Set Up Environment Variables
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
echo "SERPER_API_KEY=your_serper_api_key_here" >> .env

# Verify .env file
cat .env
```

---

## 🔧 **Phase 2: Dependencies Installation**

### Step 2.1: Install Core Dependencies
```bash
# Install Groq and LangChain integration
pip install groq langchain_groq

# Install Agent Frameworks
pip install crewai langgraph langchain-core

# Install Web Framework
pip install fastapi uvicorn pydantic

# Install Utilities
pip install python-dotenv requests serper-python
```

### Step 2.2: Install Google ADK (for Travel Planner)
```bash
# Install Google ADK
pip install google-adk google-generativeai
```

### Step 2.3: Install A2A SDK (Optional - for full coordination)
```bash
# Clone and install a2a-sdk
git clone https://github.com/google/a2a-python.git
cd a2a-python
pip install -e .
cd ..
```

---

## 🧪 **Phase 3: Individual Agent Testing**

### Step 3.1: Test Hotel Booking Agent
```bash
# Navigate to hotel agent
cd hotel_booking_agent_crewai

# Run test script
python test_hotel_agent.py

# Expected output:
# 🏨 Testing Hotel Booking Agent with Groq Llama-3 70B
# ✅ Hotel Booking Agent initialized successfully!
# 🔍 Test 1: Find hotels in Paris for next week
# ✅ Response: [Hotel search results from SerperAPI...]
```

### Step 3.2: Test Car Rental Agent
```bash
# Navigate to car rental agent
cd ../car_rental_agent_langgraph

# Run test script
python test_car_agent.py

# Expected output:
# 🚗 Testing Car Rental Agent with Groq Llama-3 70B
# ✅ Car Rental Agent initialized successfully!
# 🔍 Test 1: Find car rentals in Paris for next week
# ✅ Response: [Car rental options from SerperAPI...]
```

### Step 3.3: Verify Agent Functionality
- ✅ **Hotel Agent**: Should return hotel search results
- ✅ **Car Rental Agent**: Should return car rental options
- ✅ **Groq Integration**: Should use Llama-3 70B for responses
- ✅ **SerperAPI**: Should provide real-time search data

---

## 🌐 **Phase 4: Multi-Agent System Setup**

### Step 4.1: Start Car Rental Agent (Terminal 1)
```bash
# Open new terminal
cd travel_planning_system/car_rental_agent_langgraph

# Start the agent server
python app/__main__.py

# Expected output:
# INFO:     Started server process [PID]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:10003
```

### Step 4.2: Start Hotel Booking Agent (Terminal 2)
```bash
# Open new terminal
cd travel_planning_system/hotel_booking_agent_crewai

# Start the agent server
python __main__.py

# Expected output:
# INFO:     Started server process [PID]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:10002
```

### Step 4.3: Start Travel Planner Agent (Terminal 3)
```bash
# Open new terminal
cd travel_planning_system/travel_planner_agent_adk

# Start the ADK web interface
adk web

# Expected output:
# Travel Planner Agent initialized
# ADK web server running on http://localhost:10001
```

---

## 🎮 **Phase 5: System Testing & Interaction**

### Step 5.1: Verify Agent Connectivity
```bash
# Test agent endpoints
curl http://localhost:10002/agent_card
curl http://localhost:10003/agent_card

# Expected response: Agent information in JSON format
```

### Step 5.2: Access Travel Planner Interface
1. **Open browser**: Navigate to `http://localhost:10001`
2. **Login**: Use default credentials or create account
3. **Verify interface**: Should show Travel Planner Agent chat interface

### Step 5.3: Test Complete Workflow
**Query**: "Plan a trip to Paris for next week"

**Expected Workflow**:
1. **Travel Planner** receives request
2. **Travel Planner** searches flights using SerperAPI
3. **Travel Planner** sends A2A message to **Hotel Agent**: "Find hotels in Paris for 2024-01-15 to 2024-01-22"
4. **Travel Planner** sends A2A message to **Car Rental Agent**: "Find car rentals in Paris for 2024-01-15 to 2024-01-22"
5. **Hotel Agent** searches SerperAPI and responds with hotel options
6. **Car Rental Agent** searches SerperAPI and responds with car rental options
7. **Travel Planner** compiles complete itinerary and responds to user

---

## 🔍 **Phase 6: Monitoring & Debugging**

### Step 6.1: Monitor Agent Logs
```bash
# Terminal 1: Car Rental Agent logs
# Terminal 2: Hotel Booking Agent logs  
# Terminal 3: Travel Planner Agent logs

# Look for:
# - A2A message exchanges
# - SerperAPI search requests
# - Groq LLM responses
# - Error messages
```

### Step 6.2: Test Different Scenarios
```bash
# Test queries to try:
"Find me a luxury hotel in Tokyo for the weekend"
"Book a car rental in New York for 3 days"
"Plan a complete vacation to London including flights, hotel, and car"
"Find budget hotels in Rome for next month"
```

### Step 6.3: Performance Monitoring
- **Response Time**: Should be < 5 seconds for simple queries
- **A2A Communication**: Should be seamless between agents
- **SerperAPI Integration**: Should provide current, relevant results
- **Groq LLM**: Should generate coherent, helpful responses

---

## 🚀 **Phase 7: Production Deployment**

### Step 7.1: Environment Optimization
```bash
# Set production environment variables
export GROQ_API_KEY="production_key"
export SERPER_API_KEY="production_key"

# Configure logging
export LOG_LEVEL="INFO"
```

### Step 7.2: Process Management
```bash
# Use process managers like PM2 or systemd
pm2 start car_rental_agent.py --name "car-rental-agent"
pm2 start hotel_booking_agent.py --name "hotel-booking-agent"
pm2 start travel_planner_agent.py --name "travel-planner-agent"
```

### Step 7.3: Load Balancing
```bash
# Set up reverse proxy (nginx)
# Configure multiple agent instances
# Set up health checks
```

---

## 📊 **Expected Results**

### Successful System Operation:
- ✅ **All agents start without errors**
- ✅ **A2A protocol enables seamless communication**
- ✅ **SerperAPI provides real-time search results**
- ✅ **Groq Llama-3 70B generates intelligent responses**
- ✅ **Complete travel itineraries are created**

### Sample Output:
```
User: "Plan a trip to Paris for next week"

Travel Planner Agent:
🎯 Travel Planning Complete!

✈️ FLIGHTS:
- Air France AF123: JFK → CDG, $850
- Delta DL456: JFK → CDG, $920

🏨 HOTELS:
- Hotel Ritz Paris: $450/night, 5-star luxury
- Hotel de Crillon: $380/night, 4-star boutique

🚗 CAR RENTALS:
- Europcar: Economy car, $45/day
- Hertz: Luxury sedan, $120/day

📅 ITINERARY:
- Check-in: 2024-01-15
- Check-out: 2024-01-22
- Total estimated cost: $2,500
```

---

## 🔧 **Troubleshooting Guide**

### Common Issues:
1. **Port conflicts**: Change ports in `__main__.py` files
2. **API key errors**: Verify `.env` file and key validity
3. **Import errors**: Install missing dependencies
4. **A2A connection failures**: Check agent URLs and network connectivity

### Debug Commands:
```bash
# Check agent status
curl http://localhost:10002/health
curl http://localhost:10003/health

# Test API keys
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('GROQ:', bool(os.getenv('GROQ_API_KEY'))); print('SERPER:', bool(os.getenv('SERPER_API_KEY')))"

# Check dependencies
pip list | grep -E "(groq|crewai|langgraph|fastapi)"
```

This workflow provides a complete path from setup to production deployment of your multi-agent travel planning system! 