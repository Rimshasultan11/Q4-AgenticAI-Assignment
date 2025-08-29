from dotenv import load_dotenv
from connection import config
from agents import Agent, RunContextWrapper,Runner,trace
import asyncio
from pydantic import BaseModel
import rich

load_dotenv()

# ---------------------Exercise 1: Medical Consultation Agent--------------------

class MedicalConsultation(BaseModel):
    user_type: str

user = MedicalConsultation(user_type="Doctor") 

def get_dynamic_instructions(ctx:RunContextWrapper[MedicalConsultation],agent:Agent):
    if ctx.context.user_type == "Patient":
        return """You are a medical consultation assistant. Use simple, non-technical language.
            Explain medical terms in everyday words. Be empathetic and reassuring."""
    
    elif ctx.context.user_type == "Medical Student":
        return """You are a medical consultation assistant. Use moderate medical terminology with explanations.
            Include learning opportunities."""

    elif ctx.context.user_type == "Doctor":
        return """You are a medical consultation assistant. Use full medical terminology, abbreviations, and clinical language.
            Be concise and professional."""
    

medical_agent = Agent(
    name = "MedicalConsultationAgent",
    instructions = get_dynamic_instructions
)


async def main():
    with trace("medical_consultation_agent"):
        result = await Runner.run(
            medical_agent,
            input="what are the symptoms of diabetes?",
            run_config=config,
            context = user
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
    