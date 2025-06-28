#!/usr/bin/env python3
"""
Simplified Hotel Booking Agent without CrewAI.
This version directly uses the tools and LLM for better compatibility.
"""

import os
import json
from datetime import date
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from agent import HotelSearchTool, HotelBookingTool

class SimpleHotelAgent:
    """Simplified hotel booking agent without CrewAI."""
    
    def __init__(self):
        """Initialize the simple hotel agent."""
        load_dotenv()
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY not found")
        
        self.llm = ChatGroq(model="llama3-70b-8192", api_key=groq_key)
        self.search_tool = HotelSearchTool()
        self.booking_tool = HotelBookingTool()
        
    def search_hotels(self, location, check_in, check_out, budget="budget"):
        """Search for hotels using the search tool."""
        try:
            result = self.search_tool._run(
                location=location,
                check_in=check_in,
                check_out=check_out,
                budget=budget
            )
            return result
        except Exception as e:
            return f"Error searching hotels: {e}"
    
    def book_hotel(self, hotel_name, check_in, check_out, guests=1):
        """Book a hotel using the booking tool."""
        try:
            result = self.booking_tool._run(
                hotel_name=hotel_name,
                check_in=check_in,
                check_out=check_out,
                guests=guests
            )
            return result
        except Exception as e:
            return f"Error booking hotel: {e}"
    
    def process_query(self, query):
        """Process a hotel booking query."""
        print(f"🔍 Processing query: {query}")
        
        # First, search for hotels
        search_results = self.search_hotels(
            location="Paris",  # Default location, can be extracted from query
            check_in="2024-07-15",  # Default dates, can be extracted from query
            check_out="2024-07-22",
            budget="budget"
        )
        
        # Create a prompt for the LLM to analyze the results
        prompt = f"""
        You are a hotel booking specialist. The user asked: "{query}"
        
        Here are the hotel search results:
        {search_results}
        
        Please provide a comprehensive response with:
        1. Top 10 budget-friendly hotel recommendations
        2. Price ranges and amenities
        3. Guest ratings and reviews
        4. Location details
        5. Booking recommendations
        
        Format your response clearly with bullet points and sections.
        """
        
        try:
            # Get LLM response
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error processing with LLM: {e}"

def test_simple_agent():
    """Test the simple hotel agent."""
    print("🏨 Testing Simple Hotel Agent")
    print("=" * 50)
    
    try:
        agent = SimpleHotelAgent()
        print("✅ Agent initialized successfully!")
        
        # Test queries
        test_queries = [
            "Find top 10 budget-friendly hotels in Paris for next week",
            "Search for cheap hotels in Tokyo under $100 per night",
            "What are the best budget hotels in New York City?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}: {query}")
            print("-" * 60)
            
            try:
                response = agent.process_query(query)
                print(f"✅ Response:")
                print(response)
                print("\n" + "="*60)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        print("\n🎉 Simple agent tests completed!")
        
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")

if __name__ == "__main__":
    test_simple_agent() 