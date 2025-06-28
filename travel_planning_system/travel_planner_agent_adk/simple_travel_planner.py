#!/usr/bin/env python3
"""
Simplified Travel Planner Agent without A2A dependencies.
This version directly communicates with the hotel and car rental agents via HTTP.
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq

class SimpleTravelPlanner:
    """Simplified travel planner that coordinates with other agents."""
    
    def __init__(self):
        """Initialize the travel planner."""
        load_dotenv()
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY not found")
        
        self.llm = ChatGroq(model="llama3-70b-8192", api_key=groq_key)
        
        # Agent endpoints
        self.hotel_agent_url = "http://localhost:10002"
        self.car_rental_agent_url = "http://localhost:10003"
        
    def check_agent_status(self):
        """Check if the other agents are running."""
        print("🔍 Checking agent status...")
        
        agents_status = {}
        
        # Check hotel agent
        try:
            response = requests.get(f"{self.hotel_agent_url}/health", timeout=5)
            if response.status_code == 200:
                agents_status["hotel"] = "✅ Running"
            else:
                agents_status["hotel"] = "❌ Not responding"
        except:
            agents_status["hotel"] = "❌ Not reachable"
        
        # Check car rental agent
        try:
            response = requests.get(f"{self.car_rental_agent_url}/health", timeout=5)
            if response.status_code == 200:
                agents_status["car_rental"] = "✅ Running"
            else:
                agents_status["car_rental"] = "❌ Not responding"
        except:
            agents_status["car_rental"] = "❌ Not reachable"
        
        return agents_status
    
    def ask_hotel_agent(self, query):
        """Ask the hotel booking agent for recommendations."""
        try:
            payload = {"message": query}
            response = requests.post(
                f"{self.hotel_agent_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]["content"]
            else:
                return f"Hotel agent error: {response.status_code}"
                
        except Exception as e:
            return f"Error communicating with hotel agent: {e}"
    
    def ask_car_rental_agent(self, query):
        """Ask the car rental agent for recommendations."""
        try:
            payload = {"message": query}
            response = requests.post(
                f"{self.car_rental_agent_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]["content"]
            else:
                return f"Car rental agent error: {response.status_code}"
                
        except Exception as e:
            return f"Error communicating with car rental agent: {e}"
    
    def plan_trip(self, query):
        """Plan a complete trip by coordinating with other agents."""
        print(f"✈️ Planning trip: {query}")
        print("=" * 60)
        
        # Check agent status
        status = self.check_agent_status()
        print("📊 Agent Status:")
        for agent, status_text in status.items():
            print(f"  {agent}: {status_text}")
        
        # Extract destination from query (simple approach)
        destination = "Paris"  # Default, can be improved with LLM extraction
        
        # Ask hotel agent for recommendations
        print(f"\n🏨 Getting hotel recommendations for {destination}...")
        hotel_query = f"Find top 10 budget-friendly hotels in {destination}"
        hotel_response = self.ask_hotel_agent(hotel_query)
        
        # Ask car rental agent for recommendations
        print(f"\n🚗 Getting car rental options for {destination}...")
        car_query = f"Find car rental options in {destination}"
        car_response = self.ask_car_rental_agent(car_query)
        
        # Create comprehensive travel plan
        print(f"\n📋 Creating comprehensive travel plan...")
        
        plan_prompt = f"""
        You are a travel planning expert. Create a comprehensive travel plan based on the following information:
        
        User Request: {query}
        Destination: {destination}
        
        Hotel Recommendations:
        {hotel_response}
        
        Car Rental Options:
        {car_response}
        
        Please create a detailed travel itinerary that includes:
        1. Summary of the trip
        2. Top hotel recommendations with prices and features
        3. Car rental options and recommendations
        4. Estimated total cost
        5. Travel tips and recommendations
        
        Format the response clearly with sections and bullet points.
        """
        
        try:
            response = self.llm.invoke(plan_prompt)
            return response.content
        except Exception as e:
            return f"Error creating travel plan: {e}"

def test_travel_planner():
    """Test the simplified travel planner."""
    print("🚀 Testing Simplified Travel Planner")
    print("=" * 60)
    
    try:
        planner = SimpleTravelPlanner()
        print("✅ Travel planner initialized successfully!")
        
        # Test queries
        test_queries = [
            "Plan a trip to Paris for next week with budget-friendly options",
            "I need a complete travel plan for Tokyo including hotel and car rental",
            "Help me plan a vacation to New York with affordable accommodations"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}: {query}")
            print("-" * 60)
            
            try:
                plan = planner.plan_trip(query)
                print(f"✅ Travel Plan:")
                print(plan)
                print("\n" + "="*60)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n🎉 Travel planner tests completed!")
        
    except Exception as e:
        print(f"❌ Error initializing travel planner: {str(e)}")

if __name__ == "__main__":
    test_travel_planner() 