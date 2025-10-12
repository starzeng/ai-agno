from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    add_location_to_context=True,
    tools=[DuckDuckGoTools(cache_results=True)],
    debug_mode=True,
    debug_level=2,
    markdown=False,
)

agent.print_response("我在哪个国家?", stream=False)

agent.print_response("关于我的国家有哪些好玩的地方？", stream=False)
