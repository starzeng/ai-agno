from agno.agent import Agent
from agno.tools.sleep import SleepTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[SleepTools()],
    markdown=True,
    debug_mode=True,
    debug_level=2,
)
agent.print_response("等待 5 秒后再继续")
