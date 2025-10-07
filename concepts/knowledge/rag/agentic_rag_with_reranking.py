from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType

from models.gpu_stack import BGE_M3
from models.models import QWEN3_OMNI_FLASH_2025_09_15

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="./tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=BGE_M3,
        reranker=QWEN3_OMNI_FLASH_2025_09_15
    ),

)

# knowledge.add_content(
#     name="Agno Docs", url="https://docs.agno.com/introduction.md"
# )

agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    knowledge=knowledge,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("Agno的主要功能是什么？")
