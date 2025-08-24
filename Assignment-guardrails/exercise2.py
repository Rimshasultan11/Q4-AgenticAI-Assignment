from connection import config
from pydantic import BaseModel
import rich
import asyncio
from agents import Agent, input_guardrail, Runner, InputGuardrailTripwireTriggered, GuardrailFunctionOutput

# Output Model
class WeatherRequest(BaseModel):
    response: str
    isSafeToRun: bool

# Father Guardrail Agent
father_guardrail_agent = Agent(
    name="Father-Guardrail-Agent",
    instructions="""
    You are a father guardrail agent.
    Your job is to stop your child from running if the temperature is below 26C.
    
    """,
    output_type=WeatherRequest,
)

# Guardrail Function
@input_guardrail
async def father_guardrail(ctx, agent, input):
    result = await Runner.run(
        father_guardrail_agent,
        input,
        run_config=config,
    )
    rich.print("Father Guardrail Check:", result.final_output)

    return GuardrailFunctionOutput(
        output_info=result.final_output.response,
        tripwire_triggered=not result.final_output.isSafeToRun
    )

# Child Agent
child_agent = Agent(
    name="Child-Agent",
    instructions="You are a helpful assistant.",
    input_guardrails=[father_guardrail],
)

# Main Function
async def main():
    try:
        result = await Runner.run(
            child_agent,
            input="I want to run, AC is set to 26C.",
            run_config=config,
        )
        print("Child is safe to run..")
    except InputGuardrailTripwireTriggered:
        print("Child is not safe to run.")

if __name__ == "__main__":
    asyncio.run(main())
