import asyncio

from agno.agent import Agent
from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.milvus import Milvus

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX

vector_db = Milvus(
    collection="recipes_recursive_chunking",
    embedder=TEXT_EMBEDDING_V4,

)
knowledge = Knowledge(
    vector_db=vector_db
)

# asyncio.run(knowledge.add_content_async(
#     path="./大数据风控实战课程.pdf",
#     reader=PDFReader(
#         name="Recursive Chunking Reader",
#         chunking_strategy=RecursiveChunking(chunk_size=200),
#     ),
# ))

agent = Agent(
    model=QWEN3_MAX,
    instructions="""查询知识库回答问题,知识库没有回答一句歉意的话,不废话""",
    knowledge=knowledge,
    search_knowledge=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("知识库有什么", markdown=True)
