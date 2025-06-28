#!/usr/bin/env python3
"""
Test script for hotel booking agent with focus on budget-friendly hotels.
"""

import os
import json
from dotenv import load_dotenv
from agent import HotelBookingAgent

def test_hotel_search():
    """Test hotel search functionality."""
    print("🏨 Testing Hotel Booking Agent - Budget-Friendly Hotels")
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
        print("📦 Initializing Hotel Booking Agent...")
        agent = HotelBookingAgent()
        print("✅ Agent initialized successfully!")
        
        # Test queries for budget-friendly hotels
        test_queries = [
            "Find top 10 budget-friendly hotels in Paris for next week",
            "Search for cheap hotels in Tokyo under $100 per night",
            "What are the best budget hotels in New York City?",
            "Find affordable hotels in London for a family of 4",
            "Search for budget-friendly hotels in Rome with good reviews"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}: {query}")
            print("-" * 60)
            
            try:
                response = agent.invoke(query)
                print(f"✅ Response:")
                print(response)
                print("\n" + "="*60)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n🎉 All hotel search tests completed!")
        
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        print("Please check your dependencies and API keys.")

def test_specific_budget_query():
    """Test a specific budget-friendly hotel query."""
    print("\n🎯 Testing Specific Budget Query")
    print("=" * 40)
    
    try:
        agent = HotelBookingAgent()
        
        # Specific query for budget hotels
        query = """
        Search for the top 10 budget-friendly hotels in Paris, France. 
        Please include:
        - Hotel names and locations
        - Price ranges per night
        - Guest ratings and reviews
        - Amenities offered
        - Distance from city center
        Focus on hotels under $150 per night.
        """
        
        print(f"🔍 Query: {query}")
        print("-" * 40)
        
        response = agent.invoke(query)
        print(f"✅ Detailed Response:")
        print(response)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Test basic hotel search
    test_hotel_search()
    
    # Test specific budget query
    test_specific_budget_query() 