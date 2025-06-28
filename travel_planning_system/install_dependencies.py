#!/usr/bin/env python3
"""
Installation script for the multi-agent travel planning system.
This script handles dependency conflicts and ensures all agents can run properly.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        print(f"✓ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return None

def install_agent_dependencies(agent_path):
    """Install dependencies for a specific agent."""
    print(f"\n📦 Installing dependencies for {agent_path.name}...")
    
    # First, upgrade pip
    run_command("python -m pip install --upgrade pip", cwd=agent_path)
    
    # Install core dependencies first
    core_deps = [
        "python-dotenv",
        "requests",
        "fastapi",
        "uvicorn",
        "pydantic",
        "groq"
    ]
    
    for dep in core_deps:
        run_command(f"pip install {dep}", cwd=agent_path)
    
    # Install langchain ecosystem with compatible versions
    langchain_deps = [
        "langchain>=0.2.0",
        "langchain-core>=0.3.0",
        "langchain-community>=0.2.0",
        "langchain-groq>=0.3.0"
    ]
    
    for dep in langchain_deps:
        run_command(f"pip install {dep}", cwd=agent_path)
    
    # Install agent-specific dependencies
    if "car_rental_agent_langgraph" in str(agent_path):
        run_command("pip install langgraph>=0.5.0", cwd=agent_path)
        run_command("pip install langchain-google-genai>=2.0.0", cwd=agent_path)
    elif "hotel_booking_agent_crewai" in str(agent_path):
        run_command("pip install crewai>=0.70.0", cwd=agent_path)
    elif "travel_planner_agent_adk" in str(agent_path):
        run_command("pip install google-adk>=1.2.1", cwd=agent_path)
        run_command("pip install nest-asyncio>=1.6.0", cwd=agent_path)
        run_command("pip install click", cwd=agent_path)
        run_command("pip install google-generativeai", cwd=agent_path)
        run_command("pip install httpx", cwd=agent_path)

def main():
    """Main installation function."""
    print("🚀 Multi-Agent Travel Planning System - Dependency Installation")
    print("=" * 60)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    print(f"Working directory: {current_dir}")
    
    # Find all agent directories
    agent_dirs = [
        current_dir / "car_rental_agent_langgraph",
        current_dir / "hotel_booking_agent_crewai", 
        current_dir / "travel_planner_agent_adk"
    ]
    
    # Verify all directories exist
    for agent_dir in agent_dirs:
        if not agent_dir.exists():
            print(f"❌ Error: Agent directory {agent_dir} not found!")
            return 1
    
    # Install dependencies for each agent
    for agent_dir in agent_dirs:
        install_agent_dependencies(agent_dir)
    
    print("\n✅ Installation completed!")
    print("\n📋 Next steps:")
    print("1. Create .env files in each agent directory with your API keys")
    print("2. Test individual agents using their simple_executor.py files")
    print("3. Run the full multi-agent system using the travel planner agent")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 