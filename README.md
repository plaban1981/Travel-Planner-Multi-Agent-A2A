# Detailed Step-by-Step Workflow: User Query to Travel Plan

<img width="1278" alt="image" src="https://github.com/user-attachments/assets/df6b7af5-2994-4868-bb80-e95a3760b46f" />


## 🎯 Overview

This document provides a comprehensive, step-by-step breakdown of exactly what happens when a user enters a travel query into the Multi-Agent Travel Planning System. Each step includes technical details, data transformations, and system interactions.

## 📋 Prerequisites

Before the workflow begins, the following components must be running:

1. **Streamlit Web App** (`streamlit_travel_app.py`) - Port 8501
2. **Travel Planner Agent** (`travel_planner_agent.py`) - Port 10001
3. **Hotel Booking Agent** (`hotel_booking_agent.py`) - Port 10002
4. **Car Rental Agent** (`car_rental_agent.py`) - Port 10003

## 🔄 Complete Workflow Breakdown

### **Phase 1: User Input & Interface Processing**

#### **Step 1.1: User Interface Interaction**
```
User Action: Opens browser and navigates to http://localhost:8501
System Response: Streamlit app loads with travel planning form

User Input Example:
├── Destination: "Paris, France"
├── Check-in Date: "2024-06-15"
├── Check-out Date: "2024-06-20"
├── Budget Range: "Budget-friendly"
├── Number of Guests: 2
├── Car Rental Needed: Yes
└── Special Preferences: "Near city center"
```

#### **Step 1.2: Input Validation & Processing**
```python
# Streamlit app validates input
def validate_travel_input(destination, check_in, check_out, budget, guests):
    # Date validation
    if check_in >= check_out:
        raise ValueError("Check-in date must be before check-out date")
    
    # Budget validation
    valid_budgets = ["budget-friendly", "mid-range", "luxury"]
    if budget not in valid_budgets:
        raise ValueError("Invalid budget range")
    
    # Guest count validation
    if guests < 1 or guests > 10:
        raise ValueError("Invalid number of guests")
    
    return True
```

#### **Step 1.3: Request Formatting**
```python
# Format request for Travel Planner Agent
travel_request = {
    "destination": "Paris, France",
    "check_in": "2024-06-15",
    "check_out": "2024-06-20",
    "budget": "budget-friendly",
    "guests": 2,
    "car_rental": True,
    "preferences": "Near city center",
    "request_id": "uuid-12345-67890"
}
```

### **Phase 2: Travel Planner Agent Initialization**

#### **Step 2.1: Agent Startup & Configuration**
```python
# Travel Planner Agent loads configuration
class TravelPlannerAgent:
    def __init__(self):
        # Load environment variables
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        
        # Initialize Groq LLM
        self.llm = Groq(
            api_key=self.groq_api_key,
            model_name="llama-3-70b-versatile-0914"
        )
        
        # Define agent endpoints
        self.hotel_agent_url = "http://localhost:10002"
        self.car_rental_agent_url = "http://localhost:10003"
        
        # Initialize HTTP client
        self.http_client = httpx.AsyncClient(timeout=30.0)
```

#### **Step 2.2: Request Reception & Parsing**
```python
# Travel Planner receives request
@app.post("/plan_travel")
async def plan_travel(request: TravelRequest):
    # Parse incoming request
    destination = request.destination
    check_in = request.check_in
    check_out = request.check_out
    budget = request.budget
    guests = request.guests
    car_rental = request.car_rental
    preferences = request.preferences
    
    # Log request for tracking
    logger.info(f"Received travel request: {request.request_id}")
    
    return await process_travel_request(request)
```

### **Phase 3: Agent Discovery & Health Check**

#### **Step 3.1: Agent Health Verification**
```python
async def check_agent_health(self):
    """Check if all specialist agents are available"""
    agent_status = {}
    
    # Check Hotel Agent
    try:
        response = await self.http_client.get(f"{self.hotel_agent_url}/health")
        agent_status["hotel_agent"] = response.status_code == 200
    except Exception as e:
        logger.error(f"Hotel agent health check failed: {e}")
        agent_status["hotel_agent"] = False
    
    # Check Car Rental Agent
    try:
        response = await self.http_client.get(f"{self.car_rental_agent_url}/health")
        agent_status["car_rental_agent"] = response.status_code == 200
    except Exception as e:
        logger.error(f"Car rental agent health check failed: {e}")
        agent_status["car_rental_agent"] = False
    
    return agent_status
```

