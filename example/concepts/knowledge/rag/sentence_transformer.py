from agno.agent import Agent
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.sentence_transformer import SentenceTransformerReranker
from agno.vectordb.milvus import Milvus

from models.models import QWEN3_MAX

search_results = [
    "有机护肤品适用于敏感肌肤，含有芦荟和洋甘菊成分。",
    "新的化妆趋势注重大胆的色彩和创新的技术",
    "适用于敏感肌肤的生物护肤品，含芦荟和洋甘菊",
    "新的化妆趋势强调鲜艳的颜色和创新技术",
    "适用于敏感肌肤的有机护肤产品，含芦荟和洋甘菊",
    "新的化妆趋势集中在鲜艳的颜色和创新技巧上",
    "针对敏感肌专门设计的天然有机护肤产品",
    "新的化妆趋势注重鲜艳的颜色和创新的技巧",
    "为敏感肌特别设计的天然有机护肤产品",
    "新的彩妆趋势聚焦于鲜明色彩与创新技法",
]
vector_db = Milvus(
    collection="sentence_transformer_rerank_docs",
    embedder=SentenceTransformerEmbedder(
        id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ),
    reranker=SentenceTransformerReranker(
        model="BAAI/bge-reranker-v2-m3"
    ),
)
knowledge = Knowledge(
    vector_db=vector_db
)

for result in search_results:
    knowledge.add_content(
        text_content=result,
        metadata={
            "source": "search_results",
        },
    )

agent = Agent(
    model=QWEN3_MAX,
    knowledge=knowledge,
    search_knowledge=True,
    instructions=[
        "在回复中包含来源信息。",
        "在回答问题前始终搜索你的知识库。",
    ],
    markdown=True,
    # debug_mode=True,
    # debug_level=2,
    # telemetry=False,
)

agent.print_response(
    "比较不同语言的护肤和化妆信息",
    stream=True,
    show_full_reasoning=True,
)
