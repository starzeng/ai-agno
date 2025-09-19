import json
from textwrap import dedent

import httpx
from agno.agent import Agent

from models.models import QWEN_PLUS_2025_07_28


def get_top_hackernews_stories(num_stories: int = 5) -> str:
    """获取并返回 HackerNews 的头条故事。

    参数:
        num_stories: 要检索的头条数量（默认: 5）
    返回:
        包含故事详情（标题、链接、分数等）的 JSON 字符串
    """
    # 获取头条故事
    stories = [
        {
            k: v
            for k, v in httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
        )
        .json()
        .items()
            if k != "kids"  # 排除讨论线程
        }
        for id in httpx.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json"
        ).json()[:num_stories]
    ]
    return json.dumps(stories, indent=4)


# 创建一个上下文感知的代理，可以访问实时的 HackerNews 数据
agent = Agent(
    model=QWEN_PLUS_2025_07_28,
    # 上下文中的每个函数在代理运行时被求值，
    # 可以把它视为对 Agent 的依赖注入
    dependencies={"top_hackernews_stories": get_top_hackernews_stories},
    # 或者，你可以手动将上下文添加到指令中。这里会自动解析。
    instructions=dedent("""\
        你是一位具有洞察力的科技趋势观察者！📰

        以下是 HackerNews 的头条故事：
        {top_hackernews_stories}\
    """),
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

# 示例用法
agent.print_response(
    "目前热门的技术讨论是什么？",
    stream=True,
)
