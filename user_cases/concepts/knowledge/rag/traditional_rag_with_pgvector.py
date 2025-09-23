from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType

from models.gpu_stack import QWEN3_30B_128K, BGE_M3

db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"

knowledge = Knowledge(
    # 使用PGVECTOR作为矢量数据库，并将嵌入在“ ai.agno_docs”表中
    vector_db=PgVector(
        table_name="agno_docs",
        db_url=db_url,
        search_type=SearchType.hybrid,
        embedder=BGE_M3,
    ),
)

knowledge.add_content(
    name="AgnoDocs",
    url="https://docs.agno.com/llms-full.txt",
)


# agent = Agent(
#     model=QWEN3_30B_128K,
#     knowledge=knowledge,
#     # 通过将“知识”中的上下文添加到用户提示来启用 RAG。
#     add_knowledge_to_context=True,
#     # 设置为false，因为Agents默认为`search_knowledge = True`
#     search_knowledge=False,
#     markdown=True,
#     debug_level=2,
#     debug_mode=True,
# )
# agent.print_response(
#     input="agno是什么",
#     stream=True
# )
