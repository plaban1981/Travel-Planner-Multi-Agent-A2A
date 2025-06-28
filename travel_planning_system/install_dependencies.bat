@echo off
echo 🚀 Multi-Agent Travel Planning System - Dependency Installation
echo ============================================================

echo.
echo 📦 Installing dependencies for Car Rental Agent (LangGraph)...
cd car_rental_agent_langgraph
python -m pip install --upgrade pip
pip install python-dotenv requests fastapi uvicorn pydantic groq
pip install langchain>=0.2.0 langchain-core>=0.3.0 langchain-community>=0.2.0 langchain-groq>=0.3.0
pip install langgraph>=0.5.0 langchain-google-genai>=2.0.0
cd ..

echo.
echo 📦 Installing dependencies for Hotel Booking Agent (CrewAI)...
cd hotel_booking_agent_crewai
python -m pip install --upgrade pip
pip install python-dotenv requests fastapi uvicorn pydantic groq
pip install langchain>=0.2.0 langchain-core>=0.3.0 langchain-community>=0.2.0 langchain-groq>=0.3.0
pip install crewai>=0.70.0
cd ..

echo.
echo 📦 Installing dependencies for Travel Planner Agent (ADK)...
cd travel_planner_agent_adk
python -m pip install --upgrade pip
pip install python-dotenv requests fastapi uvicorn pydantic groq
pip install langchain>=0.2.0 langchain-core>=0.3.0 langchain-community>=0.2.0 langchain-groq>=0.3.0
pip install google-adk>=1.2.1 nest-asyncio>=1.6.0 click google-generativeai httpx
cd ..

echo.
echo ✅ Installation completed!
echo.
echo 📋 Next steps:
echo 1. Create .env files in each agent directory with your API keys
echo 2. Test individual agents using their simple_executor.py files
echo 3. Run the full multi-agent system using the travel planner agent
echo.
pause 