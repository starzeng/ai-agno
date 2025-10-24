import asyncio
import time

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.milvus import Milvus

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX

vector_db = Milvus(
    collection="agentic_filtering",
    embedder=TEXT_EMBEDDING_V4,
)

knowledge = Knowledge(
    name="CSV 知识库",
    description="CSV 文件的知识库",
    vector_db=vector_db,
)

asyncio.run(
    knowledge.add_content_async(
        path="../filters_2.csv",
        metadata={
            "year": "2024",
        }
    )
)

agent = Agent(
    model=QWEN3_MAX,
    knowledge=knowledge,
    search_knowledge=True,
    # enable_agentic_knowledge_filters=True,
    knowledge_filters={"year": "2024"},
    debug_level=2,
    debug_mode=True,
)

agent.print_response(
    "告诉我最畅销产品",
    markdown=True,
)
