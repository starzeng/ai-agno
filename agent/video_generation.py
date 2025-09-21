from textwrap import dedent

from agno.agent import Agent
from agno.run.agent import RunOutput

from models.models import QWEN_PLUS_2025_04_28
from my_tools.qwen_video_tools import QwenVideoTools

# 创建一个创意型 AI 视频导演 Agent
video_agent = Agent(
    model=QWEN_PLUS_2025_04_28,
    tools=[QwenVideoTools()],
    description=dedent("""\
        你是一名经验丰富的 AI 视频导演，擅长多种视频风格，
        从自然场景到艺术动画。你对运动、时间节奏和
        通过视频进行视觉叙事有深刻理解。\
    """),
    instructions=dedent("""\
        作为 AI 视频导演，请遵循以下准则：
        1. 仔细分析用户请求，理解所需的风格与氛围
        2. 在生成之前，增强提示词，加入关于运动、时间和氛围的细节
        3. 使用 `generate_video` 工具并提供详细且精心设计的提示词
        4. 将工具生成的结果输出

        视频链接将在界面中自动显示在你的回复下方。\
    """),
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

# 示例用法
video_agent.print_response(
    "生成一段舒适壁炉中火焰跳动的视频"
)

# 获取并展示生成的视频
run_response = video_agent.get_last_run_output()
# todo 没有解决工具返回数据的问题
if run_response and run_response.videos:
    for video in run_response.videos:
        print(f"生成的视频地址: {video.url}")

# 更多示例提示：
"""
尝试以下创意提示：
1. "创建一段秋叶在宁静森林中飘落的视频"
2. "生成一段猫玩球的视频"
3. "创建一段宁静锦鲤池塘中水面荡漾的视频"
4. "生成一段舒适壁炉中火焰跳动的视频"
5. "创建一段神秘传送门在魔法领域中开启的视频"
"""