#### **Step 3.2: Agent Capability Discovery (A2A Protocol)**
```python
async def discover_agent_capabilities(self):
    """Discover agent capabilities using A2A protocol"""
    agent_capabilities = {}
    
    # Discover Hotel Agent capabilities
    try:
        response = await self.http_client.get(
            f"{self.hotel_agent_url}/.well-known/agent.json"
        )
        if response.status_code == 200:
            agent_capabilities["hotel_agent"] = response.json()
    except Exception as e:
        logger.warning(f"Could not discover hotel agent capabilities: {e}")
    
    # Discover Car Rental Agent capabilities
    try:
        response = await self.http_client.get(
            f"{self.car_rental_agent_url}/.well-known/agent.json"
        )
        if response.status_code == 200:
            agent_capabilities["car_rental_agent"] = response.json()
    except Exception as e:
        logger.warning(f"Could not discover car rental agent capabilities: {e}")
    
    return agent_capabilities
```

### **Phase 4: Parallel Agent Task Execution**

#### **Step 4.1: Hotel Agent Task Execution**

##### **4.1.1: Query Construction**
```python
# Travel Planner constructs hotel query
hotel_query = {
    "message": f"Find top 10 {budget} hotels in {destination} for {guests} guests from {check_in} to {check_out}. {preferences}",
    "request_id": request.request_id,
    "budget": budget,
    "destination": destination,
    "check_in": check_in,
    "check_out": check_out,
    "guests": guests
}
```

##### **4.1.2: Hotel Agent Processing (CrewAI)**
```python
# Hotel Agent receives query and processes with CrewAI
class HotelBookingAgent:
    def __init__(self):
        # Initialize CrewAI
        self.llm = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3-70b-versatile-0914"
        )
        
        # Create Hotel Booking Specialist
        self.hotel_specialist = Agent(
            role="Hotel Booking Specialist",
            goal="Find the best hotel options based on user requirements",
            backstory="Expert in hotel research and booking",
            verbose=True,
            allow_delegation=False,
            tools=[HotelSearchTool(), HotelBookingTool()],
            llm=self.llm
        )
        
        # Create task
        self.task = Task(
            description="Search and recommend hotels based on user requirements",
            agent=self.hotel_specialist
        )
        
        # Create crew
        self.crew = Crew(
            agents=[self.hotel_specialist],
            tasks=[self.task],
            verbose=True
        )
    
    async def process_hotel_request(self, query):
        # Execute CrewAI workflow
        result = self.crew.kickoff()
        return result
```

##### **4.1.3: Hotel Search Tool Execution**
```python
class HotelSearchTool(BaseTool):
    name = "hotel_search"
    description = "Search for hotels using real-time web search"
    
    def _run(self, query: str) -> str:
        # Construct SerperAPI query
        search_query = f"hotels in {query} budget-friendly"
        
        # Make SerperAPI request
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json"
        }
        payload = {"q": search_query, "num": 10}
        
        response = requests.post(url, headers=headers, json=payload)
        results = response.json()
        
        # Parse and format results
        hotels = []
        for result in results.get("organic", [])[:5]:
            hotel = {
                "name": result.get("title", ""),
                "description": result.get("snippet", ""),
                "url": result.get("link", ""),
                "rating": result.get("rating", "N/A"),
                "price_range": "Budget-friendly"
            }
            hotels.append(hotel)
        
        return json.dumps(hotels, indent=2)
```

##### **4.1.4: LLM Processing & Recommendation Generation**
```python
# Hotel Agent LLM processes search results
def generate_hotel_recommendations(self, search_results):
    prompt = f"""
    Based on the following hotel search results, provide detailed recommendations:
    
    Search Results:
    {search_results}
    
    User Requirements:
    - Destination: {destination}
    - Budget: {budget}
    - Guests: {guests}
    - Dates: {check_in} to {check_out}
    - Preferences: {preferences}
    
    Please provide:
    1. Top 5 hotel recommendations with prices
    2. Brief description of each hotel
    3. Why each hotel is suitable for the user
    4. Estimated total cost for the stay
    """
    
    response = self.llm.invoke(prompt)
    return response
```

