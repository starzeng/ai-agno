import os

import dotenv
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.models.dashscope import DashScope

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

QWEN_PLUS_2025_07_28 = DashScope(
    id="qwen-plus-2025-07-28",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False
)

QWEN_VL_PLUS_2025_08_15 = DashScope(
    id="qwen-vl-plus-2025-08-15",
    api_key=API_KEY,
    base_url=BASE_URL,
)

QWEN_MT_IMAGE = DashScope(
    id="qwen-mt-image",
    api_key=API_KEY,
    base_url=BASE_URL,
)

QWEN3_MAX_PREVIEW = DashScope(
    id="qwen3-max-preview",
    api_key=API_KEY,
    base_url=BASE_URL,
)

QWEN3_235B_A22B_INSTRUCT_2507 = DashScope(
    id="qwen3-235b-a22b-instruct-2507",
    api_key=API_KEY,
    base_url=BASE_URL,
)

TEXT_EMBEDDING_V4 = OpenAIEmbedder(
    id="text-embedding-v4",
    api_key=API_KEY,
    base_url=BASE_URL,
    dimensions=1024,
)
