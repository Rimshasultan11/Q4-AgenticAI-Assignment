# Exercise # 3 Objective: Make a gate keeper agent and gate keeper guardrail. The gate keeper stopping students of other school.
from connection import config
from pydantic import BaseModel
import rich
import asyncio
from agents import Agent, input_guardrail, InputGuardrailTripwireTriggered,GuardrailFunctionOutput,Runner 


class SchoolGateRequest(BaseModel):
    response: str
    isAllowedToEnter: bool

gate_guardrail_agent = Agent(
    name="Gate-Guardrail-Agent",
    instructions="""  You are a agent that helps students to enter the school.
    if student is from school Shinning Star then allow to enter otherwise not allow to enter.""",
    output_type=SchoolGateRequest,
)


@input_guardrail
async def get_guardrails(ctx,agent,input):
    result = await Runner.run(
        gate_guardrail_agent,
        input,
        run_config = config,
    )
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info = result.final_output.response,
        tripwire_triggered = not result.final_output.isAllowedToEnter
    )

gateKeeper_agent = Agent(
    name = "Gate-Keeper-Agent",
    instructions="""  You are a agent that helps students to enter the school.""",
    input_guardrails=[get_guardrails]
)

async def main():
    try:
        result = await Runner.run(
            gateKeeper_agent,
            input = "I am from school Shinning star school and I want to enter the school",
            run_config = config,
        )
        rich.print(" yes Welcome you are allowed to enter the school.")

    except InputGuardrailTripwireTriggered:
        print("No Sorry you are not allowed to enter the school.")

if __name__ == "__main__":
    asyncio.run(main())
