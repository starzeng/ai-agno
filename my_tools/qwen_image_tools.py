import logging
import os
from typing import Optional

import dotenv
from agno.media import Image
from agno.tools import Toolkit
from agno.tools.function import ToolResult
from dashscope import MultiModalConversation

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class QwenImageTools(Toolkit):
    def __init__(
            self,
            api_key: Optional[str] = None,
    ):
        super().__init__(name="qwen_image_tools")
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")

        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY is required")

        self.register(self.generate_image)

    def generate_image(self, prompt: str, ) -> ToolResult | None:
        """使用Qwen-Image生成图片

        Args:
            prompt: 图片描述文本

        Returns:
            生成结果描述
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"{prompt}"
                    }
                ]
            }
        ]

        response = MultiModalConversation.call(
            api_key=self.api_key,
            model="qwen-image",
            messages=messages,
            result_format='message',
            stream=False,
            watermark=True,
            prompt_extend=True,
            negative_prompt='',
            size='1328*1328'
        )

        if response.status_code == 200:
            images = []
            for choice in response.output.choices:
                for url in choice.message.content:
                    images.append(Image(url=url))
            return ToolResult(
                content=prompt,
                images=images
            )
        else:
            logger.debug(f"HTTP返回码：{response.status_code}")
            logger.debug(f"错误码：{response.code}")
            logger.debug(f"错误信息：{response.message}")
            logger.debug("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
            return None
