"""
agno docs
"""

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.tools.knowledge import KnowledgeTools
from agno.vectordb.lancedb import SearchType
from agno.vectordb.milvus import Milvus

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX

vector_db = Milvus(
    collection="agno_docs",
    search_type=SearchType.hybrid,
    embedder=TEXT_EMBEDDING_V4,
)
agno_docs = Knowledge(
    vector_db=vector_db
)
agno_docs.add_content(path="./llms-full.txt")

knowledge_tools = KnowledgeTools(
    knowledge=agno_docs,
    enable_think=True,
    enable_search=True,
    enable_analyze=True,
    add_few_shot=True,
)

agent = Agent(
    model=QWEN3_MAX,
    introduction="""
    中文回答所有问题
    """,
    tools=[knowledge_tools],
    markdown=True,
    debug_mode=True,
    debug_level=2,
    telemetry=False,
)

if __name__ == "__main__":
    agent.print_response(
        "如何使用agno构建Agent",
        markdown=True,
        stream=True,
    )
