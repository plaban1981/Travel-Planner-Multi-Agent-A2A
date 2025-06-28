#!/usr/bin/env python3
"""
UV Virtual Environment Setup Script for Multi-Agent Travel Planning System

This script automates the creation and setup of virtual environments for all agents
using UV package manager.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_uv_installation():
    """Check if UV is installed."""
    print("🔍 Checking UV installation...")
    result = run_command("uv --version", check=False)
    if result:
        print(f"✅ UV is installed: {result}")
        return True
    else:
        print("❌ UV is not installed. Please install it first:")
        print("   pip install uv")
        return False

def create_virtual_environment(agent_path, agent_name):
    """Create virtual environment for a specific agent."""
    print(f"\n🏗️  Setting up {agent_name}...")
    
    # Navigate to agent directory
    os.chdir(agent_path)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Create virtual environment
    print("🔧 Creating virtual environment...")
    result = run_command("uv venv")
    if not result:
        print(f"❌ Failed to create virtual environment for {agent_name}")
        return False
    
    # Determine activation script path
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(agent_path, ".venv", "Scripts", "activate")
        python_path = os.path.join(agent_path, ".venv", "Scripts", "python.exe")
    else:  # Unix/Linux/macOS
        activate_script = os.path.join(agent_path, ".venv", "bin", "activate")
        python_path = os.path.join(agent_path, ".venv", "bin", "python")
    
    print(f"✅ Virtual environment created for {agent_name}")
    return True

def install_dependencies(agent_path, agent_name, dependencies):
    """Install dependencies for a specific agent."""
    print(f"📦 Installing dependencies for {agent_name}...")
    
    # Install dependencies using UV
    deps_str = " ".join(dependencies)
    command = f"uv pip install {deps_str}"
    
    result = run_command(command, cwd=agent_path)
    if result:
        print(f"✅ Dependencies installed for {agent_name}")
        return True
    else:
        print(f"❌ Failed to install dependencies for {agent_name}")
        return False

def main():
    """Main setup function."""
    print("🚀 Multi-Agent Travel Planning System - UV Setup")
    print("=" * 60)
    
    # Check UV installation
    if not check_uv_installation():
        sys.exit(1)
    
    # Define project structure
    base_path = Path(__file__).parent
    agents = {
        "travel_planner_agent_adk": {
            "dependencies": [
                "groq",
                "langchain_groq", 
                "google-adk>=1.2.1",
                "google-generativeai",
                "python-dotenv",
                "requests",
                "serper-python",
                "fastapi",
                "uvicorn",
                "httpx",
                "nest-asyncio"
            ]
        },
        "hotel_booking_agent_crewai": {
            "dependencies": [
                "groq",
                "langchain_groq",
                "crewai>=0.70.0",
                "python-dotenv",
                "requests",
                "serper-python",
                "fastapi",
                "uvicorn",
                "pydantic"
            ]
        },
        "car_rental_agent_langgraph": {
            "dependencies": [
                "groq",
                "langchain_groq",
                "langgraph>=0.2.0",
                "langchain-core>=0.3.0",
                "python-dotenv",
                "requests",
                "serper-python",
                "fastapi",
                "uvicorn",
                "pydantic"
            ]
        }
    }
    
    # Create .env file if it doesn't exist
    env_file = base_path / ".env"
    if not env_file.exists():
        print("\n📝 Creating .env file...")
        env_content = """# API Keys for Travel Planning Multi-Agent System
GROQ_API_KEY="your_groq_api_key_here"
SERPER_API_KEY="your_serper_api_key_here"
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created. Please add your API keys.")
    
    # Setup each agent
    success_count = 0
    for agent_name, config in agents.items():
        agent_path = base_path / agent_name
        
        if not agent_path.exists():
            print(f"❌ Agent directory not found: {agent_path}")
            continue
        
        # Create virtual environment
        if create_virtual_environment(agent_path, agent_name):
            # Install dependencies
            if install_dependencies(agent_path, agent_name, config["dependencies"]):
                success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Setup Summary")
    print("=" * 60)
    print(f"✅ Successfully set up {success_count}/{len(agents)} agents")
    
    if success_count == len(agents):
        print("\n🎉 All agents are ready!")
        print("\n🚀 Next steps:")
        print("1. Add your API keys to the .env file")
        print("2. Test individual agents:")
        print("   cd hotel_booking_agent_crewai && uv run python test_hotel_agent.py")
        print("   cd car_rental_agent_langgraph && uv run python test_car_agent.py")
        print("3. Run the full system:")
        print("   # Terminal 1: cd car_rental_agent_langgraph && uv run python app/__main__.py")
        print("   # Terminal 2: cd hotel_booking_agent_crewai && uv run python __main__.py")
        print("   # Terminal 3: cd travel_planner_agent_adk && uv run adk web")
    else:
        print(f"⚠️  {len(agents) - success_count} agents failed to setup")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main() 