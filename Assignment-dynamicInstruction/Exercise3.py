from dotenv import load_dotenv
from connection import config
from agents import Agent, RunContextWrapper,Runner,trace
import asyncio
from pydantic import BaseModel


load_dotenv()

# ---------------------Exercise 3: Travel Planning Assistant--------------------

class TravelPlanningAssistant(BaseModel):
    trip_type: str
    traveler_profile: str

user = TravelPlanningAssistant(trip_type="Adventure", traveler_profile="Solo")

def get_dynamic_instructions(ctx:RunContextWrapper[TravelPlanningAssistant],agent:Agent):

    if ctx.context.trip_type == "Adventure" and ctx.context.traveler_profile == "Solo":
        return """You are a travel planning assistant.
        Suggest exciting activities, focus on safety tips.
        Recommend social hostels and group tours for meeting people."""
    
    elif ctx.context.trip_type == "Cultural" and ctx.context.traveler_profile == "Family":
        return """You are a travel planning assistant.
        Focus on educational attractions, kid-friendly museums, interactive experiences.
        Recommend family accommodations."""
    
    elif ctx.context.trip_type == "Business" and ctx.context.traveler_profile == "Executive":
        return """You are a travel planning assistant.
        Emphasize efficiency, airport proximity, business centers, reliable wifi, premium lounges."""
    
    else:
        return """You are a travel planning assistant.
        Provide general travel recommendations based on trip type and traveler profile."""

travel_planning_agent = Agent(
    name = "TravelPlanningAssistant",
    instructions = get_dynamic_instructions
)

async def main():
    with trace("travel_planning_agent"):
        result = await Runner.run(
            travel_planning_agent,
            input="what are the best activities for my trip?",
            run_config=config,
            context = user
        )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
    