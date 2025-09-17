import json
from textwrap import dedent

import httpx
from agno.agent import Agent

from models.models import QWEN3_MAX_PREVIEW


def get_top_hackernews_stories(num_stories: int = 10) -> str:
    """使用此函数获取Hacker News的热门故事。
    参数:
        num_stories (int): 返回的故事数量。默认为10。
    返回:
        str: 热门故事的JSON字符串。
    """

    # Fetch top story IDs
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    # Fetch story details
    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        if "text" in story:
            story.pop("text", None)
        stories.append(story)
    return json.dumps(stories)


agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    instructions=dedent("""\
        你是一位精通技术的Hacker News记者，对所有科技事物充满热情！🤖
        把自己想象成硅谷内部人士和技术记者的结合体。
        
        你的风格指南：
        - 以引人注目的科技标题开始，使用表情符号
        - 以热情和前沿科技态度呈现Hacker News故事
        - 保持回复简洁但内容丰富
        - 适当时使用科技行业参考和初创公司术语
        - 以吸引人的科技主题结束语结尾，如"回到终端！"或"推送到生产环境！"
        
        记住在保持高度科技热情的同时彻底分析HN故事！\
            """),
    tools=[get_top_hackernews_stories],
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("总结Hacker News上的前5个故事？", stream=True)
