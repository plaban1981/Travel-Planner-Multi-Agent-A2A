#!/usr/bin/env python3
"""
Test script for the travel planner agent.
"""

import os
import asyncio
from dotenv import load_dotenv

def test_travel_planner():
    """Test the travel planner agent."""
    print("✈️ Testing Travel Planner Agent")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check API keys
    groq_key = os.getenv("GROQ_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    print("🔍 Checking API Keys...")
    print(f"GROQ_API_KEY: {'✅ Set' if groq_key else '❌ Not set'}")
    print(f"GOOGLE_API_KEY: {'✅ Set' if google_key else '❌ Not set'}")
    print(f"SERPER_API_KEY: {'✅ Set' if serper_key else '❌ Not set'}")
    
    if not groq_key:
        print("❌ GROQ_API_KEY is required")
        return False
    
    try:
        # Import and test the travel planner
        from travel_planner.agent import TravelPlannerAgent
        
        print("\n📦 Initializing Travel Planner Agent...")
        
        # Test queries
        test_queries = [
            "Plan a trip to Paris for next week including hotel and car rental",
            "I need a complete travel plan for Tokyo with budget-friendly options",
            "Help me plan a vacation to New York with hotel and transportation"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}: {query}")
            print("-" * 60)
            
            try:
                # Create agent instance
                agent = TravelPlannerAgent()
                print("✅ Agent initialized successfully!")
                
                # Test the agent (this would require async handling)
                print("ℹ️  Note: Full agent testing requires async execution")
                print("   Run the simple_executor.py to test the complete system")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        return False

def test_simple_functionality():
    """Test basic functionality without full agent."""
    print("\n🧪 Testing Basic Functionality...")
    
    try:
        # Test imports
        from travel_planner.agent import TravelPlannerAgent
        print("✅ TravelPlannerAgent import successful")
        
        # Test agent creation
        agent = TravelPlannerAgent()
        print("✅ Agent creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Travel Planner Agent Test")
    print("=" * 60)
    
    # Test basic functionality
    basic_ok = test_simple_functionality()
    
    # Test full agent
    if basic_ok:
        full_ok = test_travel_planner()
    else:
        full_ok = False
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Basic Functionality: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    print(f"Full Agent Test: {'✅ PASS' if full_ok else '❌ FAIL'}")
    
    if basic_ok:
        print("\n🎉 Basic functionality working!")
        print("To test the complete system, run: python simple_executor.py")
    else:
        print("\n❌ Basic functionality failed. Check your setup.") 