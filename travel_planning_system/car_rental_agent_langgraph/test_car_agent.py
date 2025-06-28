import os
from dotenv import load_dotenv
from app.agent import CarRentalAgent

load_dotenv()

def test_car_agent():
    print("🚗 Testing Car Rental Agent with Groq Llama-3 70B")
    print("=" * 60)
    
    try:
        agent = CarRentalAgent()
        print("✅ Car Rental Agent initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Test queries
    queries = [
        "Find car rentals in Paris for next week",
        "Book a luxury car in Tokyo for 3 days",
        "What are the cheapest car rental options in New York?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 40)
        try:
            response = agent.invoke(query, f"test_context_{i}")
            print(f"✅ Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_car_agent() 