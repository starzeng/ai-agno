from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType
from sympy.codegen.fnodes import dimension

from models.gpu_stack import BGE_M3
from models.models import QWEN3_OMNI_FLASH_2025_09_15

db_url = "postgresql+psycopg://pgvector:pgvector@localhost:5432/pgvector"

knowledge = Knowledge(
    # 使用PGVECTOR作为矢量数据库，并将嵌入在“pgvector.recipes”表中
    vector_db=PgVector(
        table_name="rag_pgvector",
        db_url=db_url,
        search_type=SearchType.hybrid,
        embedder=BGE_M3,
    ),
)

# knowledge.add_content(
#     name="Agno Docs",
#     url="https://docs.agno.com/llms-full.txt"
# )
knowledge.add_content(
    name="my name",
    text_content="my name is starry zeng"
)

agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    knowledge=knowledge,
    add_knowledge_to_context=True,
    search_knowledge=True,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)
agent.print_response(
    "什么是agno, 中文回答", stream=True
)
