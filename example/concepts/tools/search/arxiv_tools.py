from agno.agent import Agent
from agno.tools.arxiv import ArxivTools

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    tools=[ArxivTools()],
    debug_mode=True,
    debug_level=2,
)

agent.print_response("在 arxiv 中搜索“RAG”'", markdown=True)
