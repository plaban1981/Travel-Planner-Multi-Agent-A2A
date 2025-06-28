import os
from dotenv import load_dotenv
from agent import HotelBookingAgent

load_dotenv()

def test_hotel_agent():
    print("🏨 Testing Hotel Booking Agent with Groq Llama-3 70B")
    print("=" * 60)
    
    try:
        agent = HotelBookingAgent()
        print("✅ Hotel Booking Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Test queries
    queries = [
        "Find hotels in Paris for next week",
        "Book a hotel in Tokyo for 3 nights",
        "What are the best hotels in New York?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 40)
        try:
            response = agent.invoke(query)
            print(f"✅ Response: {response[:500]}...")  # Show first 500 chars
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_hotel_agent() 