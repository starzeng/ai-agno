import asyncio

from agno.agent import Agent
from agno.knowledge.chunking.agentic import AgenticChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.milvus import Milvus

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX

vector_db = Milvus(
    collection="recipes_agentic_chunking",
    embedder=TEXT_EMBEDDING_V4,

)
knowledge = Knowledge(
    vector_db=vector_db
)

asyncio.run(
    knowledge.add_contents_async(
        paths=["../大数据风控实战课程.pdf"],
        reader=PDFReader(
            name="Agentic Chunking Reader",
            chunking_strategy=AgenticChunking(
                model=QWEN3_MAX,
            ),
        ),
    )
)

agent = Agent(
    model=QWEN3_MAX,
    instructions="""查询知识库回答问题,知识库没有回答一句歉意的话,不废话""",
    knowledge=knowledge,
    search_knowledge=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("风控是啥?", markdown=True)
