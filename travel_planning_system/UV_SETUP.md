# Using UV for Virtual Environment Management

## 🚀 **What is UV?**

`uv` is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip, pip-tools, and virtualenv.

## 📋 **Installation**

### Install UV
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### Verify Installation
```bash
uv --version
```

---

## 🔧 **Creating Virtual Environments with UV**

### **Method 1: Create Virtual Environment for Each Agent**

#### **Travel Planner Agent (ADK)**
```bash
cd travel_planning_system/travel_planner_agent_adk

# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install groq langchain_groq google-adk google-generativeai a2a-sdk python-dotenv requests serper-python fastapi uvicorn
```

#### **Hotel Booking Agent (CrewAI)**
```bash
cd travel_planning_system/hotel_booking_agent_crewai

# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install groq langchain_groq crewai python-dotenv requests serper-python fastapi uvicorn pydantic
```

#### **Car Rental Agent (LangGraph)**
```bash
cd travel_planning_system/car_rental_agent_langgraph

# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install groq langchain_groq langgraph langchain-core python-dotenv requests serper-python fastapi uvicorn pydantic
```

### **Method 2: Create Single Virtual Environment for All Agents**

```bash
cd travel_planning_system

# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install all dependencies
uv pip install groq langchain_groq crewai langgraph langchain-core google-adk google-generativeai python-dotenv requests serper-python fastapi uvicorn pydantic
```

---

## 📦 **Using pyproject.toml with UV**

### **Create pyproject.toml for Each Agent**

#### **Travel Planner Agent**
```toml
[project]
name = "travel-planner-agent-adk"
version = "0.1.0"
description = "Travel Planner Agent using Google ADK"
requires-python = ">=3.10"
dependencies = [
    "groq",
    "langchain_groq",
    "google-adk>=1.2.1",
    "google-generativeai",
    "python-dotenv",
    "requests",
    "serper-python",
    "fastapi",
    "uvicorn",
]

[project.scripts]
adk = "google.adk.cli:main"
```

#### **Hotel Booking Agent**
```toml
[project]
name = "hotel-booking-agent-crewai"
version = "0.1.0"
description = "Hotel Booking Agent using CrewAI"
requires-python = ">=3.10"
dependencies = [
    "groq",
    "langchain_groq",
    "crewai>=0.70.0",
    "python-dotenv",
    "requests",
    "serper-python",
    "fastapi",
    "uvicorn",
    "pydantic",
]
```

#### **Car Rental Agent**
```toml
[project]
name = "car-rental-agent-langgraph"
version = "0.1.0"
description = "Car Rental Agent using LangGraph"
requires-python = ">=3.10"
dependencies = [
    "groq",
    "langchain_groq",
    "langgraph>=0.2.0",
    "langchain-core>=0.3.0",
    "python-dotenv",
    "requests",
    "serper-python",
    "fastapi",
    "uvicorn",
    "pydantic",
]
```

### **Install from pyproject.toml**
```bash
# Navigate to agent directory
cd travel_planning_system/travel_planner_agent_adk

# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install from pyproject.toml
uv pip install -e .
```

---

## 🎯 **Complete UV Workflow**

### **Step 1: Install UV**
```bash
# Install UV globally
pip install uv
```

### **Step 2: Create Virtual Environments**
```bash
# For each agent directory
cd travel_planning_system/travel_planner_agent_adk
uv venv
cd ../hotel_booking_agent_crewai
uv venv
cd ../car_rental_agent_langgraph
uv venv
```

### **Step 3: Install Dependencies**
```bash
# Travel Planner Agent
cd travel_planning_system/travel_planner_agent_adk
uv pip install groq langchain_groq google-adk google-generativeai python-dotenv requests serper-python fastapi uvicorn

# Hotel Booking Agent
cd ../hotel_booking_agent_crewai
uv pip install groq langchain_groq crewai python-dotenv requests serper-python fastapi uvicorn pydantic

# Car Rental Agent
cd ../car_rental_agent_langgraph
uv pip install groq langchain_groq langgraph langchain-core python-dotenv requests serper-python fastapi uvicorn pydantic
```

### **Step 4: Run Agents**
```bash
# Terminal 1: Car Rental Agent
cd travel_planning_system/car_rental_agent_langgraph
uv run python app/__main__.py

# Terminal 2: Hotel Booking Agent
cd ../hotel_booking_agent_crewai
uv run python __main__.py

# Terminal 3: Travel Planner Agent
cd ../travel_planner_agent_adk
uv run adk web
```

---

## 🔄 **UV Commands Reference**

### **Virtual Environment Management**
```bash
# Create virtual environment
uv venv

# Create virtual environment with specific Python version
uv venv --python 3.11

# Remove virtual environment
rm -rf .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### **Package Management**
```bash
# Install package
uv pip install package_name

# Install multiple packages
uv pip install package1 package2 package3

# Install from requirements.txt
uv pip install -r requirements.txt

# Install from pyproject.toml
uv pip install -e .

# Uninstall package
uv pip uninstall package_name

# List installed packages
uv pip list
```

### **Running Scripts**
```bash
# Run script in virtual environment
uv run python script.py

# Run with specific Python version
uv run --python 3.11 python script.py

# Run with environment variables
uv run --env-file .env python script.py
```

---

## 🎨 **UV vs Traditional Methods**

### **Traditional (pip + venv)**
```bash
# Create virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install packages
pip install package_name
```

### **UV (Faster)**
```bash
# Create virtual environment
uv venv

# Activate
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install packages (much faster)
uv pip install package_name
```

---

## 🚀 **Benefits of UV**

1. **Speed**: 10-100x faster than pip
2. **Reliability**: Better dependency resolution
3. **Compatibility**: Drop-in replacement for pip
4. **Cross-platform**: Works on Windows, macOS, Linux
5. **Modern**: Built with Rust for performance

---

## 🔧 **Troubleshooting**

### **Common Issues**
```bash
# If uv command not found
export PATH="$HOME/.cargo/bin:$PATH"

# If virtual environment activation fails
# Windows:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# If packages fail to install
uv pip install --upgrade pip
uv pip install package_name --force-reinstall
```

### **Check UV Installation**
```bash
# Verify UV is installed
uv --version

# Check UV location
which uv  # macOS/Linux
where uv  # Windows
```

This guide provides everything you need to use UV for managing virtual environments in your multi-agent travel planning system! 