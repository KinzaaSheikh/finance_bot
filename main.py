# type: ignore

from fastapi import FastAPI
from pydantic import BaseModel, Field
import asyncio
from agents import Agent, AgentHooks, RunHooks, RunContextWrapper

# Pydantic request model

class UserRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=100)
    user_id: int = Field(..., gt=0)

# Hooks

class MyAgentHooks(AgentHooks):
    async def on_agent_start(self, agent, context):
        print(f"[Agent start] {agent.name} with input: {context.input}")

    async def on_agent_end(self, agent, context, result):
        print(f"[Agent end] {agent.name} with output: {result}")


class MyRunHooks(RunHooks):
    async def on_run_start(self, run_id, context):
        print(f"[Run start] {run_id}")
    
    async def on_run_end(self, run_id, context, result):
        print(f"[Run end] {run_id} with output: {result}")

# Custom context wrapper

class MyContextWrapper(RunContextWrapper):
    def __init__(self, context):
        super().__init__(context)
        self.custom_data = {}

    def add_data(self, key, value):
        self.custom_data[key] = value

    def get_data(self, key):
        return self.custom_data.get(key)

    
# Agent setup

class EchoAgent(Agent):
    async def run(self, input, context):
        user_message = input
        # Add custom info to context
        if hasattr(context, "add_data"):
            context.add_data("last_message_length", len(user_message))
        return f"Echo: {user_message}"
    
async def run_agent(agent, input, context, hooks):
    return await agent.run(input, context=context, hooks=hooks)

# FastAPI setup

app = FastAPI()

@app.post("/chat/")
async def chat(request: UserRequest):
    # Prepare context
    base_context = {
        "input": request.message
        }
    wrapped_context = MyContextWrapper(base_context)
    wrapped_context.add_data("user_id", request.user_id)

    # Setup agent and hooks
    agent = EchoAgent(
        name = "Echo Agent",
        hooks=MyAgentHooks()
    )
    run_hooks = MyRunHooks()

    # Run agent
    result = await agent.run(request.message, context=wrapped_context, hooks=run_hooks)

    return {
        "response": result,
        "custom_context_data": wrapped_context.custom_data
    }
