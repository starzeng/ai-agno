from textwrap import dedent
from typing import List

from agno.agent import Agent, RunOutput  # noqa
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field

from models.models import QWEN3_MAX_PREVIEW


class MovieScript(BaseModel):
    setting: str = Field(
        ...,
        description="对电影主要地点和时间时期的丰富详细、富有氛围的描述。包括感官细节和情绪。",
    )
    ending: str = Field(
        ...,
        description="电影强有力的结局，将所有情节线索联系在一起。应该带来情感冲击和满足感。",
    )
    genre: str = Field(
        ...,
        description="电影的主要和次要类型（例如，'科幻惊悚片'，'浪漫喜剧'）。应该与背景和基调一致。",
    )
    name: str = Field(
        ...,
        description="引人注目、令人难忘的标题，捕捉故事的精髓并吸引目标观众。",
    )
    characters: List[str] = Field(
        ...,
        description="4-6个主要角色，具有独特的名字和简短的角色描述（例如，'陈莎拉 - 有黑暗秘密的杰出量子物理学家'）。",
    )
    storyline: str = Field(
        ...,
        description="引人入胜的三句话情节摘要：设置、冲突和利害关系。用神秘和情感吸引读者。",
    )


# Agent that uses JSON mode
# 使用JSON模式的代理
json_mode_agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    description=dedent("""\
        你是一位著名的 Hollywood 编剧，以创作难忘的大片而闻名！🎬
        结合了 Christopher Nolan、Aaron Sorkin 和 Quentin Tarantino 的叙事能力，
        你创作出能吸引全球观众的独特故事。

        你的专长是将地点转化为推动叙事的活生生的角色。\
    """),
    instructions=dedent("""\
        在创作电影概念时，遵循以下原则：

        1. 地点应该是角色：
           - 用感官细节让地点活起来
           - 包括影响故事的大气元素
           - 考虑时间 period 对叙事的影响

        2. 角色发展：
           - 给每个角色独特的声音和明确的动机
           - 创造引人入胜的关系和冲突
           - 确保多样化的表现和真实的背景

        3. 故事结构：
           - 以抓住注意力的钩子开始
           - 通过升级的冲突建立紧张感
           - 提供令人惊讶但不可避免的结局

        4. 类型掌握：
           - 拥抱类型惯例同时添加新鲜的转折
           - 深思熟虑地混合类型以获得独特的组合
           - 始终保持一致的基调

        将每个地点转化为难忘的电影体验！\
    """),
    output_schema=MovieScript,
    use_json_mode=True,
    debug_mode=True,
    debug_level=2,
)

# Agent that uses structured outputs
# 使用结构化输出的代理
structured_output_agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    description=dedent("""\
        你是一位著名的 Hollywood 编剧，以创作难忘的大片而闻名！🎬
        结合了 Christopher Nolan、Aaron Sorkin 和 Quentin Tarantino 的叙事能力，
        你创作出能吸引全球观众的独特故事。

        你的专长是将地点转化为推动叙事的活生生的角色。\
    """),
    instructions=dedent("""\
        在创作电影概念时，遵循以下原则：

        1. 地点应该是角色：
           - 用感官细节让地点活起来
           - 包括影响故事的大气元素
           - 考虑时间 period 对叙事的影响

        2. 角色发展：
           - 给每个角色独特的声音和明确的动机
           - 创造引人入胜的关系和冲突
           - 确保多样化的表现和真实的背景

        3. 故事结构：
           - 以抓住注意力的钩子开始
           - 通过升级的冲突建立紧张感
           - 提供令人惊讶但不可避免的结局

        4. 类型掌握：
           - 拥抱类型惯例同时添加新鲜的转折
           - 深思熟虑地混合类型以获得独特的组合
           - 始终保持一致的基调

        将每个地点转化为难忘的电影体验！\
    """),
    output_schema=MovieScript,
    # use_json_mode=True,
    debug_mode=True,
    debug_level=2,
)

# 使用不同地点的示例用法
json_mode_agent.print_response("中国", stream=True)
print("#### ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ####")
print("#### ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ####")
print("#### ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ######## ## # ## ####")
structured_output_agent.print_response("古罗马", stream=True)

# 更多尝试的示例：
"""
探索的创意地点提示：
1. "水下研究站" - 用于幽闭恐怖的科幻惊悚片
2. "维多利亚时代的伦敦" - 用于哥特式神秘片
3. "2050年的迪拜" - 用于未来主义抢劫电影
4. "南极研究基地" - 用于生存恐怖故事
5. "加勒比海岛" - 用于热带冒险浪漫片
"""

# 要将响应存储在变量中：
# from rich.pretty import pprint

# json_mode_response: RunOutput = json_mode_agent.run("纽约")
# pprint(json_mode_response.content)
# structured_output_response: RunOutput = structured_output_agent.run("纽约")
# pprint(structured_output_response.content)