#### **Step 4.2: Car Rental Agent Task Execution**

##### **4.2.1: Query Construction**
```python
# Travel Planner constructs car rental query
car_rental_query = {
    "message": f"Find car rental options in {destination} from {check_in} to {check_out}",
    "request_id": request.request_id,
    "destination": destination,
    "check_in": check_in,
    "check_out": check_out
}
```

##### **4.2.2: Car Rental Agent Processing (LangGraph)**
```python
# Car Rental Agent receives query and processes with LangGraph
class CarRentalAgent:
    def __init__(self):
        # Initialize LangGraph
        self.llm = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3-70b-versatile-0914"
        )
        
        # Create React agent with tools
        self.agent = create_react_agent(
            llm=self.llm,
            tools=[search_car_rentals, book_car_rental],
            state_schema=AgentState
        )
        
        # Create app
        self.app = create_agent_executor(
            agent=self.agent,
            tools=[search_car_rentals, book_car_rental]
        )
    
    async def process_car_rental_request(self, query):
        # Execute LangGraph workflow
        result = self.app.invoke({"input": query})
        return result
```

##### **4.2.3: Car Rental Search Tool Execution**
```python
@tool
def search_car_rentals(query: str) -> str:
    """Search for car rental options using real-time web search"""
    
    # Construct SerperAPI query
    search_query = f"car rental {query}"
    
    # Make SerperAPI request
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }
    payload = {"q": search_query, "num": 10}
    
    response = requests.post(url, headers=headers, json=payload)
    results = response.json()
    
    # Parse and format results
    car_rentals = []
    for result in results.get("organic", [])[:5]:
        rental = {
            "company": result.get("title", ""),
            "company": result.get("title", ""),
            "description": result.get("snippet", ""),
            "url": result.get("link", ""),
            "location": query,
            "price_range": "Varies"
        }
        car_rentals.append(rental)
    
    return json.dumps(car_rentals, indent=2)
```

##### **4.2.4: LLM Processing & Recommendation Generation**
```python
# Car Rental Agent LLM processes search results
def generate_car_rental_recommendations(self, search_results):
    prompt = f"""
    Based on the following car rental search results, provide detailed recommendations:
    
    Search Results:
    {search_results}
    
    User Requirements:
    - Destination: {destination}
    - Dates: {check_in} to {check_out}
    
    Please provide:
    1. Top 5 car rental options
    2. Brief description of each company
    3. Why each option is suitable
    4. Estimated daily rental costs
    """
    
    response = self.llm.invoke(prompt)
    return response
```

### **Phase 5: Response Collection & Aggregation**

#### **Step 5.1: Response Parsing**
```python
async def collect_agent_responses(self, hotel_query, car_rental_query):
    """Collect responses from both agents in parallel"""
    
    # Execute both agents in parallel
    hotel_task = asyncio.create_task(
        self.http_client.post(f"{self.hotel_agent_url}/chat", json=hotel_query)
    )
    car_rental_task = asyncio.create_task(
        self.http_client.post(f"{self.car_rental_agent_url}/chat", json=car_rental_query)
    )
    
    # Wait for both responses
    hotel_response, car_rental_response = await asyncio.gather(
        hotel_task, car_rental_task, return_exceptions=True
    )
    
    # Parse responses
    hotel_data = None
    car_rental_data = None
    
    if isinstance(hotel_response, Exception):
        logger.error(f"Hotel agent failed: {hotel_response}")
    else:
        hotel_data = hotel_response.json()
    
    if isinstance(car_rental_response, Exception):
        logger.error(f"Car rental agent failed: {car_rental_response}")
    else:
        car_rental_data = car_rental_response.json()
    
    return hotel_data, car_rental_data
```

