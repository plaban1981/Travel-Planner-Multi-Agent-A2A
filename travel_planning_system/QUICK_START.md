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