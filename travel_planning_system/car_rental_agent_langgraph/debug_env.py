#!/usr/bin/env python3
"""
Debug script to check environment variables and API key format.
"""

import os
from dotenv import load_dotenv

def check_env_variables():
    """Check if environment variables are loaded correctly."""
    print("🔍 Debugging Environment Variables")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY")
    print(groq_key)
    print(f"GROQ_API_KEY found: {'✅ Yes' if groq_key else '❌ No'}")
    
    if groq_key:
        print(f"GROQ_API_KEY length: {len(groq_key)}")
        print(f"GROQ_API_KEY starts with: {groq_key[:10]}...")
        print(f"GROQ_API_KEY format check: {'✅ gsk_' if groq_key.startswith('gsk_') else '❌ Should start with gsk_'}")
        
        # Check for common issues
        if groq_key == "your_groq_api_key_here":
            print("❌ ERROR: API key is still the placeholder value!")
        elif len(groq_key) < 20:
            print("❌ ERROR: API key seems too short")
        elif not groq_key.startswith('gsk_'):
            print("❌ ERROR: API key should start with 'gsk_'")
        else:
            print("✅ API key format looks correct")
    
    # Check SERPER_API_KEY
    serper_key = os.getenv("SERPER_API_KEY")
    print(f"\nSERPER_API_KEY found: {'✅ Yes' if serper_key else '❌ No'}")
    
    if serper_key:
        print(f"SERPER_API_KEY length: {len(serper_key)}")
        print(f"SERPER_API_KEY starts with: {serper_key[:10]}...")
        
        if serper_key == "your_serper_api_key_here":
            print("❌ ERROR: SerperAPI key is still the placeholder value!")
    
    # Check .env file
    print(f"\n📁 .env file exists: {'✅ Yes' if os.path.exists('.env') else '❌ No'}")
    
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            print(f"📄 .env file content:")
            print("-" * 30)
            print(content)
            print("-" * 30)

def test_groq_connection():
    """Test Groq connection directly."""
    print("\n🧪 Testing Groq Connection Directly...")
    
    try:
        from langchain_groq import ChatGroq
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key == "your_groq_api_key_here":
            print("❌ No valid GROQ_API_KEY found")
            return False
        
        print(f"🔑 Using API key: {groq_key[:10]}...")
        
        # Test the connection
        llm = ChatGroq(model="llama3-70b-8192", api_key=groq_key)
        
        # Simple test query
        response = llm.invoke("Hello! Please respond with 'Connection successful'.")
        print(f"✅ Groq Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq connection failed: {e}")
        return False

def main():
    """Main debug function."""
    check_env_variables()
    
    print("\n" + "=" * 50)
    print("🔧 Troubleshooting Steps:")
    print("1. Make sure your .env file has the correct API key format")
    print("2. Groq API key should start with 'gsk_'")
    print("3. Get a valid API key from: https://console.groq.com/")
    print("4. Make sure there are no extra spaces or quotes in the .env file")
    print("5. Restart the agent after updating the .env file")
    
    # Test connection if API key looks good
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here" and groq_key.startswith('gsk_'):
        print("\n" + "=" * 50)
        test_groq_connection()

if __name__ == "__main__":
    main() 