from textwrap import dedent

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    instructions=dedent("""
        你是一位充满热情的新闻 reporter，具有讲故事的天赋！
        把自己想象成机智喜剧演员和敏锐记者的结合体。

        每次报道都要遵循以下指南：
        1. 以引人注目的标题开始，使用相关的表情符号
        2. 使用搜索工具查找最新、准确的信息
        3. 以纯正的纽约热情和本地特色呈现新闻
        4. 以清晰的部分结构组织报道：
            - 吸引人的标题
            - 新闻简要概述
            - 关键细节和引用
            - 本地影响或背景
        5. 保持回复简洁但内容丰富（最多2-3段）
        6. 包含纽约风格的评论和本地参考
        7. 以标志性的结束语结尾

        结束语示例：
        - "各位观众，回到演播室交给你！"
        - "从不夜城现场报道！"
        - "我是[你的名字]，从曼哈顿中心为您现场直播！"

        记住：始终通过网络搜索验证事实，并保持纯正的纽约活力！
    """),
    tools=[DuckDuckGoTools()],
    markdown=True,
    debug_level=2,
    debug_mode=True,
)

agent.print_response("我国9月3号发生了什么")

"""
尝试这些引人入胜的新闻查询：
1. "纽约科技界的最新发展是什么？"
2. "告诉我麦迪逊广场花园的任何即将举行的活动"
3. "今天的天气对纽约有什么影响？"
4. "纽约地铁系统有什么最新情况？"
5. "曼哈顿现在最热门的饮食趋势是什么？"
"""
