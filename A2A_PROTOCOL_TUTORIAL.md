# Mastering Agent-to-Agent (A2A) Protocol: Complete Implementation Guide

## Table of Contents
1. [Introduction to A2A Protocol](#introduction)
2. [Architecture Overview](#architecture)
3. [Core Concepts](#core-concepts)
4. [Implementation Guide](#implementation)
5. [Testing & Debugging](#testing)
6. [Best Practices](#best-practices)
7. [Common Pitfalls](#pitfalls)

---

## 1. Introduction to A2A Protocol {#introduction}

### What is A2A?

The Agent-to-Agent (A2A) protocol is a **standardized JSON-RPC 2.0 based protocol** that enables different AI agents to communicate with each other, regardless of their underlying framework (Google ADK, CrewAI, LangGraph, etc.).

### Why Use A2A?

**Traditional Approach (Without A2A):**
```python
# Agent A (LangChain)
result_a = langchain_agent.run("task")

# Agent B (CrewAI) - Can't easily communicate with Agent A
# Need custom integration code, API wrappers, etc.
result_b = crewai_agent.kickoff(crew_inputs)
```

**With A2A Protocol:**
```python
# Agent A can talk to Agent B using standardized protocol
# regardless of frameworks
response = await a2a_client.send_message(
    agent_name="Agent_B",
    message="Complete this task"
)
```

### Benefits:

1. ✅ **Framework Agnostic** - Mix Google ADK, CrewAI, LangGraph, AutoGen
2. ✅ **Standardized Communication** - JSON-RPC 2.0 format
3. ✅ **Discoverable** - Agents expose capabilities via agent cards
4. ✅ **Production Ready** - Built on proven protocols
5. ✅ **Language Independent** - Works across Python, Node.js, etc.

---

## 2. Architecture Overview {#architecture}

### Our Travel Planning System

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          Travel Planner Agent (Orchestrator)                │
│          Framework: Google ADK                              │
│          Model: Gemini 2.5 Flash                           │
│                                                             │
│  Tools:                                                     │
│  • send_message(agent_name, task) ← A2A Communication     │
│  • search_flights(origin, destination, date)               │
│  • search_destinations(destination)                        │
│  • create_travel_itinerary(...)                           │
└────────────┬─────────────────┬─────────────────────────────┘
             │                 │
    A2A      │                 │      A2A
  Protocol   │                 │    Protocol
             ▼                 ▼
┌─────────────────────┐ ┌──────────────────────┐
│ Hotel Booking Agent │ │ Car Rental Agent     │
│ Framework: CrewAI   │ │ Framework: LangGraph │
│ Model: Groq Llama-3 │ │ Model: Groq Llama-3  │
│                     │ │                      │
│ Exposes:            │ │ Exposes:             │
│ • POST /            │ │ • POST /             │
│ • GET /health       │ │ • GET /health        │
│ • GET /.well-known/ │ │ • GET /.well-known/  │
│   agent.json        │ │   agent.json         │
└─────────────────────┘ └──────────────────────┘
```

### Communication Flow

```
1. User: "Plan a trip to Paris"
   ↓
2. Travel Planner receives request
   ↓
3. Travel Planner decides to delegate:
   - Hotel search → Hotel_Booking_Agent
   - Car rental → Car_Rental_Agent
   ↓
4. Travel Planner sends A2A messages:
   POST http://localhost:10002/
   {
     "jsonrpc": "2.0",
     "method": "message/send",
     "id": "msg-123",
     "params": {
       "message": {
         "role": "user",
         "parts": [{"kind": "text", "text": "Find hotels in Paris"}]
       }
     }
   }
   ↓
5. Hotel Agent processes and responds:
   {
     "jsonrpc": "2.0",
     "id": "msg-123",
     "result": {
       "kind": "task",
       "status": {"state": "completed"},
       "artifacts": [...]
     }
   }
   ↓
6. Travel Planner combines results
   ↓
7. User receives complete itinerary
```

---

## 3. Core Concepts {#core-concepts}

### 3.1 Agent Card (Discovery)

Every A2A agent must expose an **Agent Card** at `/.well-known/agent.json`:

```json
{
  "name": "Hotel_Booking_Agent",
  "description": "Specialized agent for hotel research and booking",
  "version": "1.0.0",
  "url": "http://localhost:10002",
  "capabilities": {},
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": []
}
```

**Purpose:**
- Describes what the agent can do
- How to reach it
- What formats it accepts

**Implementation:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/.well-known/agent.json")
async def agent_card():
    return {
        "name": "Hotel_Booking_Agent",
        "description": "Specialized agent for hotel research and booking using SerperAPI for real-time information.",
        "version": "1.0.0",
        "url": "http://localhost:10002",
        "capabilities": {},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": []
    }
```

### 3.2 JSON-RPC 2.0 Request Format

A2A uses JSON-RPC 2.0 for all communication:

```python
{
  "jsonrpc": "2.0",           # Always "2.0"
  "method": "message/send",   # The RPC method
  "id": "unique-id",          # Request identifier
  "params": {                 # Parameters
    "message": {
      "role": "user",
      "parts": [
        {
          "kind": "text",     # NOT "type"!
          "text": "Your message here"
        }
      ],
      "messageId": "msg-id",
      "taskId": "task-id",
      "contextId": "context-id"
    }
  }
}
```

**Key Points:**
- `kind`: "text" (not `type`)
- All IDs should be UUIDs
- `taskId` tracks the overall task
- `contextId` maintains conversation context

### 3.3 Response Format

```python
{
  "jsonrpc": "2.0",
  "id": "same-as-request",
  "result": {
    "kind": "task",           # NOT "type"!
    "id": "task-id",
    "contextId": "context-id",
    "status": {               # TaskStatus object
      "state": "completed",   # submitted, working, completed, failed
      "timestamp": "2025-11-23T20:00:00Z"
    },
    "artifacts": [
      {
        "artifactId": "unique-id",  # REQUIRED!
        "parts": [
          {
            "kind": "text",         # NOT "type"!
            "text": "Response data here"
          }
        ]
      }
    ]
  }
}
```

**Key Points:**
- `kind`: "task" (not `type`)
- `status` is an object, not a string
- `artifactId` is required for each artifact
- Timestamp should be ISO 8601 format

---

## 4. Implementation Guide {#implementation}

### Understanding A2A SDK Usage

**IMPORTANT:** The A2A SDK is used differently on each side:

```
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR AGENT (Travel Planner)                           │
│  ✅ Uses A2A SDK Client (a2a.client)                           │
│                                                                  │
│  from a2a.client import A2AClient, A2ACardResolver             │
│  from a2a.types import SendMessageRequest, AgentCard           │
│                                                                  │
│  Purpose: Send messages TO other agents                         │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ A2A Protocol (JSON-RPC 2.0)
                           │ POST http://localhost:10002/
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  SPECIALIZED AGENTS (Hotel, Car Rental)                        │
│  ❌ Does NOT use A2A SDK Server (doesn't exist)                │
│  ✅ Uses FastAPI + Manual A2A Protocol Implementation          │
│                                                                  │
│  from fastapi import FastAPI                                    │
│  # Manually parse A2A requests                                  │
│  # Manually format A2A responses                                │
│                                                                  │
│  Purpose: Receive messages FROM orchestrator                    │
└─────────────────────────────────────────────────────────────────┘
```

**Why This Split?**

1. **A2A SDK provides CLIENT only** (not server)
   - Helps you SEND messages
   - Handles request formatting
   - Validates responses
   - Discovers agent cards

2. **No A2A SDK server exists** (yet)
   - You implement server with any framework (FastAPI, Flask, etc.)
   - Manually parse incoming A2A requests
   - Manually format A2A responses
   - Follow A2A protocol specification

3. **FastAPI is just one choice**
   - Could use Flask, Starlette, Django, etc.
   - Could even use Node.js, Go, Rust
   - A2A is language-agnostic (JSON-RPC)

### Step 1: Set Up the Orchestrator Agent

**File: `travel_planner_agent_adk/travel_planner/agent.py`**

#### 1.1 A2A SDK Imports (CLIENT SIDE ONLY)

**What we import from A2A SDK:**

```python
import httpx  # Not part of A2A SDK, but required

# A2A SDK CLIENT components
from a2a.client import (
    A2AClient,         # Main client for sending messages
    A2ACardResolver    # Fetches and validates agent cards
)

# A2A SDK TYPE definitions (used by both client and server)
from a2a.types import (
    AgentCard,              # Type definition for agent card
    SendMessageRequest,     # Type for outgoing requests
    SendMessageResponse,    # Type for incoming responses
    MessageSendParams,      # Type for message parameters
    SendMessageSuccessResponse,  # Successful response type
    Task                    # Task result type
)
```

**What Each Component Does:**

1. **A2AClient**
   ```python
   # Creates HTTP client for A2A communication
   client = A2AClient(httpx_client=http_client, url="http://localhost:10002")

   # Sends messages using A2A protocol
   response = await client.send_message(request)
   ```

2. **A2ACardResolver**
   ```python
   # Fetches agent card from /.well-known/agent.json
   resolver = A2ACardResolver(http_client, "http://localhost:10002")
   card = await resolver.get_agent_card()
   # Returns validated AgentCard object
   ```

3. **SendMessageRequest**
   ```python
   # Type-safe request creation
   request = SendMessageRequest(
       id="msg-123",
       params=MessageSendParams.model_validate(payload)
   )
   # SDK handles: jsonrpc, method fields automatically
   ```

4. **SendMessageResponse**
   ```python
   # Parses and validates response from agent
   response: SendMessageResponse = await client.send_message(request)
   # SDK validates: structure, required fields, types
   ```

#### 1.2 Initialize with A2A Client

```python
import httpx
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    AgentCard,
    SendMessageRequest,
    SendMessageResponse,
    MessageSendParams
)

class TravelPlannerAgent:
    def __init__(self):
        # Store remote agent connections
        self.remote_agent_connections: dict[str, RemoteAgentConnections] = {}
        self.cards: dict[str, AgentCard] = {}

        # Create persistent HTTP client for A2A
        self.httpx_client = httpx.AsyncClient(timeout=30)

        # Initialize your LLM
        self.llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

        # Create the agent with tools
        self._agent = self.create_agent()
```

**Why httpx.AsyncClient?**
- A2A communication is async
- Persistent connection improves performance
- Shared across all remote agent calls

#### 1.2 Discover Remote Agents

```python
async def _async_init_components(self, remote_agent_addresses: List[str]):
    """Discover and register remote agents."""

    for address in remote_agent_addresses:
        # 1. Health check first
        if not await self.validate_agent_health(address):
            print(f"Agent at {address} failed health check")
            continue

        # 2. Fetch agent card
        card_resolver = A2ACardResolver(self.httpx_client, address)
        card = await card_resolver.get_agent_card()

        # 3. Create connection wrapper
        remote_connection = RemoteAgentConnections(
            agent_card=card,
            agent_url=address,
            httpx_client=self.httpx_client
        )

        # 4. Register agent
        self.remote_agent_connections[card.name] = remote_connection
        self.cards[card.name] = card

        print(f"✅ Registered agent: {card.name}")
```

**Key Concepts:**
1. **Health Check**: Verify agent is reachable before use
2. **Card Resolver**: Fetches and validates agent card
3. **Connection Wrapper**: Encapsulates A2A client
4. **Registration**: Store by agent name for easy lookup

#### 1.3 Implement Health Check

```python
async def validate_agent_health(self, agent_url: str) -> bool:
    """Check if agent is healthy and responding."""
    try:
        response = await self.httpx_client.get(f"{agent_url}/health", timeout=5.0)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "healthy"
        return False
    except Exception as e:
        print(f"Health check failed for {agent_url}: {e}")
        return False
```

**Why Health Checks?**
- Fail fast if agent is down
- Clear error messages
- Prevents cryptic timeout errors

#### 1.4 Send Messages to Remote Agents

```python
async def send_message(self, agent_name: str, task: str, tool_context: ToolContext):
    """Send a task to a remote agent via A2A protocol."""

    # 1. Validate agent exists
    if agent_name not in self.remote_agent_connections:
        raise ValueError(f"Agent {agent_name} not found")

    client = self.remote_agent_connections[agent_name]

    # 2. Generate IDs
    state = tool_context.state
    task_id = state.get("task_id", str(uuid.uuid4()))
    context_id = state.get("context_id", str(uuid.uuid4()))
    message_id = str(uuid.uuid4())

    # 3. Create A2A request payload
    payload = {
        "message": {
            "role": "user",
            "parts": [{"type": "text", "text": task}],  # Will be converted to "kind"
            "messageId": message_id,
            "taskId": task_id,
            "contextId": context_id,
        },
    }

    # 4. Create typed request
    message_request = SendMessageRequest(
        id=message_id,
        params=MessageSendParams.model_validate(payload)
    )

    # 5. Send via A2A client
    send_response: SendMessageResponse = await client.send_message(message_request)

    # 6. Extract artifacts from response
    response_content = send_response.root.model_dump_json(exclude_none=True)
    json_content = json.loads(response_content)

    resp = []
    if json_content.get("result", {}).get("artifacts"):
        for artifact in json_content["result"]["artifacts"]:
            if artifact.get("parts"):
                resp.extend(artifact["parts"])

    return resp
```

**Key Concepts:**
1. **ID Management**: task_id tracks the task, context_id maintains conversation
2. **Type Safety**: Use Pydantic models from A2A SDK
3. **Error Handling**: Validate response structure
4. **Artifact Extraction**: Get actual content from response

### Step 2: Create Remote Agent Wrapper

**File: `travel_planner_agent_adk/travel_planner/remote_agent_connection.py`**

```python
from a2a.client import A2AClient
from a2a.types import AgentCard

class RemoteAgentConnections:
    """Manages connections to remote agents."""

    def __init__(self, agent_card: AgentCard, agent_url: str, httpx_client):
        """Initialize the remote agent connection."""
        self.agent_card = agent_card
        self.agent_url = agent_url

        # Create A2A client with shared httpx client
        self.client = A2AClient(httpx_client=httpx_client, url=agent_url)

    async def send_message(self, message_request):
        """Send a message to the remote agent."""
        return await self.client.send_message(message_request)
```

**Why a Wrapper?**
- Encapsulates A2A client creation
- Stores agent metadata
- Easy to extend with caching, retries, etc.

### Step 3: Implement Specialized Agents

#### 3.1 Why FastAPI? (NOT A2A SDK)

**IMPORTANT: Specialized agents DO NOT use A2A SDK server components!**

```python
# ❌ There is NO A2A SDK server like this:
from a2a.server import A2AServer  # DOES NOT EXIST!

# ✅ Instead, we manually implement A2A protocol with FastAPI:
from fastapi import FastAPI

app = FastAPI()

@app.post("/")  # Manually handle A2A requests
async def handle_message(request: A2AMessageRequest):
    # Parse A2A request manually
    # Call your agent
    # Format A2A response manually
    return {...}
```

**Why Manual Implementation?**

1. **A2A SDK has no server component**
   - Only provides `a2a.client` (for sending)
   - Only provides `a2a.types` (for type definitions)
   - Server implementation is up to you

2. **FastAPI is flexible**
   - Any Python web framework works (Flask, Django, Starlette)
   - Easy to add custom middleware
   - Great async support
   - Automatic API documentation

3. **You could use other languages**
   ```javascript
   // Node.js example
   app.post('/', (req, res) => {
     const message = req.body.params.message;
     // Process and return A2A response
   });
   ```

**What we DO use from A2A SDK on server side:**

```python
# ONLY the type definitions (optional, for validation)
from a2a.types import (
    AgentCard,    # To understand agent card structure
    Task,         # To understand response format
    TaskStatus,   # To understand status structure
    # etc.
)

# These are just Pydantic models for reference
# You can manually create the JSON without them
```

#### 3.2 Create FastAPI Server

**File: `hotel_booking_agent_crewai/simple_executor.py`**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import uuid
from typing import Any, Dict
from datetime import datetime

from agent import HotelBookingAgent

app = FastAPI(title="Hotel Booking Agent", version="1.0.0")

# Initialize your agent
hotel_booking_agent = HotelBookingAgent()
```

#### 3.2 Define Request Model

```python
class A2AMessageRequest(BaseModel):
    """A2A protocol message request."""
    jsonrpc: str = "2.0"
    method: str = "message/send"
    id: str
    params: Dict[str, Any]
```

**Critical Points:**
- ✅ Include `jsonrpc` and `method` fields
- ✅ Use default values for protocol fields
- ✅ `params` is a flexible dict

#### 3.3 Implement Health Check

```python
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "Hotel_Booking_Agent"}
```

#### 3.4 Implement Agent Card

```python
@app.get("/.well-known/agent.json")
async def agent_card():
    """A2A protocol agent card endpoint."""
    return {
        "name": "Hotel_Booking_Agent",
        "description": "Specialized agent for hotel research and booking using SerperAPI for real-time information.",
        "version": "1.0.0",
        "url": "http://localhost:10002",
        "capabilities": {},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": []
    }
```

#### 3.5 Implement Message Handler

```python
@app.post("/")  # A2A client posts to root URL
async def handle_a2a_message_root(request: A2AMessageRequest):
    """A2A protocol message endpoint at root URL."""
    return await handle_a2a_message(request)

@app.post("/send_message")  # Also support explicit endpoint
async def handle_a2a_message(request: A2AMessageRequest):
    """A2A protocol message endpoint."""
    try:
        # 1. Extract message from A2A request
        message_params = request.params.get("message", {})
        parts = message_params.get("parts", [])

        # 2. Get text from message parts
        user_message = ""
        for part in parts:
            # Check both "kind" and "type" for compatibility
            if part.get("kind") == "text" or part.get("type") == "text":
                user_message = part.get("text", "")
                break

        if not user_message:
            raise HTTPException(status_code=400, detail="No text found in message")

        # 3. Process with your agent
        response = hotel_booking_agent.invoke(user_message)

        # 4. Create A2A response format
        task_id = message_params.get("taskId", str(uuid.uuid4()))
        context_id = message_params.get("contextId", str(uuid.uuid4()))

        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "result": {
                "kind": "task",  # NOT "type"!
                "id": task_id,
                "contextId": context_id,
                "status": {      # TaskStatus object
                    "state": "completed",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                "artifacts": [
                    {
                        "artifactId": str(uuid.uuid4()),  # REQUIRED!
                        "parts": [
                            {
                                "kind": "text",  # NOT "type"!
                                "text": str(response)
                            }
                        ]
                    }
                ]
            }
        }
    except Exception as e:
        # Return A2A error response
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32000,
                "message": f"Error processing message: {str(e)}"
            }
        }
```

**Critical Implementation Details:**

1. **Dual Endpoint Support:**
   - `POST /` - Where A2A client sends requests
   - `POST /send_message` - Explicit endpoint for testing

2. **Message Extraction:**
   ```python
   # Extract from nested structure
   message_params = request.params.get("message", {})
   parts = message_params.get("parts", [])
   ```

3. **Field Naming:**
   - Use `"kind"` not `"type"`
   - Check both for compatibility

4. **Response Structure:**
   ```python
   {
     "kind": "task",           # NOT "type"
     "status": {               # Object, not string
       "state": "completed",
       "timestamp": "ISO 8601"
     },
     "artifacts": [{
       "artifactId": "uuid",   # REQUIRED
       "parts": [...]
     }]
   }
   ```

5. **Error Handling:**
   - Return JSON-RPC error format
   - Include meaningful error messages

#### 3.6 Start the Server

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10002)
```

### Step 4: Connect Everything

**File: `travel_planner_agent_adk/travel_planner/agent.py`**

```python
@classmethod
async def create(cls, remote_agent_addresses: List[str]):
    """Factory method to create initialized agent."""
    instance = cls()
    await instance._async_init_components(remote_agent_addresses)
    return instance

# At module level
def _get_initialized_travel_planner_agent_sync():
    """Synchronously creates and initializes the TravelPlannerAgent."""

    async def _async_main():
        # Define agent URLs
        agent_urls = [
            "http://localhost:10002",  # Hotel Booking Agent
            "http://localhost:10003",  # Car Rental Agent
        ]

        # Create and initialize
        travel_planner_instance = await TravelPlannerAgent.create(
            remote_agent_addresses=agent_urls
        )

        return travel_planner_instance.create_agent()

    # Handle event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Use nest_asyncio if loop already running
        import nest_asyncio
        nest_asyncio.apply()
        return asyncio.run(_async_main())
    else:
        # Create new event loop
        return asyncio.run(_async_main())

# Create the root agent
root_agent = _get_initialized_travel_planner_agent_sync()
```

**Why This Pattern?**
- Google ADK expects synchronous agent creation
- A2A requires async operations
- `nest_asyncio` handles nested event loops

---

## 4.5 A2A SDK Usage Summary

### Complete Component Breakdown

| Component | Orchestrator (Client) | Specialized Agent (Server) |
|-----------|----------------------|----------------------------|
| **A2A SDK Client** | ✅ YES - `A2AClient` | ❌ NO |
| **A2A SDK Types** | ✅ YES - For validation | ⚠️ Optional - For reference |
| **Card Resolver** | ✅ YES - `A2ACardResolver` | ❌ NO |
| **FastAPI** | ❌ NO | ✅ YES - Manual server |
| **httpx** | ✅ YES - HTTP client | ❌ NO (FastAPI handles) |
| **Pydantic** | ✅ YES - Via A2A types | ✅ YES - Request models |

### Import Comparison

**Orchestrator (Travel Planner):**
```python
# A2A SDK imports - Used extensively
from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    AgentCard,
    SendMessageRequest,
    SendMessageResponse,
    MessageSendParams,
    SendMessageSuccessResponse,
    Task
)

# HTTP client for A2A
import httpx

# Your framework (Google ADK)
from google.adk import Agent
```

**Specialized Agent (Hotel/Car):**
```python
# NO A2A SDK client imports!

# Web framework (your choice)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Standard library for A2A protocol implementation
import uuid
import json
from datetime import datetime
from typing import Any, Dict

# Your agent framework (CrewAI, LangGraph, etc.)
from agent import HotelBookingAgent
```

### What A2A SDK Actually Does

**On Client Side (Orchestrator):**
```python
# 1. A2AClient handles all this for you:
request = SendMessageRequest(
    id="msg-123",
    params=MessageSendParams.model_validate({
        "message": {
            "role": "user",
            "parts": [{"type": "text", "text": "Find hotels"}],
            # ...
        }
    })
)

# SDK automatically adds:
# - jsonrpc: "2.0"
# - method: "message/send"
# - Validates all fields
# - Serializes to JSON

response = await client.send_message(request)

# SDK automatically:
# - Sends HTTP POST
# - Parses response JSON
# - Validates response structure
# - Returns typed object
```

**On Server Side (Specialized Agents):**
```python
# You manually implement everything:

@app.post("/")
async def handle_message(request: A2AMessageRequest):
    # 1. You parse the request
    message_params = request.params.get("message", {})
    parts = message_params.get("parts", [])
    text = parts[0].get("text")

    # 2. You call your agent
    response = your_agent.invoke(text)

    # 3. You manually format A2A response
    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "result": {
            "kind": "task",
            "id": task_id,
            "contextId": context_id,
            "status": {
                "state": "completed",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            },
            "artifacts": [{
                "artifactId": str(uuid.uuid4()),
                "parts": [{"kind": "text", "text": str(response)}]
            }]
        }
    }
```

### Could You Use A2A Types on Server?

**Yes, but it's optional:**

```python
# Option 1: Manual (what we did)
return {
    "jsonrpc": "2.0",
    "id": request.id,
    "result": {
        "kind": "task",
        # ... manually construct
    }
}

# Option 2: Using A2A types (more verbose)
from a2a.types import Task, TaskStatus, TaskState, Artifact, TextPart

task = Task(
    kind="task",
    id=task_id,
    contextId=context_id,
    status=TaskStatus(
        state=TaskState.completed,
        timestamp=datetime.utcnow().isoformat() + "Z"
    ),
    artifacts=[
        Artifact(
            artifactId=str(uuid.uuid4()),
            parts=[
                TextPart(kind="text", text=str(response))
            ]
        )
    ]
)

return {
    "jsonrpc": "2.0",
    "id": request.id,
    "result": task.model_dump(exclude_none=True)
}
```

**We chose manual because:**
- ✅ Simpler and more direct
- ✅ Less imports and dependencies
- ✅ Easier to understand
- ✅ Same result

---

## 5. Testing & Debugging {#testing}

### 5.1 Manual Testing with curl

**Test Health Check:**
```bash
curl http://localhost:10002/health
# Expected: {"status":"healthy","agent":"Hotel_Booking_Agent"}
```

**Test Agent Card:**
```bash
curl http://localhost:10002/.well-known/agent.json
# Expected: Full agent card JSON
```

**Test Message Sending:**
```bash
curl -X POST http://localhost:10002/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "id": "test-123",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Find hotels in Paris"
          }
        ],
        "messageId": "msg-123",
        "taskId": "task-123",
        "contextId": "ctx-123"
      }
    }
  }'
```

### 5.2 Enhanced Logging

**Add to send_message:**
```python
async def send_message(self, agent_name: str, task: str, tool_context: ToolContext):
    debug_log_file = "a2a_debug.log"

    # Log outgoing request
    with open(debug_log_file, "a") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"OUTGOING MESSAGE TO: {agent_name}\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Task: {task}\n")
        f.write(f"Full Payload:\n{json.dumps(payload, indent=2)}\n")
        f.write("="*80 + "\n")

    send_response = await client.send_message(message_request)

    # Log incoming response
    with open(debug_log_file, "a") as f:
        f.write(f"INCOMING RESPONSE FROM: {agent_name}\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Full Response:\n{json.dumps(response_dict, indent=2)}\n")
        f.write("="*80 + "\n\n")
```

**Benefits:**
- Complete audit trail
- Easy to debug message flow
- Timestamps for performance analysis

### 5.3 Using A2A Inspector

**Install:**
```bash
cd /path/to/your/projects
git clone https://github.com/a2aproject/a2a-inspector.git
cd a2a-inspector
uv sync
cd frontend
npm install
cd ..
bash scripts/run.sh
```

**Use:**
1. Open `http://127.0.0.1:5001`
2. Enter agent URL: `http://localhost:10002`
3. Click "Connect"
4. View agent card
5. Send test messages
6. View raw JSON-RPC in debug console

**Features:**
- Visual agent card validation
- Interactive message sending
- Real-time protocol compliance checking
- Debug console showing raw messages

---

## 6. Best Practices {#best-practices}

### 6.1 Error Handling

**Always return proper JSON-RPC errors:**
```python
try:
    # Process message
    response = agent.invoke(message)
    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "result": {...}
    }
except Exception as e:
    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "error": {
            "code": -32000,  # Server error
            "message": str(e),
            "data": {        # Optional additional info
                "traceback": traceback.format_exc()
            }
        }
    }
```

### 6.2 ID Management

**Use UUIDs consistently:**
```python
import uuid

# Generate IDs
message_id = str(uuid.uuid4())
task_id = str(uuid.uuid4())
context_id = str(uuid.uuid4())
artifact_id = str(uuid.uuid4())

# Reuse IDs from request
task_id = message_params.get("taskId", str(uuid.uuid4()))
context_id = message_params.get("contextId", str(uuid.uuid4()))
```

### 6.3 Timeout Configuration

**Set appropriate timeouts:**
```python
# For A2A client
self.httpx_client = httpx.AsyncClient(timeout=30)

# For health checks
response = await self.httpx_client.get(
    f"{agent_url}/health",
    timeout=5.0  # Shorter timeout for health checks
)
```

### 6.4 State Management

**Maintain conversation context:**
```python
# Store in tool context
state = tool_context.state
state["task_id"] = task_id
state["context_id"] = context_id
state["conversation_history"] = messages

# Reuse in subsequent calls
task_id = state.get("task_id", str(uuid.uuid4()))
```

### 6.5 Validation

**Validate agent responses:**
```python
if not isinstance(send_response.root, SendMessageSuccessResponse):
    raise ValueError("Received error response from agent")

if not isinstance(send_response.root.result, Task):
    raise ValueError("Response is not a Task")

if send_response.root.result.status.state != "completed":
    print(f"Task not completed: {send_response.root.result.status.state}")
```

### 6.6 Resource Cleanup

**Close httpx clients properly:**
```python
class TravelPlannerAgent:
    def __init__(self):
        self.httpx_client = httpx.AsyncClient(timeout=30)

    async def cleanup(self):
        """Cleanup resources."""
        await self.httpx_client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
```

---

## 7. Common Pitfalls {#pitfalls}

### Pitfall 1: Using `"type"` Instead of `"kind"`

❌ **Wrong:**
```python
{
    "type": "task",
    "artifacts": [{
        "type": "text",
        "parts": [{"type": "text", "text": "..."}]
    }]
}
```

✅ **Correct:**
```python
{
    "kind": "task",
    "artifacts": [{
        "artifactId": "uuid",
        "parts": [{"kind": "text", "text": "..."}]
    }]
}
```

### Pitfall 2: Status as String

❌ **Wrong:**
```python
{
    "result": {
        "kind": "task",
        "status": "completed"  # String
    }
}
```

✅ **Correct:**
```python
{
    "result": {
        "kind": "task",
        "status": {            # Object
            "state": "completed",
            "timestamp": "2025-11-23T20:00:00Z"
        }
    }
}
```

### Pitfall 3: Missing artifactId

❌ **Wrong:**
```python
{
    "artifacts": [{
        "parts": [...]  # Missing artifactId
    }]
}
```

✅ **Correct:**
```python
{
    "artifacts": [{
        "artifactId": str(uuid.uuid4()),  # Required!
        "parts": [...]
    }]
}
```

### Pitfall 4: Missing jsonrpc and method in Request Model

❌ **Wrong:**
```python
class A2AMessageRequest(BaseModel):
    id: str
    params: Dict[str, Any]
    # Missing jsonrpc and method!
```

✅ **Correct:**
```python
class A2AMessageRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str = "message/send"
    id: str
    params: Dict[str, Any]
```

### Pitfall 5: Posting to Wrong Endpoint

❌ **Wrong:**
```python
# A2A client posts to root URL, not /send_message
# Only having @app.post("/send_message") will fail
```

✅ **Correct:**
```python
@app.post("/")  # A2A client uses root URL
async def handle_a2a_message_root(request: A2AMessageRequest):
    return await handle_a2a_message(request)

@app.post("/send_message")  # Also support explicit endpoint
async def handle_a2a_message(request: A2AMessageRequest):
    # Implementation
```

### Pitfall 6: httpx Client Lifecycle

❌ **Wrong:**
```python
async def init(self):
    async with httpx.AsyncClient() as client:
        # Client closes when exiting context
        self.client = A2AClient(httpx_client=client, url=url)
    # Client is now closed!
```

✅ **Correct:**
```python
def __init__(self):
    # Create persistent client
    self.httpx_client = httpx.AsyncClient(timeout=30)
    self.client = A2AClient(httpx_client=self.httpx_client, url=url)
```

### Pitfall 7: Not Handling Both "kind" and "type"

❌ **Wrong:**
```python
for part in parts:
    if part.get("type") == "text":  # Only checks "type"
        user_message = part.get("text", "")
```

✅ **Correct:**
```python
for part in parts:
    # Check both for compatibility
    if part.get("kind") == "text" or part.get("type") == "text":
        user_message = part.get("text", "")
```

---

## 8. Advanced Topics

### 8.1 Streaming Responses

```python
from a2a.types import SendStreamingMessageRequest

async def send_message_streaming(self, agent_name: str, task: str):
    """Stream responses from agent."""
    client = self.remote_agent_connections[agent_name]

    request = SendStreamingMessageRequest(
        id=str(uuid.uuid4()),
        params=MessageSendParams.model_validate(payload)
    )

    async for response in client.send_message_streaming(request):
        # Handle incremental updates
        if response.kind == "status-update":
            print(f"Status: {response.status.state}")
        elif response.kind == "artifact-update":
            print(f"Artifact: {response.artifact}")
```

### 8.2 Task Management

```python
from a2a.types import GetTaskRequest

async def get_task_status(self, task_id: str):
    """Query task status."""
    request = GetTaskRequest(
        id=str(uuid.uuid4()),
        params=TaskQueryParams(id=task_id)
    )

    response = await client.get_task(request)
    return response.result.status
```

### 8.3 Error Recovery

```python
async def send_message_with_retry(
    self,
    agent_name: str,
    task: str,
    max_retries: int = 3
):
    """Send message with automatic retry."""
    for attempt in range(max_retries):
        try:
            return await self.send_message(agent_name, task, tool_context)
        except httpx.HTTPError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Retry {attempt + 1}/{max_retries} after error: {e}")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## 9. Complete Example: End-to-End Flow

### Scenario: User asks "Plan a trip to Paris"

**1. Travel Planner receives user request:**
```python
# In Google ADK agent
async def stream(self, query: str, session_id: str):
    # User query: "Plan a trip to Paris for December 25-29, 2025"
    # Gemini decides to use send_message tool
    pass
```

**2. Travel Planner calls send_message:**
```python
# Gemini calls
await send_message(
    agent_name="Hotel_Booking_Agent",
    task="Find hotels in Paris for December 25-29, 2025",
    tool_context=context
)
```

**3. A2A request sent:**
```json
POST http://localhost:10002/
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "msg-abc123",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "Find hotels in Paris for December 25-29, 2025"
        }
      ],
      "messageId": "msg-abc123",
      "taskId": "task-xyz789",
      "contextId": "ctx-def456"
    }
  }
}
```

**4. Hotel Agent receives and processes:**
```python
# In hotel_booking_agent/simple_executor.py
@app.post("/")
async def handle_a2a_message_root(request: A2AMessageRequest):
    # Extract message
    message_params = request.params.get("message", {})
    user_message = message_params["parts"][0]["text"]

    # Process with CrewAI
    response = hotel_booking_agent.invoke(user_message)
    # Response: List of hotels with prices

    # Return A2A response
    return {
        "jsonrpc": "2.0",
        "id": "msg-abc123",
        "result": {
            "kind": "task",
            "id": "task-xyz789",
            "contextId": "ctx-def456",
            "status": {
                "state": "completed",
                "timestamp": "2025-11-23T20:00:00Z"
            },
            "artifacts": [{
                "artifactId": "artifact-123",
                "parts": [{
                    "kind": "text",
                    "text": "[{\"name\": \"Hotel Astoria\", \"price\": \"$80\"}]"
                }]
            }]
        }
    }
