import asyncio

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType

from models.models import QWEN3_MAX_PREVIEW, TEXT_EMBEDDING_V4

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="./tmp/lancedb",
        table_name="agno_assist_knowledge",
        search_type=SearchType.hybrid,
        embedder=TEXT_EMBEDDING_V4,
    ),
)

asyncio.run(
    knowledge.add_content_async(name="Agno文档", url="https://docs.agno.com/llms-full.txt")
)

agno_assist = Agent(
    name="Agno助手",
    model=QWEN3_MAX_PREVIEW,
    description="你帮助回答关于 Agno 框架的问题。",
    instructions="在回答问题之前搜索你的知识库。中文回答所有问题.",
    knowledge=knowledge,
    db=SqliteDb(session_table="agno_assist_sessions", db_file="./tmp/agents.db"),
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

if __name__ == "__main__":
    agno_assist.print_response("什么是Agno?")
