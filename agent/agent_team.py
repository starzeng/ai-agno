import os
from textwrap import dedent

import dotenv
from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.exa import ExaTools

from models.models import QWEN_PLUS_2025_07_14

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

web_agent = Agent(
    name="Web Agent",
    role="搜索网络信息",
    model=QWEN_PLUS_2025_07_14,
    tools=[DuckDuckGoTools()],
    instructions=dedent("""\
        你是一名经验丰富的网络研究员和新闻分析师！🔍

        搜索信息时遵循以下步骤：
        1. 从最新且最相关的来源开始
        2. 对多个来源的信息进行交叉验证
        3. 优先考虑权威新闻媒体和官方来源
        4. 始终附上带链接的引用
        5. 重点关注影响市场的新闻和重大进展

        风格指南：
        - 以清晰、新闻报道的风格呈现信息
        - 使用项目符号突出要点
        - 包含相关引文（如有）
        - 指明每条新闻的日期和时间
        - 突出市场情绪和行业趋势
        - 以简要分析整体叙事收尾
        - 特别关注监管新闻、财报和战略公告\
    """),
    markdown=True,
    debug_level=2,
    debug_mode=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="获取金融数据",
    model=QWEN_PLUS_2025_07_14,
    tools=[
        ExaTools(
            include_domains=["trendlyne.com"],
            text=False,
            show_results=True,
            highlights=False,
        )
    ],
    instructions=dedent("""\
        你是一名擅长市场数据的金融分析师！📊

        分析金融数据时遵循以下步骤：
        1. 从最新股价、成交量和当日波动区间开始
        2. 提供详细的分析师推荐和一致目标价
        3. 包括关键指标：市盈率、市值、52周区间
        4. 分析交易模式和成交量趋势
        5. 将表现与相关行业指数进行比较

        风格指南：
        - 用表格展示结构化数据
        - 每个数据部分要有清晰标题
        - 对技术术语做简要解释
        - 用表情符号标注显著变化 (📈 📉)
        - 用项目符号提供快速洞察
        - 将当前值与历史均值对比
        - 以数据驱动的金融前景收尾\
    """),
    markdown=True,
    debug_level=2,
    debug_mode=True,
)

agent_team = Team(
    members=[web_agent, finance_agent],
    model=QWEN_PLUS_2025_07_14,
    instructions=dedent("""\
        你是知名财经新闻编辑部的主编！📰

        你的角色：
        1. 协调网络研究员和金融分析师的工作
        2. 将他们的发现整合为有说服力的叙事
        3. 确保所有信息都有来源并已验证
        4. 提供兼顾新闻和数据的平衡视角
        5. 突出关键风险和机会

        风格指南：
        - 以吸引眼球的标题开篇
        - 从有力的执行摘要开始
        - 先呈现金融数据，再提供新闻背景
        - 在不同类型信息之间使用清晰的分隔
        - 包含相关图表或表格（如有）
        - 添加“市场情绪”部分描述当前氛围
        - 在结尾加入“关键要点”部分
        - 必要时增加“风险因素”
        - 以“市场观察团队”和当前日期署名收尾\
    """),
    add_datetime_to_context=True,
    markdown=True,
    show_members_responses=True,
    debug_level=2,
    debug_mode=True,
)

# 使用示例，处理不同类型查询
# agent_team.print_response(
#     input="总结 NVDA 的分析师推荐并分享最新新闻",
#     stream=True,
# )
# agent_team.print_response(
#     input="AI 半导体公司的市场前景和财务表现如何？",
#     stream=True,
# )
# agent_team.print_response(
#     input="分析 TSLA 的最新动态和财务表现",
#     stream=True,
# )
agent_team.print_response(
    input="分析 AI应用 的最新动态",
    stream=True,
)

# 更多可尝试的提示：
"""
进阶查询示例：
1. "比较主要云服务商 (AMZN, MSFT, GOOGL) 的财务表现和最新新闻"
2. "美联储近期决策对银行股的影响如何？重点关注 JPM 和 BAC"
3. "通过 ATVI、EA 和 TTWO 的表现分析游戏行业前景"
4. "社交媒体公司表现如何？比较 META 和 SNAP"
5. "AI 芯片制造商的最新情况和市场地位如何？"
"""
