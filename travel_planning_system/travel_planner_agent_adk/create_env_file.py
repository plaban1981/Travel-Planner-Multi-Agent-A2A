#!/usr/bin/env python3
"""
Script to help create .env files for the travel planner agent.
"""

import os

def create_env_file():
    """Create .env file with template API keys."""
    env_content = """# Travel Planner Agent Environment Variables
# Replace with your actual API keys

# Groq API Key for Llama-3 70B LLM
# Get your API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here

# Google API Key for ADK functionality
# Get your API key from: https://console.cloud.google.com/
GOOGLE_API_KEY=your_google_api_key_here

# SerperAPI Key for web search functionality
# Get your API key from: https://serper.dev/
SERPER_API_KEY=your_serper_api_key_here
"""
    
    env_file_path = ".env"
    
    if os.path.exists(env_file_path):
        print(f"⚠️  {env_file_path} already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled.")
            return
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file_path}")
        print("\n📝 Next steps:")
        print("1. Edit the .env file and replace 'your_groq_api_key_here' with your actual Groq API key")
        print("2. Replace 'your_google_api_key_here' with your actual Google API key")
        print("3. Replace 'your_serper_api_key_here' with your actual SerperAPI key")
        print("4. Save the file")
        print("5. Run: python simple_executor.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def check_env_file():
    """Check if .env file exists and has API keys."""
    if not os.path.exists(".env"):
        print("❌ .env file not found!")
        create_env_file()
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    print("🔍 Checking .env file...")
    print(f"GROQ_API_KEY: {'✅ Set' if groq_key and groq_key != 'your_groq_api_key_here' else '❌ Not set or placeholder'}")
    print(f"GOOGLE_API_KEY: {'✅ Set' if google_key and google_key != 'your_google_api_key_here' else '❌ Not set or placeholder'}")
    print(f"SERPER_API_KEY: {'✅ Set' if serper_key and serper_key != 'your_serper_api_key_here' else '❌ Not set or placeholder'}")
    
    if not groq_key or groq_key == 'your_groq_api_key_here':
        print("\n⚠️  Please set your GROQ_API_KEY in the .env file")
        return False
    
    return True

if __name__ == "__main__":
    print("🔧 Travel Planner Agent Environment Setup Helper")
    print("=" * 55)
    
    if check_env_file():
        print("\n✅ Environment is properly configured!")
        print("You can now run: python simple_executor.py")
    else:
        print("\n❌ Environment needs configuration.")
        print("Please set up your API keys and try again.") 