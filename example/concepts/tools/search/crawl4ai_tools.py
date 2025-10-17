from agno.agent import Agent
from agno.tools.crawl4ai import Crawl4aiTools

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    tools=[Crawl4aiTools(max_length=None)],
    debug_mode=True,
    debug_level=2,
)
agent.print_response("告诉我关于 https://github.com/agno-agi/agno.")