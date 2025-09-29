from agno.agent import Agent, RunOutput
from agno.utils.audio import write_audio_to_file

from models.models import QWEN3_TTS_FLASH

audio_agent = Agent(
    model=QWEN3_TTS_FLASH,
    description="一个能用自然语言生成音频的助手。",
    instructions="用自然语言生成音频,返回生成音频。",
    debug_mode=True,
    debug_level=2,
    stream=True,
)

audio_story: RunOutput = audio_agent.run(
    "用生动的方式朗读这个故事: 远山染霞，孤舟轻荡，渔火点点，归人未还。"
)
print(audio_story)
