from typing import Iterator

from agno.agent import Agent
from agno.run.agent import RunOutputEvent

from models.models import QWEN3_MAX


def get_user_profile(user_id: str = "john_doe") -> dict:
    """获取可在回复中引用的用户资料信息。

    参数:
        user_id: 用户ID
    返回:
        包含用户资料信息的字典
    """
    profiles = {
        "john_doe": {
            "name": "约翰·多",
            "preferences": {
                "communication_style": "专业",
                "topics_of_interest": ["人工智能/机器学习", "软件工程", "金融"],
                "experience_level": "高级",
            },
            "location": "旧金山，加利福尼亚",
            "role": "高级软件工程师",
        }
    }

    return profiles.get(user_id, {"name": "未知用户"})


def get_current_context() -> dict:
    """获取当前上下文信息，例如时间、时区等。"""
    from datetime import datetime

    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "PST",
        "day_of_week": datetime.now().strftime("%A"),
    }


agent = Agent(
    model=QWEN3_MAX,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

# 同步示例
response: Iterator[RunOutputEvent] = agent.run(
    "请根据我的个人资料和兴趣，提供一份今日优先事项的个性化总结。",
    dependencies={
        "user_profile": get_user_profile,
        "current_context": get_current_context,
    },
    add_dependencies_to_context=True,
    stream=True,
    debug_mode=True,
    # debug_level=2,
)



for chunk in response:
    print(chunk.content)


# ------------------------------------------------------------
# 异步示例
# ------------------------------------------------------------
# async def test_async():
#     async_response = await agent.arun(
#         "根据我的个人资料，告诉我本周的重点关注方向，并提供具体建议。",
#         dependencies={
#             "user_profile": get_user_profile,
#             "current_context": get_current_context
#         },
#         add_dependencies_to_context=True,
#         debug_mode=True,
#     )
#
#     print("\n=== 异步运行结果 ===")
#     print(async_response.content)
#
# # 运行异步示例
# import asyncio
# asyncio.run(test_async())

# ------------------------------------------------------------
# 打印回复示例
# ------------------------------------------------------------
# agent.print_response(
#     "请根据我的个人资料和兴趣，提供一份今日优先事项的个性化总结。",
#     dependencies={
#         "user_profile": get_user_profile,
#         "current_context": get_current_context,
#     },
#     add_dependencies_to_context=True,
#     debug_mode=True,
# )
