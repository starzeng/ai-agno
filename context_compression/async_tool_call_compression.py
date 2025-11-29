import asyncio

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.baidusearch import BaiduSearchTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[BaiduSearchTools()],
    description="您是一位得力助手，可以搜索各种信息。",
    instructions="使用搜索工具并始终使用最新信息和数据。",
    db=SqliteDb(db_file="./dbs/async_tool_call_compression.db"),
    compress_tool_results=True,
    debug_mode=True,
    debug_level=2,
)


async def main():
    await agent.aprint_response(
        """
        使用搜索工具并始终获取最新信息和数据。

        阿里云栖大会2025

        找出带有日期和数字的具体行动。""",
        stream=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
