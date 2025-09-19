from textwrap import dedent

from agno.agent import Agent
from agno.media import Image
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN_VL_PLUS_2025_08_15

agent = Agent(
    model=QWEN_VL_PLUS_2025_08_15,
    description=dedent("""\
        你是一位世界级的视觉记者和文化通讯员，擅长通过讲故事赋予图像生命！📸✨
        拥有侦探般的观察力和畅销作家的叙事才能，你将视觉分析转化为引人入胜的故事，
        既提供信息又吸引读者。\
    """),
    instructions=dedent("""\
        在分析图像和报道新闻时，请遵循以下原则：

        1. 视觉分析：
           - 用相关表情符号开头，制作引人注目的标题
           - 精准分解关键视觉元素
           - 注意其他人可能忽略的细节
           - 将视觉元素与更广泛的背景联系起来

        2. 新闻整合：
           - 研究并核实与图像相关的时事
           - 将历史背景与当下意义相连接
           - 优先保证准确性，同时保持吸引力
           - 在可用情况下加入相关统计或数据

        3. 讲故事风格：
           - 保持专业且引人入胜的语气
           - 使用生动、描述性的语言
           - 相关时引用文化和历史背景
           - 以符合故事的难忘结尾结束

        4. 报道指南：
           - 保持回答简明但有信息量（2-3 段）
           - 平衡事实与人文兴趣
           - 保持新闻职业道德
           - 引用具体信息时注明来源

        将每幅图像转化为引人入胜的新闻故事，让人既获得信息又受到启发！\
    """),
    tools=[DuckDuckGoTools()],
    markdown=False,
    debug_mode=True,
    debug_level=2,
)

# 示例用法：使用著名地标
agent.print_response(
    "讲述这张图片的内容并分享最新相关新闻。",
    images=[
        Image(
            url="https://media.gq.com.tw/photos/5dbc7de4851a4300088a44c1/16:9/w_2240,c_limit/2017012064964105.jpg"
        )
    ],
    stream=True,
)

# 更多尝试示例：
"""
探索示例提示：
1. "这个地点的历史意义是什么？"
2. "这个地方随时间如何变化？"
3. "这里有哪些文化活动？"
4. "建筑风格及其影响是什么？"
5. "最近有哪些发展影响了该地区？"

示例图片 URL：
1. 埃菲尔铁塔: "https://upload.wikimedia.org/wikipedia/commons/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg"
2. 泰姬陵: "https://upload.wikimedia.org/wikipedia/commons/b/bd/Taj_Mahal%2C_Agra%2C_India_edit3.jpg"
3. 金门大桥: "https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
"""

# 获取响应到变量：
# from rich.pretty import pprint
# response = agent.run(
#     "分析这个地标的建筑风格及最新新闻。",
#     images=[Image(url="YOUR_IMAGE_URL")],
# )
# pprint(response.content)
