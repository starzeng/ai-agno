from agno.agent import Agent
from agno.tools.webtools import WebTools

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    instructions=[
        "你是一个网络工具助手，帮助处理URL操作",
        "展开缩短的URL以显示其最终目标地址",
        "在用户访问链接前帮助他们了解链接指向何处",
    ],
    tools=[WebTools()],
    markdown=True,
)

agent.print_response("展开这个缩短的URL: https://bit.ly/3example")
