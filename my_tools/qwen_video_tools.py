import logging
import os
from http import HTTPStatus
from typing import Optional
from uuid import uuid4

import dotenv
from agno.media import Video
from agno.tools import Toolkit
from agno.tools.function import ToolResult
from dashscope import VideoSynthesis

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class QwenVideoTools(Toolkit):
    def __init__(
            self,
            api_key: Optional[str] = None,
            model: str = "wan2.2-t2v-plus"
    ):
        super().__init__(name="qwen_video_tools")
        dotenv.load_dotenv()
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.model = model

        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY is required")

        self.register(self.generate_video)

    def generate_video(
            self,
            prompt: str,
            size: str = "1920*1080",
    ) -> ToolResult | None:
        """使用Qwen生成视频

        Args:
            prompt: 视频描述文本
            size: 视频尺寸，默认1920*1080

        Returns:
            生成结果描述
        """
        try:
            logger.info(f"开始生成视频，提示词: {prompt}")

            # 构建参数
            params = {
                'model': self.model,
                'api_key': self.api_key,
                'prompt': prompt,
                'size': size,
            }

            # 调用DashScope API
            rsp = VideoSynthesis.call(**params)
            logger.info(f"DashScope API 调用结果: {rsp}")

            if rsp.status_code == HTTPStatus.OK:
                video_url = rsp.output.video_url
                original_prompt = rsp.output.orig_prompt
                revised_prompt = rsp.output.actual_prompt
                logger.info(f"视频生成成功: {video_url}")
                response_str = f"视频生成成功！\n视频URL: {video_url}\n提示词: {prompt}\n尺寸: {size}"
                generated_videos = []
                video = Video(
                    id=str(uuid4()),
                    url=video_url,
                    original_prompt=original_prompt,
                    revised_prompt=revised_prompt,
                )
                generated_videos.append(video)
                return ToolResult(
                    content=response_str or "No video were generated",
                    videos=generated_videos if generated_videos else None,
                )
            else:
                error_msg = f"视频生成失败 - 状态码: {rsp.status_code}, 错误码: {rsp.code}, 消息: {rsp.message}"
                logger.error(error_msg)
                return ToolResult(content=error_msg)

        except Exception as e:
            error_msg = f"视频生成异常: {str(e)}"
            logger.error(error_msg)
            return ToolResult(content=error_msg)
