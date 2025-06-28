import os
import json
import requests
from datetime import date
from typing import Type

from crewai import LLM, Agent, Crew, Process, Task,LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

load_dotenv()


class HotelSearchToolInput(BaseModel):
    """Input schema for HotelSearchTool."""

    location: str = Field(
        ...,
        description="The location/city to search for hotels in.",
    )
    check_in: str = Field(
        ...,
        description="Check-in date in YYYY-MM-DD format.",
    )
    check_out: str = Field(
        ...,
        description="Check-out date in YYYY-MM-DD format.",
    )
    budget: str = Field(
        default="any",
        description="Budget range (e.g., 'budget', 'mid-range', 'luxury', 'any').",
    )


class HotelSearchTool(BaseTool):
    name: str = "Hotel Search Tool"
    description: str = (
        "Search for hotels in a specific location with check-in and check-out dates. "
        "Use this to find available hotels and their details."
    )
    args_schema: Type[BaseModel] = HotelSearchToolInput

    def _run(self, location: str, check_in: str, check_out: str, budget: str = "any") -> str:
        """Search for hotels using web search."""
        serper_api_key = os.getenv("SERPER_API_KEY")
        if not serper_api_key:
            return "SERPER_API_KEY not found in environment variables"
        
        # Bias search toward MakeMyTrip, Goibibo, Booking.com
        search_query = (
            f"Budget friendly hotels in {location} from {check_in} to {check_out}"
        )
        if budget != "any":
            search_query += f" {budget} hotels"
        
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
            
            # Extract hotel information
            results = []
            if "organic" in data:
                for result in data["organic"][:5]:
                    # Try to extract price in USD from snippet if possible
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
                        "location": location,
                        "check_in": check_in,
                        "check_out": check_out,
                        "budget": budget,
                        "estimated_cost_usd": price_usd if price_usd else "N/A"
                    })
            
            return json.dumps(results, indent=2)
        except Exception as e:
            return f"Error searching for hotels: {str(e)}"


class HotelBookingToolInput(BaseModel):
    """Input schema for HotelBookingTool."""

    hotel_name: str = Field(
        ...,
        description="The name of the hotel to book.",
    )
    check_in: str = Field(
        ...,
        description="Check-in date in YYYY-MM-DD format.",
    )
    check_out: str = Field(
        ...,
        description="Check-out date in YYYY-MM-DD format.",
    )
    guests: int = Field(
        default=1,
        description="Number of guests.",
    )


class HotelBookingTool(BaseTool):
    name: str = "Hotel Booking Tool"
    description: str = (
        "Book a hotel room for specified dates and guests. "
        "Use this to make hotel reservations."
    )
    args_schema: Type[BaseModel] = HotelBookingToolInput

    def _run(self, hotel_name: str, check_in: str, check_out: str, guests: int = 1) -> str:
        """Simulate hotel booking process."""
        # In a real implementation, this would integrate with hotel booking APIs
        booking_id = f"HB{date.today().strftime('%Y%m%d')}{hash(hotel_name) % 10000:04d}"
        
        booking = {
            "booking_id": booking_id,
            "hotel_name": hotel_name,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "status": "confirmed",
            "booking_date": date.today().isoformat()
        }
        
        return json.dumps(booking, indent=2)


class HotelBookingAgent:
    """Agent that handles hotel booking tasks."""

    SUPPORTED_CONTENT_TYPES = ["text/plain"]

    def __init__(self):
        """Initializes the HotelBookingAgent."""
        groq_api_key = os.getenv("GROQ_API_KEY")
        print(groq_api_key)
        if os.getenv("GROQ_API_KEY"):
            self.llm = LLM(
                            model="groq/llama-3.3-70b-versatile",
                            api_key=os.getenv("GROQ_API_KEY")
                        )
        else:
            raise ValueError("GROQ_API_KEY environment variable not set.")

        self.hotel_booking_assistant = Agent(
            role="Hotel Booking Specialist",
            goal="Find and book the best hotels for travelers based on their preferences and requirements.",
            backstory=(
                "You are an expert hotel booking specialist with years of experience in the travel industry. "
                "You have extensive knowledge of hotels worldwide and can find the perfect accommodation "
                "for any traveler's needs. You use advanced search tools to find current availability and "
                "pricing, and you can handle bookings efficiently. You always prioritize customer satisfaction "
                "and provide detailed information about each hotel option."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[HotelSearchTool(), HotelBookingTool()],
            llm=self.llm,
        )

    def invoke(self, question: str) -> str:
        """Kicks off the crew to answer a hotel booking question."""
        task_description = (
            f"Help the user with their hotel booking request. The user asked: '{question}'. "
            f"Today's date is {date.today().strftime('%Y-%m-%d')}. "
            f"First search for available hotels, then provide booking options or make a booking if requested."
        )

        hotel_booking_task = Task(
            description=task_description,
            expected_output="""
                    [
                    {
                        "name": "Name of the  hotel",
                        "description": "A description of the hotel in no more than 40 words",
                        "link": "https://...(URL)",
                        "estimated_cost_usd": "$10"
                    },
                    ...
                ]
            """,
            agent=self.hotel_booking_assistant,
        )

        crew = Crew(
            agents=[self.hotel_booking_assistant],
            tasks=[hotel_booking_task],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        print(f"Hotel response CREWAI: {result.raw}")
        # response ={"hotel_response":result.raw}
        return result.raw