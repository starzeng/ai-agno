from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.run.agent import RunOutput
from agno.tools.dalle import DalleTools

from models.models import QWEN_PLUS_2025_04_28
from my_tools.qwen_image_tools import QwenImageTools

# 创建一个创意 AI 艺术家智能体
image_agent = Agent(
    model=QWEN_PLUS_2025_04_28,
    tools=[QwenImageTools()],
    description=dedent("""\
        你是一名经验丰富的 AI 艺术家，精通从写实到抽象等多种艺术风格。
        你对构图、色彩理论和视觉叙事有深刻理解。\
    """),
    instructions=dedent("""\
        作为一名 AI 艺术家，请遵循以下指南：
        1. 仔细分析用户的请求，理解所需的风格与氛围
        2. 在生成前，优化提示词，加入光影、视角和氛围等艺术细节
        3. 使用 `create_image` 工具，并提供详细精炼的提示词
        4. 简要说明所做的艺术选择
        5. 如果请求不明确，询问用户的风格偏好

        始终致力于创作视觉震撼且富有意义的作品，以捕捉用户的想象！\
    """),
    markdown=False,
    db=SqliteDb(session_table="test_agent", db_file="./tmp/test.db"),
    debug_mode=True,
    debug_level=2,
)

# 示例用法
image_agent.print_response(
    "生成一个蒸汽朋克风格的小提琴机器人"
)

# 获取并展示生成的图像
run_response = image_agent.get_last_run_output()
if run_response and isinstance(run_response, RunOutput):
    for image_response in run_response.images:
        image_url = image_response.url
        print("image_url: ", image_url)
else:
    print("No images found or images is not a list")

# 更多创意提示示例：
"""
尝试以下创意提示：
1. "生成一个蒸汽朋克风格的小提琴机器人"
2. "设计一个樱花季的静谧禅意花园"
3. "创作一座拥有生物发光建筑的水下城市"
4. "生成一间雪夜森林中的温馨木屋"
5. "创作一座有飞行汽车与摩天大楼的未来城市景观"
"""
