from textwrap import dedent

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType

from models.gpu_stack import BGE_M3
from models.models import QWEN_PLUS_2025_07_28

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="./tmp/lancedb",
        table_name="agno_knowledge",
        search_type=SearchType.hybrid,
        embedder=BGE_M3,
    ),
)

knowledge.add_content(
    url="https://docs.agno.com/llms-full.txt",
)

agent = Agent(
    model=QWEN_PLUS_2025_07_28,
    instructions=dedent("""\
    agno 框架编程专家\
    """),
    knowledge=knowledge,
    search_knowledge=True,
    # tools=[DuckDuckGoTools()],
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("agno是什么", stream=True)
