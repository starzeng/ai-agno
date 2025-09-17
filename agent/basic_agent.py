from textwrap import dedent

from agno.agent import Agent

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    instructions=dedent("""
    你是一个AI新闻收集专家, 只会答AI相关的新闻信息.
    """),
    markdown=True,
    debug_level=2,
    debug_mode=True,
)

agent.print_response(
    "最新的AI应用新闻", stream=True
)

