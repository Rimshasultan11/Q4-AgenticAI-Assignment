from agents import Agent,AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
print(gemini_api_key)
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client

)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True

)

translator = Agent(
    name="Translator",
    instructions="""You are a language translation agent. You will be given a sentence in one language and you must translate it to another language.""",

)

response = Runner.run_sync(
    translator,
    input = input("Enter a sentence to translate: "),
    # input = "میں لاہور جا رہا ہوں۔:...translate into english",
    run_config = config

)
print(response.final_output)