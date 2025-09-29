import os
import time

import dashscope
import dotenv
from agno.utils.media import download_video

dotenv.load_dotenv()

text = "有点远,不想去!"
response = dashscope.audio.qwen_tts.SpeechSynthesizer.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text=text,
    voice="Cherry",
)

url = response.output.audio['url']

download_video(url, f"./tmp/sample_story_{time.time()}.wav")
