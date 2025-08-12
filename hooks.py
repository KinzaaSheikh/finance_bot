# type: ignore

from agents import Runner, RunHooks, Agent

agent: Agent = Agent(
    name="Assistant"
)

class MyCustomRunHooks(RunHooks):
    async def on_run_start(self, runner: Runner):
        print(f"Run started for agent: {runner.agent.name}")

    async def on_run_end(self, runner: Runner):
        print(f"Run ended for agent: {runner.agent.name}"   )