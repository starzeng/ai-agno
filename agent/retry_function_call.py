from typing import Iterator

from agno.agent import Agent
from agno.exceptions import RetryAgentRun
from agno.tools import FunctionCall, tool

from models.models import QWEN_PLUS_2025_07_28

num_calls = 0


def pre_hook(fc: FunctionCall):
    global num_calls
    print(f"Pre-hook: {fc.function.name}")
    print(f"Arguments: {fc.arguments}")
    num_calls += 1
    if num_calls < 2:
        raise RetryAgentRun(
            "这不够有趣，请换个参数再试一次"
        )


@tool(pre_hook=pre_hook)
def print_something(something: str) -> Iterator[str]:
    print(something)
    yield f"我已经打印了 {something}"


agent = Agent(model=QWEN_PLUS_2025_07_28, tools=[print_something], markdown=True)
agent.print_response("打印一些有趣的东西", stream=True)
