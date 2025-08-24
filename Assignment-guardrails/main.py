# Exercise # 1 Objective:
# Make a agent and make an input guardrail trigger. Prompt: I want to change my class timings 😭😭 Outcome: After running the above prompt an InputGuardRailTripwireTriggered in except should be called. See the outcome in LOGS

import rich
from connection import config
from agents import Agent ,input_guardrail,Runner,InputGuardrailTripwireTriggered,GuardrailFunctionOutput
from  pydantic import BaseModel
import asyncio

class ClassTimingChangeRequest(BaseModel):
    response: str
    isChangePossible: bool

timing_guardrail_agent = Agent(
    name = "Timing-Change-Agent",
    instructions="""  You are a agent that helps students to change their class timings.
    if class timming 9:00 am between 5:00 pm so change is possible otherwise not possible.
    
    """,
    output_type=ClassTimingChangeRequest,
)

@input_guardrail
async def timing_change_guardrail(ctx,agent,input):
    result = await Runner.run(
        timing_guardrail_agent,
        input,
        run_config= config
    )
    rich.print("Guardrail Result:", result.final_output)

    return GuardrailFunctionOutput(
        output_info = result.final_output.response,
        tripwire_triggered = not result.final_output.isChangePossible
    )

time_agent = Agent(
    name = "Timing-Change-Agent",
    instructions="""  You are a agent that helps students to change their class timings.""",
    input_guardrails=[timing_change_guardrail],
)

async def main():
    try:
        result = await Runner.run( 
            time_agent,
            """I want to change my class timings 😭😭
             I have a class at 9:00 AM and I want to change it to 10:00 AM""",
            run_config= config
        )
        print("yes change possible")
    except InputGuardrailTripwireTriggered:
        print("no change possible")
       
    

if __name__ == "__main__":
    asyncio.run(main())


