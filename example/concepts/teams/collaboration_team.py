import asyncio
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.team import Team
from agno.tools.arxiv import ArxivTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools

from models.models import QWEN3_MAX_PREVIEW

arxiv_download_dir = Path(__file__).parent.joinpath("./tmp", "arxiv_pdfs__{session_id}")
arxiv_download_dir.mkdir(parents=True, exist_ok=True)

academic_paper_researcher = Agent(
    name="Academic Paper Researcher",
    model=QWEN3_MAX_PREVIEW,
    role="研究学术论文和学术内容",
    tools=[GoogleSearchTools(), ArxivTools(download_dir=arxiv_download_dir)],
    add_name_to_context=True,
    instructions=dedent("""
    你是一名学术论文研究员。
    你会在学术文献中收到一个研究主题。
    你需要找到相关的学术文章、论文和学术讨论。
    专注于同行评议的内容和知名来源的引用。
    提供关键发现和方法论的简要摘要。
    """),
    debug_mode=True,
    debug_level=2,
)

twitter_researcher = Agent(
    name="Twitter Researcher",
    model=QWEN3_MAX_PREVIEW,
    role="研究热门讨论和实时更新",
    tools=[DuckDuckGoTools()],
    add_name_to_context=True,
    instructions=dedent("""
    你是一名Twitter/X研究员。
    你会在Twitter/X上收到一个研究主题。
    你需要找到热门讨论、有影响力的声音和实时更新。
    尽可能关注已验证账户和可信来源。
    跟踪相关的话题标签和正在进行的对话。
    """),
    debug_mode=True,
    debug_level=2,
)

agent_team = Team(
    name="Discussion Team",
    model=QWEN3_MAX_PREVIEW,
    members=[
        academic_paper_researcher,
        twitter_researcher,
    ],
    instructions=[
        "你是一名讨论主持人。",
        "当你认为团队已达成共识时，你需要停止讨论。",
    ],
    markdown=True,
    show_members_responses=True,
    debug_mode=True,
    debug_level=2,
)

asyncio.run(
    agent_team.aprint_response(
        input="开始讨论主题：'学习编程的最佳方式是什么？'",
        stream=True,
        stream_events=True,
        debug_mode=True,
    )
)
