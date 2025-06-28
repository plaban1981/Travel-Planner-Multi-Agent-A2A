#!/usr/bin/env python3
"""
Direct test of hotel search tools without CrewAI.
"""

import os
from dotenv import load_dotenv
from agent import HotelSearchTool, HotelBookingTool

def test_hotel_search_tool():
    """Test the hotel search tool directly."""
    print("🏨 Testing Hotel Search Tool Directly")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    if not os.getenv("SERPER_API_KEY"):
        print("❌ SERPER_API_KEY not found")
        return False
    
    try:
        # Create the search tool
        search_tool = HotelSearchTool()
        
        # Test search queries
        test_searches = [
            {
                "location": "Paris",
                "check_in": "2024-07-15",
                "check_out": "2024-07-22",
                "budget": "budget"
            },
            {
                "location": "Tokyo",
                "check_in": "2024-08-01",
                "check_out": "2024-08-07",
                "budget": "budget"
            },
            {
                "location": "New York",
                "check_in": "2024-09-10",
                "check_out": "2024-09-15",
                "budget": "budget"
            }
        ]
        
        for i, search_params in enumerate(test_searches, 1):
            print(f"\n🧪 Test {i}: {search_params['location']} ({search_params['budget']})")
            print("-" * 40)
            
            try:
                result = search_tool._run(**search_params)
                print(f"✅ Search Result:")
                print(result[:500] + "..." if len(result) > 500 else result)
                
            except Exception as e:
                print(f"❌ Search failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        return False

def test_hotel_booking_tool():
    """Test the hotel booking tool directly."""
    print("\n🏨 Testing Hotel Booking Tool Directly")
    print("=" * 50)
    
    try:
        # Create the booking tool
        booking_tool = HotelBookingTool()
        
        # Test booking
        booking_params = {
            "hotel_name": "Test Hotel Paris",
            "check_in": "2024-07-15",
            "check_out": "2024-07-22",
            "guests": 2
        }
        
        print(f"🧪 Test Booking: {booking_params}")
        print("-" * 40)
        
        result = booking_tool._run(**booking_params)
        print(f"✅ Booking Result:")
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Booking test failed: {e}")
        return False

def test_groq_connection():
    """Test Groq connection directly."""
    print("\n🧪 Testing Groq Connection...")
    
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("❌ GROQ_API_KEY not found")
        return False
    
    try:
        from langchain_groq import ChatGroq
        
        llm = ChatGroq(model="llama3-70b-8192", api_key=groq_key)
        response = llm.invoke("Hello! Please respond with 'Groq working'.")
        print(f"✅ Groq Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Direct Hotel Tools Test")
    print("=" * 60)
    
    # Test search tool
    search_ok = test_hotel_search_tool()
    
    # Test booking tool
    booking_ok = test_hotel_booking_tool()
    
    # Test Groq connection
    groq_ok = test_groq_connection()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Hotel Search Tool: {'✅ PASS' if search_ok else '❌ FAIL'}")
    print(f"Hotel Booking Tool: {'✅ PASS' if booking_ok else '❌ FAIL'}")
    print(f"Groq Connection: {'✅ PASS' if groq_ok else '❌ FAIL'}")
    
    if search_ok and booking_ok and groq_ok:
        print("\n🎉 All tools working! Now try the full agent test.")
        print("Run: python test_hotel_search.py")
    else:
        print("\n❌ Some tests failed. Check your API keys and dependencies.") 