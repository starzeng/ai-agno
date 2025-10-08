import os

import dotenv
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.models.dashscope import DashScope

dotenv.load_dotenv()

GPU_STACK_API_KEY = os.getenv("GPU_STACK_API_KEY")
GPU_STACK_BASE_URL = os.getenv("GPU_STACK_BASE_URL")

QWEN3_NEXT_80B_A3B_INSTRUCT_AWQ_4BIT = DashScope(
    id="qwen3-next-80b-a3b-instruct-awq-4bit",
    api_key=GPU_STACK_API_KEY,
    base_url=GPU_STACK_BASE_URL,
    enable_thinking=False,
)
QWEN3_30B_128K = DashScope(
    id="qwen3-30b-128K",
    api_key=GPU_STACK_API_KEY,
    base_url=GPU_STACK_BASE_URL,
    temperature=0.3,
    enable_thinking=False,
)
BGE_M3 = OpenAIEmbedder(
    id="bge-m3",
    api_key=GPU_STACK_API_KEY,
    base_url=GPU_STACK_BASE_URL,
    dimensions=1024,
)
