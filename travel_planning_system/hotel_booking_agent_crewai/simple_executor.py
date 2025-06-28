"""Simplified agent executor for hotel booking agent (without A2A dependencies)."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from agent import HotelBookingAgent

app = FastAPI(title="Hotel Booking Agent", version="1.0.0")

# Initialize the hotel booking agent
hotel_booking_agent = HotelBookingAgent()


class SimpleMessageRequest(BaseModel):
    """Simple request model for testing."""
    message: str


@app.post("/chat")
async def chat(request: SimpleMessageRequest):
    """Simple chat endpoint for testing."""
    try:
        response = hotel_booking_agent.invoke(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "Hotel_Booking_Agent"}


@app.get("/")
async def root():
    """Root endpoint with agent information."""
    return {
        "agent": "Hotel_Booking_Agent",
        "description": "Hotel booking agent using CrewAI + Groq Llama-3 70B",
        "endpoints": {
            "chat": "/chat",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10002) 