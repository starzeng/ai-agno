from agno.agent import Agent
from agno.utils.audio import write_audio_to_file

from models.models import QWEN3_TTS_FLASH
agent = Agent(
    model=QWEN3_TTS_FLASH,
    instructions="""回答限制20字以内.""",
    add_history_to_context=True,
    stream=True,
    debug_mode=True,
    debug_level=2,
)

response_1 = agent.run("你还好吗？")
if response_1.response_audio is not None:
    write_audio_to_file(
        audio=response_1.response_audio.content, filename="./tmp/answer_1.wav"
    )

response_2 = agent.run("说爱我？")
if response_2.response_audio is not None:
    write_audio_to_file(
        audio=response_2.response_audio.content, filename="./tmp/answer_2.wav"
    )
