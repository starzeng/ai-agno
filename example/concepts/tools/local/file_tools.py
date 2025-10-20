from pathlib import Path

from agno.agent import Agent
from agno.tools.file import FileTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[FileTools(Path("./tmp/file"))],
    debug_mode=True,
    debug_level=2,
)
agent.print_response(
    "目前最高级的LLM是什么？将答案保存到MD文件中。",
    markdown=True
)
