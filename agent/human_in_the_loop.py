import json
from textwrap import dedent

import httpx
from agno.agent import Agent
from agno.tools import tool
from agno.utils import pprint
from rich.console import Console
from rich.prompt import Prompt

from models.models import QWEN_PLUS_2025_07_28

console = Console()


@tool(requires_confirmation=True)
def get_top_hackernews_stories(num_stories: int) -> str:
    """获取 Hacker News 的热门故事。

    Args:
        num_stories (int): 要获取的故事数量

    Returns:
        str: 包含故事详情的 JSON 字符串
    """
    # 获取热门故事 ID
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    # 返回故事详情
    all_stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        if "text" in story:
            story.pop("text", None)
        all_stories.append(story)
    return json.dumps(all_stories)


# 初始化代理，具备技术新闻风格和清晰指令
agent = Agent(
    model=QWEN_PLUS_2025_07_28,
    description="一个技术新闻助手，用于获取并总结 Hacker News 的故事",
    instructions=dedent("""\
        你是一名充满热情的技术记者

        你的职责：
        - 以有趣且信息丰富的方式呈现 Hacker News 的故事
        - 清晰总结你收集到的信息

        风格指南：
        - 使用表情符号使你的回答更生动
        - 保持总结简明但有信息量
        - 以友好的科技风格结尾\
    """),
    tools=[get_top_hackernews_stories],
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

# 示例提问：
# - "现在的前三条 HN 热门故事是什么？"
# - "给我看看 Hacker News 最近的一条故事"
# - "获取前五条故事（你可以尝试接受或拒绝确认）"
response = agent.run("获取前 2 条 Hacker News 热门故事？")
if response.is_paused:
    for tool in response.tools:  # type: ignore
        # 请求确认
        console.print(
            f"工具名称 [bold blue]{tool.tool_name}({tool.tool_args})[/] 需要确认。"
        )
        message = (
            Prompt.ask("你想继续吗？", choices=["y", "n"], default="y")
            .strip()
            .lower()
        )

        if message == "n":
            break
        else:
            # 我们在原地更新工具状态
            tool.confirmed = True

    run_response = agent.continue_run(run_response=response)
    pprint.pprint_run_response(run_response)
