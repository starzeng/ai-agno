from agno.agent import Agent
from agno.knowledge.chunking.document import DocumentChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.text_reader import TextReader
from agno.vectordb.lancedb import LanceDb, SearchType

from models.models import QWEN3_MAX, TEXT_EMBEDDING_V4
from reranker.dashscope_reranker import DashScopeReranker

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="./tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=TEXT_EMBEDDING_V4,
        reranker=DashScopeReranker(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            top_n=3,
        )
    ),
)

# knowledge.add_content(
#     name="Agno Docs", url="https://docs.agno.com/introduction.md",
#     reader=TextReader(
#         chunking_strategy=DocumentChunking(
#             chunk_size=500,
#             overlap=20
#         )
#     ),
# )

agent = Agent(
    model=QWEN3_MAX,
    knowledge=knowledge,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("Agno的主要功能是什么？")