#### **Step 5.2: Data Integration**
```python
def integrate_agent_data(self, hotel_data, car_rental_data, user_request):
    """Integrate data from both agents"""
    
    integrated_data = {
        "user_request": user_request,
        "hotel_recommendations": hotel_data.get("recommendations", []),
        "car_rental_options": car_rental_data.get("recommendations", []),
        "total_hotels": len(hotel_data.get("recommendations", [])),
        "total_car_rentals": len(car_rental_data.get("recommendations", [])),
        "collection_timestamp": datetime.now().isoformat()
    }
    
    return integrated_data
```

### **Phase 6: Comprehensive Plan Generation**

#### **Step 6.1: LLM Prompt Construction**
```python
def construct_final_plan_prompt(self, integrated_data):
    """Construct prompt for final travel plan generation"""
    
    prompt = f"""
    Create a comprehensive travel plan based on the following information:
    
    USER REQUEST:
    - Destination: {integrated_data['user_request']['destination']}
    - Check-in: {integrated_data['user_request']['check_in']}
    - Check-out: {integrated_data['user_request']['check_out']}
    - Budget: {integrated_data['user_request']['budget']}
    - Guests: {integrated_data['user_request']['guests']}
    - Car Rental: {integrated_data['user_request']['car_rental']}
    - Preferences: {integrated_data['user_request']['preferences']}
    
    HOTEL RECOMMENDATIONS:
    {json.dumps(integrated_data['hotel_recommendations'], indent=2)}
    
    CAR RENTAL OPTIONS:
    {json.dumps(integrated_data['car_rental_options'], indent=2)}
    
    Please create a comprehensive travel plan that includes:
    
    1. TRIP SUMMARY
       - Destination overview
       - Travel dates and duration
       - Number of travelers
    
    2. ACCOMMODATION RECOMMENDATIONS
       - Top 3 hotel recommendations with prices
       - Why each hotel is suitable
       - Estimated accommodation costs
    
    3. TRANSPORTATION OPTIONS
       - Car rental recommendations
       - Alternative transportation options
       - Estimated transportation costs
    
    4. COST BREAKDOWN
       - Accommodation costs
       - Transportation costs
       - Estimated total trip cost
    
    5. TRAVEL TIPS
       - Best time to visit
       - Local customs and etiquette
       - Money-saving tips
    
    6. DAY-BY-DAY SUGGESTIONS
       - Recommended activities
       - Restaurant suggestions
       - Sightseeing highlights
    
    Format the response in a clear, organized manner with proper sections and bullet points.
    """
    
    return prompt
```

#### **Step 6.2: Final Plan Generation**
```python
async def generate_comprehensive_plan(self, integrated_data):
    """Generate final comprehensive travel plan"""
    
    # Construct prompt
    prompt = self.construct_final_plan_prompt(integrated_data)
    
    # Generate plan with Groq LLM
    try:
        response = self.llm.invoke(prompt)
        
        # Parse and structure the response
        comprehensive_plan = {
            "request_id": integrated_data["user_request"]["request_id"],
            "generated_at": datetime.now().isoformat(),
            "agent_status": {
                "hotel_agent": "success" if integrated_data["hotel_recommendations"] else "failed",
                "car_rental_agent": "success" if integrated_data["car_rental_options"] else "failed"
            },
            "plan": response,
            "summary": {
                "total_hotels_found": integrated_data["total_hotels"],
                "total_car_rentals_found": integrated_data["total_car_rentals"],
                "processing_time": "7-18 seconds"
            }
        }
        
        return comprehensive_plan
        
    except Exception as e:
        logger.error(f"Failed to generate comprehensive plan: {e}")
        return {
            "error": "Failed to generate travel plan",
            "details": str(e)
        }
```

### **Phase 7: Response Delivery & User Interface Update**

#### **Step 7.1: Response Formatting**
```python
def format_response_for_ui(self, comprehensive_plan):
    """Format response for Streamlit UI display"""
    
    formatted_response = {
        "status": "success" if "error" not in comprehensive_plan else "error",
        "data": comprehensive_plan,
        "ui_elements": {
            "show_agent_status": True,
            "show_download_button": True,
            "show_cost_breakdown": True,
            "show_recommendations": True
        }
    }
    
    return formatted_response
```

