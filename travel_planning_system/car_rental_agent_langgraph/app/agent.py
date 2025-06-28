import os
import json
import requests
from collections.abc import AsyncIterable
from datetime import date, datetime
from typing import Any, Literal, List, Dict
from typing import List
from pydantic import BaseModel, HttpUrl



from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

memory = MemorySaver()


class CarSearchToolInput(BaseModel):
    """Input schema for the car search tool."""

    location: str = Field(
        ...,
        description="The location/city to search for car rentals in.",
    )
    pickup_date: str = Field(
        ...,
        description="Pickup date in YYYY-MM-DD format.",
    )
    return_date: str = Field(
        ...,
        description="Return date in YYYY-MM-DD format.",
    )
    car_type: str = Field(
        default="any",
        description="Type of car (e.g., 'economy', 'luxury', 'suv', 'any').",
    )


@tool(args_schema=CarSearchToolInput)
def search_car_rentals(location: str, pickup_date: str, return_date: str, car_type: str = "any") -> list:
    """Search for car rental options in a specific location using web search."""
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        return []
    
    search_query = (
        f"car rental {location} from {pickup_date} to {return_date}"
    )
    if car_type != "any":
        search_query += f" {car_type} car"
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": search_query,
        "num": 10
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        results = []
        if "organic" in data:
            for result in data["organic"][:5]:
                price_usd = None
                snippet = result.get("snippet", "")
                import re
                price_match = re.search(r"\$([0-9]+[,.]?[0-9]*)", snippet)
                if price_match:
                    price_usd = f"${price_match.group(1)} USD"
                results.append({
                    "name": result.get("title", ""),
                    "description": snippet,
                    "link": result.get("link", ""),
                    "estimated_cost_usd": price_usd if price_usd else "N/A"
                })
        return results
    except Exception as e:
        return []


class CarBookingToolInput(BaseModel):
    """Input schema for the car booking tool."""

    company: str = Field(
        ...,
        description="The car rental company name.",
    )
    location: str = Field(
        ...,
        description="The pickup location.",
    )
    pickup_date: str = Field(
        ...,
        description="Pickup date in YYYY-MM-DD format.",
    )
    return_date: str = Field(
        ...,
        description="Return date in YYYY-MM-DD format.",
    )
    car_type: str = Field(
        default="economy",
        description="Type of car to rent.",
    )


@tool(args_schema=CarBookingToolInput)
def book_car_rental(company: str, location: str, pickup_date: str, return_date: str, car_type: str = "economy") -> str:
    """Book a car rental for specified dates and location."""
    # In a real implementation, this would integrate with car rental booking APIs
    booking_id = f"CR{date.today().strftime('%Y%m%d')}{hash(company) % 10000:04d}"
    
    booking = {
        "booking_id": booking_id,
        "company": company,
        "location": location,
        "pickup_date": pickup_date,
        "return_date": return_date,
        "car_type": car_type,
        "status": "confirmed",
        "booking_date": date.today().isoformat()
    }
    
    return json.dumps(booking, indent=2)
class CarRentalAgency(BaseModel):
    name: str
    description: str
    link: HttpUrl
    estimated_cost_usd: str

class ResponseFormat(BaseModel):
    status: Literal["input_required", "completed", "error"] = "input_required"
    results: list = [CarRentalAgency]
    message: str = ""

SYSTEM_INSTRUCTION = (
    "You are a car rental booking specialist. "
    "Your primary purpose is to help users find and book car rentals using the available tools. "
    "When presenting car rental options, you MUST put the list of car rental options as a list of dictionaries in the 'results' field of the response, and NOT in the 'message' field. "
    "The 'message' field should only contain a short summary or be left empty. Do NOT put the options as a string in the message. "
    "The 'results' field should look like this:\n"
    "'results': [\n"
    "  {\n"
    "    'name': 'Car Rental in Paris from $23/day - KAYAK',\n"
    "    'description': 'Looking for car rentals in Paris? ...',\n"
    "    'link': 'https://www.kayak.com/Cheap-Paris-Car-Rentals.36014.cars.ksp',\n"
    "    'estimated_cost_usd': '$23 USD'\n"
    "  },\n"
    "  ...\n"
    "]\n"
    "If you cannot find any options, return an empty list []. "
    "If the user asks about anything other than car rentals, politely state that you cannot help with that topic and can only assist with car rental queries. "
    "Set response status to input_required if the user needs to provide more information. "
    "Set response status to error if there is an error while processing the request. "
    "Set response status to completed if the request is complete."
)

class CarRentalAgent:
    """CarRentalAgent - a specialized assistant for car rental booking."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        self.model = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
        self.tools = [search_car_rentals, book_car_rental]

        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=SYSTEM_INSTRUCTION,
            response_format=ResponseFormat,
        )

    def invoke(self, query, context_id):
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
        augmented_query = f"{today_str}\n\nUser query: {query}"
        response = self.graph.invoke({"messages": [("user", augmented_query)]}, config)
        print(f"Car rental response: {response["structured_response"]}")
        return response["structured_response"]

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}."
        augmented_query = f"{today_str}\n\nUser query: {query}"
        inputs = {"messages": [("user", augmented_query)]}
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}

        for item in self.graph.stream(inputs, config, stream_mode="values"):
            message = item["messages"][-1]
            if (
                isinstance(message, AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Searching for car rental options...",
                }
            elif isinstance(message, ToolMessage):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Processing car rental information...",
                }

        yield self.get_agent_response(config)

    def get_agent_response(self, config):
        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get("structured_response")
        if structured_response and isinstance(structured_response, ResponseFormat):
            if structured_response.status == "input_required":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.message,
                }
            if structured_response.status == "error":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.message,
                }
            if structured_response.status == "completed":
                rentals = structured_response.results if structured_response.results else []
                # If rentals is empty, try to extract a list from the message string
                if not rentals and structured_response.message:
                    msg = structured_response.message
                    start = msg.find('[')
                    end = msg.rfind(']') + 1
                    if start != -1 and end != -1 and end > start:
                        list_str = msg[start:end]
                        try:
                            rentals = json.loads(list_str)
                        except Exception:
                            pass
                return {
                    "is_task_complete": True,
                    "require_user_input": False,
                    "content": rentals,
                }
        return {
            "is_task_complete": False,
            "require_user_input": True,
            "content": (
                "We are unable to process your request at the moment. "
                "Please try again."
            ),
        } 