from agno.agent import Agent
from agno.tools.wikipedia import WikipediaTools

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    tools=[WikipediaTools()],
    markdown=True,
    debug_mode=True,
    debug_level=2,
)
agent.print_response("搜索维基百科以获取有关人工智能的信息")
