from agno.agent import Agent
from agno.tools.apify import ApifyTools

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    tools=[ApifyTools()],
    debug_mode=True,
    debug_level=2,
)
agent.print_response("Tell me about https://docs.agno.com/introduction", markdown=True)