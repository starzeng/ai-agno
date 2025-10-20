from agno.agent import Agent
from agno.tools.python import PythonTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[PythonTools()],
    markdown=True,
    debug_level=2,
    debug_mode=True,
)
agent.print_response("使用Python计算5的阶乘")
