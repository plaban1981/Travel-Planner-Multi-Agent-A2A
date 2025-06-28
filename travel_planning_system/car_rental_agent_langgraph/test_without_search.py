#!/usr/bin/env python3
"""
Test the car rental agent without requiring SerperAPI.
This script tests the basic LLM functionality.
"""

import os
from dotenv import load_dotenv

def test_groq_connection():
    """Test if Groq API key is working."""
    print("🧪 Testing Groq API Connection...")
    
    try:
        from langchain_groq import ChatGroq
        
        # Load environment variables
        load_dotenv()
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key == "your_groq_api_key_here":
            print("❌ GROQ_API_KEY not set or still placeholder")
            return False
        
        # Test the connection
        llm = ChatGroq(model="llama3-70b-8192", api_key=groq_key)
        
        # Simple test query
        response = llm.invoke("Hello! Can you respond with 'Groq connection successful'?")
        print(f"✅ Groq Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq connection failed: {e}")
        return False

def test_agent_initialization():
    """Test if the agent can be initialized."""
    print("\n🧪 Testing Agent Initialization...")
    
    try:
        from agent import CarRentalAgent
        
        # Temporarily mock the search function to avoid SerperAPI requirement
        import agent
        
        # Save original function
        original_search = agent.search_car_rentals
        
        # Mock the search function
        def mock_search(*args, **kwargs):
            return """[
  {
    "company": "Test Car Rental",
    "description": "Mock car rental service for testing",
    "link": "https://example.com",
    "location": "Test Location",
    "pickup_date": "2024-06-15",
    "return_date": "2024-06-22",
    "car_type": "economy"
  }
]"""
        
        # Replace the function temporarily
        agent.search_car_rentals = mock_search
        
        # Initialize agent
        agent_instance = CarRentalAgent()
        print("✅ Agent initialized successfully!")
        
        # Test a simple query
        response = agent_instance.invoke("Find me a car rental in Paris", "test_context")
        print(f"✅ Agent Response: {response}")
        
        # Restore original function
        agent.search_car_rentals = original_search
        
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚗 Testing Car Rental Agent (Basic Functionality)")
    print("=" * 60)
    
    # Test 1: Groq connection
    groq_ok = test_groq_connection()
    
    # Test 2: Agent initialization (only if Groq works)
    if groq_ok:
        agent_ok = test_agent_initialization()
    else:
        agent_ok = False
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Groq Connection: {'✅ PASS' if groq_ok else '❌ FAIL'}")
    print(f"Agent Initialization: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    
    if groq_ok and agent_ok:
        print("\n🎉 All tests passed! Your agent is ready to use.")
        print("You can now run: python app/simple_executor.py")
    else:
        print("\n❌ Some tests failed. Please check your configuration.")

if __name__ == "__main__":
    main() 