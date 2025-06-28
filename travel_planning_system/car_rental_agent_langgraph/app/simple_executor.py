"""Simplified agent executor for car rental agent (without A2A dependencies)."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

load_dotenv()
    
from agent import CarRentalAgent

app = FastAPI(title="Car Rental Agent", version="1.0.0")

# Initialize the car rental agent
car_rental_agent = CarRentalAgent()


class SimpleMessageRequest(BaseModel):
    """Simple request model for testing."""
    message: str
    car_type: str = "any"


@app.post("/chat")
async def chat(request: SimpleMessageRequest):
    """Simple chat endpoint for testing."""
    try:
        message = request.message
        if request.car_type and request.car_type != "any":
            message += f" with car type {request.car_type}"
        response = car_rental_agent.invoke(message, "test_context")
        # Ensure response is serializable (dict/list/str)
        if hasattr(response, 'model_dump'):
            response = response.model_dump()
        elif hasattr(response, 'dict'):
            response = response.dict()
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "Car_Rental_Agent"}


@app.get("/")
async def root():
    """Root endpoint with agent information."""
    return {
        "agent": "Car_Rental_Agent",
        "description": "Car rental booking agent using Groq Llama-3 70B",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10003) 