import asyncio

from agno.agent import Agent
from agno.tools.mcp import MCPTools

from models.models import QWEN3_MAX


async def agno_mcp():
    async with MCPTools(
            transport="streamable-http",
            url="https://docs.agno.com/mcp"
    ) as mcp_tools:
        agent = Agent(
            model=QWEN3_MAX,
            tools=[mcp_tools],
            debug_mode=True,
            debug_level=2,
        )
        await agent.aprint_response("告诉我关于 Agno 的 MCP 支持")


asyncio.run(agno_mcp())
