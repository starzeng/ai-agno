import asyncio
from agno.agent import Agent
from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.pgvector import PgVector

from models.gpu_stack import BGE_M3
from models.models import QWEN3_OMNI_FLASH_2025_09_15

db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="recipes_fixed_size_chunking",
        db_url=db_url,
        embedder=BGE_M3,
    ),
)

asyncio.run(knowledge.add_content_async(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
    reader=PDFReader(
        name="Fixed Size Chunking Reader",
        chunking_strategy=FixedSizeChunking(),
    ),
))
agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    knowledge=knowledge,
    search_knowledge=True,
)

agent.print_response("How to make Thai curry?", markdown=True)