```

**5. Travel Planner receives response:**
```python
# Extract artifacts
artifacts = response.root.result.artifacts
hotel_data = artifacts[0].parts[0].text
# hotel_data = "[{\"name\": \"Hotel Astoria\", \"price\": \"$80\"}]"
```

**6. Travel Planner repeats for Car Rental:**
```python
await send_message(
    agent_name="Car_Rental_Agent",
    task="Find car rentals in Paris for December 25-29, 2025",
    tool_context=context
)
```

**7. Travel Planner combines results:**
```python
await create_travel_itinerary(
    destination="Paris",
    dates="December 25-29, 2025",
    hotels=hotel_data,
    car_rentals=car_data,
    flights=flight_data,
    tool_context=context
)
```

**8. User receives complete itinerary:**
```json
{
  "destination": "Paris",
  "travel_dates": "December 25-29, 2025",
  "flights": [...],
  "hotels": [{"name": "Hotel Astoria", "price": "$80"}],
  "car_rentals": [...],
  "created_at": "2025-11-23T20:00:00",
  "status": "planned"
}
```

---

## 10. Summary & Next Steps

### What You've Learned

✅ **A2A Protocol Fundamentals**
- JSON-RPC 2.0 structure
- Agent cards and discovery
- Request/response formats

✅ **Implementation Patterns**
- Orchestrator agent with A2A client
- Specialized agents with FastAPI
- Error handling and validation

✅ **Best Practices**
- Health checks
- Enhanced logging
- Proper field naming (`kind` vs `type`)

✅ **Debugging Techniques**
- Manual testing with curl
- A2A Inspector
- Debug logging

### Architecture Mastered

```
Orchestrator (Google ADK)
    │
    ├─→ A2A Client
    │   ├─→ httpx.AsyncClient
    │   ├─→ AgentCard Discovery
    │   └─→ SendMessageRequest/Response
    │
    └─→ Remote Agents
        ├─→ FastAPI Server
        ├─→ Health Check
        ├─→ Agent Card Endpoint
        └─→ Message Handler