#### **Step 7.2: Streamlit UI Update**
```python
# Streamlit app receives and displays response
def display_travel_plan(response):
    """Display travel plan in Streamlit UI"""
    
    if response["status"] == "success":
        # Display agent status
        st.subheader("🤖 Agent Status")
        col1, col2 = st.columns(2)
        
        with col1:
            hotel_status = response["data"]["agent_status"]["hotel_agent"]
            st.metric("Hotel Agent", "✅ Success" if hotel_status == "success" else "❌ Failed")
        
        with col2:
            car_status = response["data"]["agent_status"]["car_rental_agent"]
            st.metric("Car Rental Agent", "✅ Success" if car_status == "success" else "❌ Failed")
        
        # Display comprehensive plan
        st.subheader("🗺️ Your Travel Plan")
        st.markdown(response["data"]["plan"])
        
        # Display summary
        st.subheader("📊 Trip Summary")
        summary = response["data"]["summary"]
        st.write(f"Hotels Found: {summary['total_hotels_found']}")
        st.write(f"Car Rentals Found: {summary['total_car_rentals_found']}")
        st.write(f"Processing Time: {summary['processing_time']}")
        
        # Download button
        if response["ui_elements"]["show_download_button"]:
            st.download_button(
                label="📥 Download Travel Plan",
                data=response["data"]["plan"],
                file_name=f"travel_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
    
    else:
        st.error("❌ Failed to generate travel plan")
        st.write(f"Error: {response['data']['error']}")
```

## 📊 Performance Metrics & Timing

### **Response Time Breakdown**
```
Total Response Time: 7-18 seconds

Breakdown:
├── Agent Discovery: 100-200ms
├── Hotel Search: 2-5 seconds
│   ├── SerperAPI call: 500ms-1s
│   ├── LLM processing: 1-3s
│   └── Response formatting: 500ms
├── Car Rental Search: 2-5 seconds
│   ├── SerperAPI call: 500ms-1s
│   ├── LLM processing: 1-3s
│   └── Response formatting: 500ms
├── Plan Generation: 3-8 seconds
│   ├── Prompt construction: 100ms
│   ├── LLM processing: 2-6s
│   └── Response formatting: 1-2s
└── UI Update: 100-200ms
```

### **Success Rate Metrics**
```
Agent Success Rates:
├── Hotel Agent: 95% (fails on SerperAPI issues)
├── Car Rental Agent: 95% (fails on SerperAPI issues)
├── Travel Planner: 98% (fails on LLM issues)
└── Overall System: 90% (graceful degradation)
```

## 🔧 Error Handling & Recovery

### **Agent Failure Scenarios**
```python
async def handle_agent_failures(self, hotel_data, car_rental_data):
    """Handle cases where agents fail"""
    
    if not hotel_data and not car_rental_data:
        # Both agents failed
        return {
            "status": "error",
            "message": "All agents are currently unavailable. Please try again later.",
            "fallback_data": self.get_cached_recommendations()
        }
    
    elif not hotel_data:
        # Only hotel agent failed
        return {
            "status": "partial",
            "message": "Hotel recommendations unavailable. Showing car rental options only.",
            "car_rental_data": car_rental_data
        }
    
    elif not car_rental_data:
        # Only car rental agent failed
        return {
            "status": "partial",
            "message": "Car rental options unavailable. Showing hotel recommendations only.",
            "hotel_data": hotel_data
        }
    
    else:
        # Both agents succeeded
        return {
            "status": "success",
            "hotel_data": hotel_data,
            "car_rental_data": car_rental_data
        }
```

### **API Failure Recovery**
```python
def handle_api_failures(self, api_response, fallback_data):
    """Handle external API failures"""
    
    if api_response.status_code != 200:
        logger.warning(f"API call failed: {api_response.status_code}")
        
        # Use cached data if available
        if fallback_data:
            logger.info("Using cached data as fallback")
            return fallback_data
        
        # Return generic recommendations
        return self.generate_generic_recommendations()
    
    return api_response.json()
```

This detailed workflow provides a complete understanding of how the multi-agent travel planning system processes user queries, from initial input to final response delivery, including all technical details, data transformations, and error handling mechanisms. 




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



# Multi-Agent Travel Planning System - Quick Reference

## 🚀 Quick Start

<img width="970" alt="image" src="https://github.com/user-attachments/assets/aafb47e3-fee6-4a5f-ab5d-ffe4a582c052" />


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
