# type: ignore

import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

agent = Agent(
    name="Tutor Huang",
    instructions="You are a helpful tutor that answers questions in the style of Zia Khan",
    model=model
)

result: Runner = Runner.run_sync(agent, input="Tell me about RunContextWrapper in OpenAI Agent SDK")

print(result.final_output)