```

### Next Steps

1. **Add More Agents:**
   - Flight booking agent
   - Restaurant recommendation agent
   - Activity planning agent

2. **Implement Advanced Features:**
   - Streaming responses
   - Task cancellation
   - Push notifications

3. **Production Readiness:**
   - Add authentication
   - Rate limiting
   - Monitoring and metrics
   - Error tracking

4. **Optimization:**
   - Caching agent cards
   - Connection pooling
   - Batch requests

### Resources

- **A2A Specification:** https://github.com/a2aproject/A2A
- **A2A Inspector:** https://github.com/a2aproject/a2a-inspector
- **Example Projects:** https://github.com/bhancockio/agent2agent
- **This Project:** Your working travel planning system!

### Congratulations!

You now have a complete understanding of the A2A protocol and can build production-ready multi-agent systems that work across different AI frameworks!

---

## Appendix: Quick Reference

### A2A Request Structure
```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "uuid",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "..."}],
      "messageId": "uuid",
      "taskId": "uuid",
      "contextId": "uuid"
    }
  }
}
```

### A2A Response Structure
```json
{
  "jsonrpc": "2.0",
  "id": "uuid",
  "result": {
    "kind": "task",
    "id": "uuid",
    "contextId": "uuid",
    "status": {
      "state": "completed",
      "timestamp": "ISO 8601"
    },
    "artifacts": [{
      "artifactId": "uuid",
      "parts": [{"kind": "text", "text": "..."}]
    }]
  }
}
```

### Key Field Names
- ✅ `kind` (not `type`)
- ✅ `artifactId` (required)
- ✅ `status` as object (not string)
- ✅ `state` for status value

### Common HTTP Codes
- 200: Success
- 400: Bad request (missing text, invalid format)
- 405: Method not allowed (missing POST endpoint)
- 500: Server error
- 503: Service unavailable

---

**End of Tutorial**

*Last Updated: November 23, 2025*
*Based on: Travel Planning Multi-Agent A2A System*
