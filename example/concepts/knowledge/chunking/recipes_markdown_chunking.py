import asyncio

from agno.agent import Agent
from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.vectordb.milvus import Milvus

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX

vector_db = Milvus(
    collection="recipes_markdown_chunking",
    embedder=TEXT_EMBEDDING_V4,
)
knowledge = Knowledge(
    vector_db=vector_db
)

asyncio.run(knowledge.add_content_async(
    path="./第一性原理.md",
    reader=MarkdownReader(
        name="Markdown Chunking Reader",
        chunking_strategy=MarkdownChunking(chunk_size=100, overlap=20),
    ),
))
agent = Agent(
    model=QWEN3_MAX,
    instructions="""查询知识库回答问题,知识库没有回答一句歉意的话,不废话""",
    knowledge=knowledge,
    search_knowledge=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("什么是原理?", markdown=True)
