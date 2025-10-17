from agno.agent import Agent
from agno.tools.baidusearch import BaiduSearchTools

from models.models import QWEN3_235B_A22B

agent = Agent(
    model=QWEN3_235B_A22B,
    tools=[BaiduSearchTools()],
    description="你是一个搜索助手，帮助用户使用百度查找最相关的信息。",
    instructions=[
        "根据用户提供的主题，返回关于该主题的1个最相关的搜索结果。",
        "搜索3个结果并从中选择前1个独特的项目。",
        "同时使用英文和中文进行搜索。",
    ],
    debug_level=2,
    debug_mode=True,
)
agent.print_response("人工智能的最新进展有哪些？", markdown=True)
