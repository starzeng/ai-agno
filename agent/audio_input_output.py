import base64
import logging
import os

import dotenv
import requests
from agno.agent import Agent
from agno.media import Audio
from agno.models.dashscope import DashScope
from agno.models.openai import OpenAILike, OpenAIChat

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
dotenv.load_dotenv()

model_1 = DashScope(
    id="qwen-omni-turbo-2025-03-26",
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)
model_2 = OpenAILike(
    id="qwen-omni-turbo-2025-03-26",
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

# Load audio file
url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"
response = requests.get(url)
response.raise_for_status()

# Create agent with audio capabilities
agent = Agent(
    model=OpenAIChat(
        id="qwen-omni-turbo-2025-03-26",
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
        modalities=["text", "audio"],
        audio={"voice": "Cherry", "format": "wav"},
    ),
    markdown=True,
)

# Run with audio input
response = agent.run(
    "这段音频在说什么",
    # TODO 只能想到使用tool生成audio文件返回, 没办法实现qwen base64文件头添加
    audio=[Audio(content=response.content, format="mp3")],
    stream=True,
)

print(response)
