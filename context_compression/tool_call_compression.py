"""
[上下文压缩提示词]

你正在压缩工具调用结果以节省上下文空间，同时保留关键信息。

你的目标：仅从工具输出中提取必要信息。

必须保留：
• 具体事实：数字、统计数据、金额、价格、数量、指标
• 时间数据：日期、时间、时间戳（使用短格式："Oct 21 2025"）
• 实体：人物、公司、产品、地点、组织
• 标识符：URL、ID、代码、技术标识符、版本
• 关键引用、引文、来源（如果与代理任务相关）

压缩至 essentials：
• 描述：仅保留关键属性
• 解释：提炼为核心见解
• 列表：根据代理上下文关注最相关项目
• 背景：仅保留关键的最小上下文

完全移除：
• 引言、结论、过渡语句
• 犹豫语言（"可能"、"似乎"、"看起来"）
• 元评论（"根据"、"结果显示"）
• 格式化工件（markdown、HTML、JSON结构）
• 冗余或重复信息
• 与代理任务无关的通用背景
• 宣传语言、填充词

示例：
输入："根据最近的市场分析和行业报告，OpenAI在技术领域做出了几项重要公告。该公司于2025年10月21日发布了ChatGPT Atlas，这是一款专为macOS用户设计的新AI浏览器应用。该浏览器战略性地定位于与传统搜索引擎竞争。此外，OpenAI于2025年10月6日推出了ChatGPT中的应用程序，其中包括面向开发者的综合软件开发工具包(SDK)。该公司还宣布了几家初始战略合作伙伴将集成这一新功能，包括知名公司如Spotify（流行音乐流媒体服务）、Zillow（房地产市场平台）和Canva（图形设计平台）。"

输出："OpenAI - Oct 21 2025: ChatGPT Atlas (AI浏览器, macOS, 搜索竞争对手); Oct 6 2025: Apps in ChatGPT + SDK; 合作伙伴: Spotify, Zillow, Canva"

保持简洁同时保留所有关键事实。

"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[DuckDuckGoTools()],
    description="专门跟踪竞争对手活动",
    instructions="使用搜索工具，并始终使用最新信息和数据。",
    db=SqliteDb(db_file="./dbs/tool_call_compression.db"),
    compress_tool_results=True,  # 启用工具调用压缩
    debug_mode=True,
    debug_level=2,
)

agent.print_response(
    """
    使用搜索工具，并始终获取最新信息和数据。
    研究以下AI公司的近期活动（最近一天）：

    1. OpenAI - 产品发布、合作伙伴关系、定价
    2. Anthropic - 新功能、企业合作、融资
    3. Google DeepMind - 研究突破、产品发布
    4. Meta AI - 开源发布、研究论文

    对于每家公司，找出具体的行动及其日期和数字。""",
    stream=True,
)
