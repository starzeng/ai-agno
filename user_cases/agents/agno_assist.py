from agno.agent import Agent
from agno.db.mysql import MySQLDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.vectordb.search import SearchType

from models.gpu_stack import BGE_M3
from models.models import QWEN3_OMNI_FLASH_2025_09_15

db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"
vector_db = PgVector(
    table_name="vectors",
    db_url=db_url,
    search_type=SearchType.hybrid,
    embedder=BGE_M3,
)

knowledge = Knowledge(
    vector_db=vector_db,
)

# knowledge.add_content(name="Agno Docs", url="https://docs.agno.com/llms-full.txt")


db = MySQLDb(
    db_url="mysql+pymysql://root:123456@localhost:3306/ai",
    session_table="agent_sessions",
    memory_table="agent_memories",
    metrics_table="agent_metrics",
)

agno_assist = Agent(
    name="Agno 助手",
    model=QWEN3_OMNI_FLASH_2025_09_15,
    description="你帮助回答有关 Agno 框架的问题。",
    instructions="在回答问题之前先搜索你的知识库。没有搜索到回答:'我不知道是什么呢!'.搜索到后总结精炼, 最后翻译成中文回答输出.",
    knowledge=knowledge,
    db=db,
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
    stream=True,
    debug_mode=True,
    telemetry=False,
)

if __name__ == "__main__":
    agno_assist.print_response("agno是什么,能做什么")
