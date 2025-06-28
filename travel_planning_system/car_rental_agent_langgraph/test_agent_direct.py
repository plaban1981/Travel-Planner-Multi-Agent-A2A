#!/usr/bin/env python3
"""
Simple test script for the Car Rental Agent.
This script tests the agent directly without FastAPI dependencies.
"""

import os
from dotenv import load_dotenv
from agent import CarRentalAgent

def main():
    """Test the car rental agent directly."""
    print("🚗 Testing Car Rental Agent (LangGraph + Groq Llama-3 70B)")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with your GROQ_API_KEY")
        return
    
    try:
        # Initialize the agent
        print("📦 Initializing Car Rental Agent...")
        agent = CarRentalAgent()
        print("✅ Agent initialized successfully!")
        
        # Test queries
        test_queries = [
            "Find car rentals in Paris for next week",
            "I need a luxury car in Tokyo from 2024-06-15 to 2024-06-22",
            "What are the best car rental options in New York?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}: {query}")
            print("-" * 40)
            
            try:
                response = agent.invoke(query, f"test_context_{i}")
                print(f"✅ Response: {response}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        print("Please check your dependencies and API keys.")

if __name__ == "__main__":
    main() 