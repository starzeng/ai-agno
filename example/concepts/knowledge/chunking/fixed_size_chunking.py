import asyncio

from agno.agent import Agent
from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.milvus import Milvus

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX

vector_db = Milvus(
    collection="recipes_fixed_size_chunking",
    embedder=TEXT_EMBEDDING_V4,

)
knowledge = Knowledge(
    vector_db=vector_db
)

asyncio.run(knowledge.add_content_async(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
    reader=PDFReader(
        name="Fixed Size Chunking Reader",
        chunking_strategy=FixedSizeChunking(),
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

agent.print_response("鸡汤怎么做?", markdown=True)
