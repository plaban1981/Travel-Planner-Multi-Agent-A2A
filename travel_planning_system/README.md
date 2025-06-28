# Travel Planning Multi-Agent System

This document describes a multi-agent application demonstrating how to orchestrate conversations between different agents to plan and book travel arrangements.

This application contains three specialized agents:
*   **Travel Planner Agent**: The primary agent that orchestrates the travel planning task using Google ADK.
*   **Hotel Booking Agent**: An agent that handles hotel research and booking using CrewAI.
*   **Car Rental Agent**: An agent that handles car rental research and booking using LangGraph.

## Features

- **Intelligent Travel Planning**: The system can plan complete travel itineraries including flights, hotels, and car rentals
- **Real-time Search**: All agents use SerperAPI to search for current information about destinations, hotels, and car rental options
- **Multi-Agent Coordination**: Agents communicate using the Agent-to-Agent (A2A) protocol for seamless coordination
- **Specialized Expertise**: Each agent has domain-specific knowledge and tools for their respective areas

## Setup and Deployment

### Prerequisites

Before running the application locally, ensure you have the following installed:

1. **uv:** The Python package management tool used in this project. Follow the installation guide: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)
2. **python 3.13** Python 3.13 is required to run a2a-sdk 
3. **set up .env** 

Create a `.env` file in the root of the `travel_planning_system` directory with your API keys:
```
GOOGLE_API_KEY="your_google_api_key_here"
SERPER_API_KEY="your_serper_api_key_here"
```

## Run the Agents

You will need to run each agent in a separate terminal window. The first time you run these commands, `uv` will create a virtual environment and install all necessary dependencies before starting the agent.

### Terminal 1: Run Car Rental Agent
```bash
cd car_rental_agent_langgraph
uv venv
source .venv/bin/activate
uv run --active app/__main__.py
```

### Terminal 2: Run Hotel Booking Agent
```bash
cd hotel_booking_agent_crewai
uv venv
source .venv/bin/activate
uv run --active .
```

### Terminal 3: Run Travel Planner Agent
```bash
cd travel_planner_agent_adk
uv venv
source .venv/bin/activate
uv run --active adk web      
```

## Interact with the Travel Planner Agent

Once all agents are running, the travel planner agent will begin the planning process. You can interact with it by asking questions like:

- "Plan a trip to Paris for next week"
- "Find me a hotel in Tokyo for the weekend"
- "Book a car rental in New York for 3 days"
- "Plan a complete vacation to London including flights, hotel, and car"

## Agent Capabilities

### Travel Planner Agent (Google ADK)
- Orchestrates the entire travel planning process
- Coordinates with hotel and car rental agents
- Searches for flight information using SerperAPI
- Creates comprehensive travel itineraries
- Handles user preferences and requirements

### Hotel Booking Agent (CrewAI)
- Searches for hotels using SerperAPI
- Provides detailed hotel information (amenities, reviews, pricing)
- Handles hotel booking requests
- Manages hotel preferences and requirements

### Car Rental Agent (LangGraph)
- Searches for car rental options using SerperAPI
- Provides car rental information (vehicle types, pricing, locations)
- Handles car rental booking requests
- Manages rental preferences and requirements

## References
- https://github.com/google/a2a-python
- https://codelabs.developers.google.com/intro-a2a-purchasing-concierge#1
- https://serper.dev/ - Search API for real-time information 