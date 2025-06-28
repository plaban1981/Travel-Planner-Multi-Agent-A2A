"""Agent executor for hotel booking agent."""

import json
from typing import Any, Dict, List

from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse,
    SendMessageSuccessResponse,
    Task,
    TaskArtifact,
    TaskArtifactPart,
)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agent import HotelBookingAgent

app = FastAPI(title="Hotel Booking Agent", version="1.0.0")

# Initialize the hotel booking agent
hotel_booking_agent = HotelBookingAgent()


class MessageRequest(BaseModel):
    """Request model for incoming messages."""

    message: Message


@app.post("/send_message")
async def send_message(request: SendMessageRequest) -> SendMessageResponse:
    """Handle incoming messages and return responses."""
    try:
        # Extract the user's question from the message
        user_message = request.params.message
        user_text = ""
        
        if user_message.parts:
            for part in user_message.parts:
                if hasattr(part, 'text') and part.text:
                    user_text += part.text
        
        if not user_text:
            raise HTTPException(status_code=400, detail="No text content found in message")
        
        # Process the request using the hotel booking agent
        response_text = hotel_booking_agent.invoke(user_text)
        
        # Create response artifacts
        artifact_part = TaskArtifactPart(
            type="text",
            text=response_text
        )
        
        artifact = TaskArtifact(
            type="text/plain",
            parts=[artifact_part]
        )
        
        # Create the task result
        task = Task(
            artifacts=[artifact]
        )
        
        # Create success response
        success_response = SendMessageSuccessResponse(
            result=task
        )
        
        return SendMessageResponse(
            id=request.id,
            root=success_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/agent_card")
async def get_agent_card() -> AgentCard:
    """Return the agent card for this hotel booking agent."""
    return AgentCard(
        name="Hotel_Booking_Agent",
        description="Specialized agent for hotel research and booking using SerperAPI for real-time information.",
        version="1.0.0"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10002) 