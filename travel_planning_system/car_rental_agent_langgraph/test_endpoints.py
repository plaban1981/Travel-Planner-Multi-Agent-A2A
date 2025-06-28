#!/usr/bin/env python3
"""
Test script for the running Car Rental Agent endpoints.
Make sure the agent is running on http://localhost:10003 before running this script.
"""

import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_health_endpoint():
    """Test the health check endpoint."""
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get("http://localhost:10003/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data}")
            return True
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    print("\n🏠 Testing Root Endpoint...")
    try:
        response = requests.get("http://localhost:10003/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root Endpoint: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Root Endpoint Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root Endpoint Error: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a car rental query."""
    print("\n💬 Testing Chat Endpoint...")
    
    test_queries = [
        "Find car rentals in Paris for next week",
        "I need a luxury car in Tokyo from 2024-06-15 to 2024-06-22",
        "What are the best car rental options in New York?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 Test Query {i}: {query}")
        print("-" * 50)
        
        try:
            payload = {"message": query}
            response = requests.post(
                "http://localhost:10003/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response: {json.dumps(data, indent=2)}")
            else:
                print(f"❌ Chat Failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Chat Error: {e}")

def main():
    """Main test function."""
    print("🚗 Testing Car Rental Agent Endpoints")
    print("=" * 60)
    print("Make sure the agent is running on http://localhost:10003")
    print("=" * 60)
    
    # Test all endpoints
    health_ok = test_health_endpoint()
    root_ok = test_root_endpoint()
    
    if health_ok and root_ok:
        print("\n✅ Basic endpoints working! Testing chat functionality...")
        test_chat_endpoint()
    else:
        print("\n❌ Basic endpoints failed. Please check if the agent is running.")
    
    print("\n" + "=" * 60)
    print("🎯 Manual Testing:")
    print("1. Open your browser and go to: http://localhost:10003")
    print("2. Check health: http://localhost:10003/health")
    print("3. Use curl or Postman to test the chat endpoint:")
    print("   curl -X POST http://localhost:10003/chat \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"message\": \"Find car rentals in Paris\"}'")

if __name__ == "__main__":
    main() 