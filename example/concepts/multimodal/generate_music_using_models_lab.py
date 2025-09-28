import os
from uuid import uuid4

import requests
from agno.agent import Agent, RunOutput
from agno.tools.models_labs import FileType, ModelsLabTools
from agno.utils.log import logger

from models.models import QWEN3_OMNI_FLASH_2025_09_15

agent = Agent(
    name="ModelsLab 音乐智能体",
    id="ml_music_agent",
    model=QWEN3_OMNI_FLASH_2025_09_15,
    tools=[ModelsLabTools(wait_for_completion=True, file_type=FileType.MP3)],
    description="你是一个可以通过 ModelsLabs API 生成音乐的 AI 智能体。",
    instructions=[
        "在生成音乐时，使用 `generate_media` 工具，并提供详细的提示信息，包括：",
        "- 音乐的流派和风格（如古典、爵士、电子）",
        "- 包含的乐器和声音",
        "- 节奏、氛围和情绪特质",
        "- 结构（前奏、主歌、副歌、桥段等）",
        "创建丰富且描述性强的提示，准确表达期望的音乐元素。",
        "专注于生成高质量、完整的纯音乐作品。",
    ],
    markdown=True,
    debug_mode=True,
)

music: RunOutput = agent.run("生成一段 30 秒的古典音乐片段")

save_dir = "./audio_generations"

if music.audio is not None and len(music.audio) > 0:
    url = music.audio[0].url
    response = requests.get(url)
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{save_dir}/sample_music{uuid4()}.wav"
    with open(filename, "wb") as f:
        f.write(response.content)
    logger.info(f"音乐已保存到 {filename}")
