from dotenv import load_dotenv
from connection import config
from agents import Agent, RunContextWrapper,Runner,trace
import asyncio
from pydantic import BaseModel
import rich

load_dotenv()

# ---------------------Exercise 2: Airline Seat Preference Agent--------------------


class AirlineBooking(BaseModel):
    seat_preference: str
    travel_experience: str

user = AirlineBooking(seat_preference="middle", travel_experience="frequent")

def get_dynamic_instruction(ctx:RunContextWrapper[AirlineBooking],agent:Agent):
    if ctx.context.seat_preference == "window" and ctx.context.travel_experience == "first_time":
        return """You are an airline booking assistant.
        Explain the benefits of a window seat, highlight scenic views during takeoff and landing.
        Reassure the passenger about the flight experience in a friendly tone."""
    
    elif  ctx.context.seat_preference == "middle" and ctx.context.travel_experience == "frequent":
        return """You are an airline booking assistant.
        Explain the benefits of a middle seat, highlight the convenience of having more legroom.
        Reassure the passenger about the flight experience in a friendly tone."""
    
    elif  ctx.context.seat_preference == "any" and ctx.context.travel_experience == "premium":
        return """You are an airline booking assistant.
        Highlight luxury options, upgrades, priority boarding.
        Reassure the passenger about the flight experience in a friendly tone."""
    
    else:
        return """You are an airline booking assistant.
        Provide general information about seat options and travel experience.
        Reassure the passenger about the flight experience in a friendly tone."""
    

airline_agent = Agent(
    name = "AirlineBookingAgent",
    instructions = get_dynamic_instruction
)

async def main():
    with trace("airline_booking_agent"):
        result = await Runner.run(
            airline_agent,
            input="what are the benefits of my seat choice?",
            run_config=config,
            context = user
        )

        rich.print(result.final_output)
    

if __name__ == "__main__":
    asyncio.run(main())