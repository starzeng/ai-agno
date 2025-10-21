from agno.agent import Agent
from agno.tools.shell import ShellTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[ShellTools()],
    markdown=True,
)
agent.print_response("列出当前目录下的所有文件")
