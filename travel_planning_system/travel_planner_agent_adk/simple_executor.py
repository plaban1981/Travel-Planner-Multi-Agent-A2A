#!/usr/bin/env python3
"""
Simple executor for the travel planner agent.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from simple_travel_planner import SimpleTravelPlanner

app = FastAPI(title="Travel Planner Agent", version="1.0.0")

# Initialize the travel planner
travel_planner = SimpleTravelPlanner()


class TravelRequest(BaseModel):
    """Request model for travel planning."""
    message: str


@app.post("/plan")
async def plan_trip(request: TravelRequest):
    """Plan a trip by coordinating with other agents."""
    try:
        plan = travel_planner.plan_trip(request.message)
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "Travel_Planner_Agent"}


@app.get("/agents/status")
async def check_agents():
    """Check status of other agents."""
    status = travel_planner.check_agent_status()
    return {"agents": status}


@app.get("/")
async def root():
    """Root endpoint with agent information."""
    return {
        "agent": "Travel_Planner_Agent",
        "description": "Travel planning agent that coordinates with hotel and car rental agents",
        "endpoints": {
            "plan": "/plan",
            "health": "/health",
            "agents_status": "/agents/status"
        },
        "coordinated_agents": {
            "hotel_booking": "http://localhost:10002",
            "car_rental": "http://localhost:10003"
        }
    }


if __name__ == "__main__":
    print("✈️ Starting Travel Planner Agent")
    print("📍 Server will be available at: http://localhost:10001")
    print("🔗 Health check: http://localhost:10001/health")
    print("📋 Plan endpoint: http://localhost:10001/plan")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=10001) 