import base64
import logging
import os

import dotenv
from openai import OpenAI

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

dotenv.load_dotenv()


def encode_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")


base64_audio = encode_audio("./tmp/audio.wav")
completion = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
).chat.completions.create(
    model="qwen-omni-turbo-2025-03-26",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这段音频在说什么"},
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": f"data:;base64,{base64_audio}",
                        "format": "mp3",
                    },
                },
            ],
        },
    ],
    # 设置输出数据的模态，当前支持两种：["text","audio"]、["text"]
    modalities=["text", "audio"],
    audio={"voice": "Cherry", "format": "wav"},
    # stream 必须设置为 True，否则会报错
    stream=True,
    stream_options={"include_usage": True},
)

for chunk in completion:
    if chunk.choices:
        print(chunk.choices[0].delta)
    else:
        print(chunk.usage)
