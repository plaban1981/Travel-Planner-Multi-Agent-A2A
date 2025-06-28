#!/usr/bin/env python3
"""
Quick test script for hotel booking agent.
"""

import os
import requests
from dotenv import load_dotenv

def test_hotel_search_tool():
    """Test the hotel search tool directly."""
    print("🏨 Quick Hotel Search Test")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    serper_key = os.getenv("SERPER_API_KEY")
    if not serper_key:
        print("❌ SERPER_API_KEY not found")
        return
    
    # Test search query
    search_query = "top 10 budget friendly hotels in Paris under $150 per night"
    
    print(f"🔍 Searching for: {search_query}")
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": search_query,
        "num": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Found {len(data.get('organic', []))} results")
        
        # Display top results
        for i, result in enumerate(data.get('organic', [])[:5], 1):
            print(f"\n{i}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No link')}")
            print(f"   Description: {result.get('snippet', 'No description')[:100]}...")
        
        return data
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return None

def test_groq_connection():
    """Test Groq connection."""
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
    print("🚀 Quick Hotel Booking Agent Test")
    print("=" * 50)
    
    # Test search functionality
    search_results = test_hotel_search_tool()
    
    # Test Groq connection
    groq_ok = test_groq_connection()
    
    print("\n" + "=" * 50)
    if search_results and groq_ok:
        print("✅ All tests passed! Ready to run the full agent.")
        print("Run: python test_hotel_search.py")
    else:
        print("❌ Some tests failed. Check your API keys.") 