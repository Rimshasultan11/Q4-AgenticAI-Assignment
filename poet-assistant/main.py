from agents import Agent, Runner , trace
from connection import config
import asyncio
import rich
from dotenv import load_dotenv

load_dotenv()


lyricPoet_agent = Agent(
    name = "Lyric_poet-agent",
    instructions = """You are a Lyric Poetry Analyst Agent.
      Analyze the given poem and determine whether it is an example of lyric poetry.
      If it is, provide the poem's title, the author's name (if available), and explain the meaning of its stanza(s) in simple terms."""
)
    

narrativePoet_agent = Agent(
    name =  "Narrative_poet-agent",
    instructions = """You are a Narrative Poetry Analyst Agent.
      Analyze the given poem and determine whether it is an example of narrative poetry.
      If it is, provide the poem's title, the author's name (if available), and explain the meaning of its stanza(s) in simple terms."""
    )

dramaticPoet_agent = Agent(
    name = "Dramatic_poet-agent",
    instructions = """You are a Lyric Poetry Analyst Agent.
     Analyze the given poem and determine whether it is an example of lyric poetry.
     If it is, provide the poem's title, the author's name (if available), and explain the meaning of its stanza(s) in simple terms."""
)

orchestrator_agent = Agent(
    name = "Orchestrator-agent",
    instructions="""
You are an Orchestrator Agent.

Your task is to receive a poem and determine which type of poetry it belongs to. Based on the classification, delegate the task to the appropriate agent:
If it is **lyric poetry**, pass it to the **Lyric_poet-agent**.
If it is **narrative poetry**, pass it to the **Narrative_poet-agent**.
If it is **dramatic poetry**, pass it to the **Dramatic_poet-agent**.
If the poem does not belong to any of these categories, simply respond with:
"This poem does not fit into any recognized category. Please try again with a different poem."
""",
    handoffs = [lyricPoet_agent, narrativePoet_agent, dramaticPoet_agent]
)

async def main():
    with trace("Home Work: Poet_Agents"):
        prompt = input("Enter a poem (2 stanzas): ")
        result = await Runner.run(
            orchestrator_agent,
            input=prompt,
            run_config = config
        )
        rich.print(result.final_output)
        rich.print("last agent:", result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())