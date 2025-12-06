import dotenv
from agno.agent import Agent
from agno.knowledge.chunking.document import DocumentChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.text_reader import TextReader
from agno.models.dashscope import DashScope
from agno.vectordb.lancedb import LanceDb, SearchType

from my_ext.dashscop_embedder import DashScopeEmbedder
from reranker.dashscope_reranker import DashScopeReranker

dotenv.load_dotenv()

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="./tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=DashScopeEmbedder(
            id="text-embedding-v4",
            base_url=BASE_URL,
            dimensions=128,
            enable_batch=True,
            batch_size=10
        ),
        reranker=DashScopeReranker(
            base_url=BASE_URL,
            top_n=3,
        )
    ),
)

knowledge.add_content(
    name="Agno Docs",
    url="https://docs.agno.com/introduction.md",
    reader=TextReader(
        chunking_strategy=DocumentChunking(
            chunk_size=500,
            overlap=20
        )
    ),
)

agent = Agent(
    model=DashScope(
        id="qwen3-max",
        base_url=BASE_URL,
    ),
    knowledge=knowledge,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("what is agno?")
