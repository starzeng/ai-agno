import os

import dotenv
from agno.models.dashscope import DashScope

from my_ext.dashscop_embedder import DashScopeEmbedder

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

QWEN3_235B_A22B = DashScope(
    id="qwen3-235b-a22b",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False,
    temperature=0.3,
)
QWEN3_TTS_FLASH = DashScope(
    id="qwen3-tts-flash",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False,
    temperature=0.7,
    modalities=["text", "audio"],
    audio={"voice": "Cherry", "format": "wav"},
)
QWEN3_OMNI_FLASH_2025_09_15 = DashScope(
    id="qwen3-omni-flash-2025-09-15",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False,
    temperature=0.7,
    modalities=["text", "audio"],
    audio={"voice": "Cherry", "format": "wav"},
)

QWEN_PLUS_2025_07_14 = DashScope(
    id="qwen-plus-2025-07-14",
    api_key=API_KEY,
    base_url=BASE_URL,
    # modalities=["text", "audio"],
    # audio={"voice": "Cherry", "format": "wav"},
    enable_thinking=False,
    temperature=0.3,
)

QWEN_OMNI_TURBO_LATEST_2025_03_26 = DashScope(
    id="qwen-omni-turbo-2025-03-26",
    api_key=API_KEY,
    base_url=BASE_URL,
    modalities=["text", "audio"],
    audio={"voice": "Cherry", "format": "wav"},
    enable_thinking=False,
    temperature=0.3,
)

WAN22_T2V_PLUS = DashScope(
    id="wan2.2-t2v-plus",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False,
    temperature=0.3,
)

QWEN_IMAGE = DashScope(
    id="qwen-image",
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
)

QWEN_PLUS = DashScope(
    id="qwen-plus",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False,
    temperature=0.3,
)

QWEN_PLUS_2025_04_28 = DashScope(
    id="qwen-plus-2025-04-28",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False,
    temperature=0.3,
)
QWEN_OMNI_TURBO_2025_03_26 = DashScope(
    id="qwen-omni-turbo-2025-03-26",
    api_key=API_KEY,
    base_url=BASE_URL,
)

QWEN_PLUS_2025_07_28 = DashScope(
    id="qwen-plus-2025-07-28",
    api_key=API_KEY,
    base_url=BASE_URL,
    enable_thinking=False,
    temperature=0.3,
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

QWEN3_MAX = DashScope(
    id="qwen3-max",
    api_key=API_KEY,
    base_url=BASE_URL,
)

QWEN3_235B_A22B_INSTRUCT_2507 = DashScope(
    id="qwen3-235b-a22b-instruct-2507",
    api_key=API_KEY,
    base_url=BASE_URL,
)

TEXT_EMBEDDING_V4 = DashScopeEmbedder(
    id="text-embedding-v4",
    api_key=API_KEY,
    base_url=BASE_URL,
    dimensions=128,
)
