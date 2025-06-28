#!/usr/bin/env python3
"""
Check which dependencies are missing in the current environment.
"""

import importlib
import sys

def check_module(module_name):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def main():
    """Check all required dependencies."""
    print("🔍 Checking dependencies for Car Rental Agent...")
    print("=" * 50)
    
    required_modules = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "requests",
        "python-dotenv",
        "groq",
        "langchain_groq",
        "langchain_core",
        "langgraph",
        "langchain_google_genai"
    ]
    
    missing_modules = []
    available_modules = []
    
    for module in required_modules:
        if check_module(module):
            print(f"✅ {module}")
            available_modules.append(module)
        else:
            print(f"❌ {module}")
            missing_modules.append(module)
    
    print("\n" + "=" * 50)
    print(f"📊 Summary: {len(available_modules)} available, {len(missing_modules)} missing")
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("\n💡 To install missing modules, run:")
        print("pip install " + " ".join(missing_modules))
    else:
        print("\n🎉 All dependencies are available!")
    
    print(f"\n🐍 Python executable: {sys.executable}")
    print(f"📁 Python path: {sys.path[0]}")

if __name__ == "__main__":
    main() 