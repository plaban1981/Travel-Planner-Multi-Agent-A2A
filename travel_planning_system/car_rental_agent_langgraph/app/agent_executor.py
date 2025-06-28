"""Agent executor for car rental agent."""

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

from .agent import CarRentalAgent

app = FastAPI(title="Car Rental Agent", version="1.0.0")

# Initialize the car rental agent
car_rental_agent = CarRentalAgent()


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
        
        # Process the request using the car rental agent
        response = car_rental_agent.invoke(user_text, str(request.id))
        
        # Extract content from response
        if isinstance(response, dict) and 'content' in response:
            response_text = response['content']
        else:
            response_text = str(response)
        
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
    """Return the agent card for this car rental agent."""
    return AgentCard(
        name="Car_Rental_Agent",
        description="Specialized agent for car rental research and booking using SerperAPI for real-time information.",
        version="1.0.0"
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "Car_Rental_Agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10003) 