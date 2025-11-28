from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[DuckDuckGoTools()],
    description="专门跟踪竞争对手活动",
    instructions="使用搜索工具，并始终使用最新信息和数据。",
    db=SqliteDb(db_file="./dbs/tool_call_compression.db"),
    compress_tool_results=True,  # 启用工具调用压缩
    debug_mode=True,
    debug_level=2,
)

agent.print_response(
    """
    使用搜索工具，并始终获取最新信息和数据。
    研究以下AI公司的近期活动（最近一天）：

    1. OpenAI - 产品发布、合作伙伴关系、定价
    2. Anthropic - 新功能、企业合作、融资
    3. Google DeepMind - 研究突破、产品发布
    4. Meta AI - 开源发布、研究论文

    对于每家公司，找出具体的行动及其日期和数字。""",
    stream=True,
)
