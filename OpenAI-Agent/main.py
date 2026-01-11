from dotenv import load_dotenv
load_dotenv()

import os
from agents import Agent, Runner

agent = Agent(
    name="OpenAI Agent",
    instructions="You are an intelligent agent that uses OpenAI's API to assist users with their queries using emojies and funny ways",  
)

result = Runner.run_sync(agent, "What is the capital of France?")
print(result.final_output) 