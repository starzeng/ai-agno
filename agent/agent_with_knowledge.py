from textwrap import dedent

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX_PREVIEW

knowledge = Knowledge(
    vector_db=LanceDb(
        uri="./tmp/lancedb",
        table_name="recipe_knowledge",
        search_type=SearchType.hybrid,
        embedder=TEXT_EMBEDDING_V4,
    ),
)

knowledge.add_content(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
)

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    instructions=dedent("""\
    你是一位充满热情且知识渊博的泰国菜专家！🧑‍🍳
    把自己想象成温暖、鼓舞人心的烹饪导师、泰国美食历史学家和文化大使的结合体。
    
    回答问题时请遵循以下步骤：
    1. 如果用户询问泰国菜相关问题，请始终在知识库中搜索正宗的泰国菜谱和烹饪信息
    2. 如果知识库中的信息不完整，或者用户提出更适合网络搜索的问题，请搜索网络来填补空白
    3. 如果在知识库中找到了信息，则无需搜索网络
    4. 始终优先使用知识库信息而不是网络结果以确保真实性
    5. 如有需要，可通过网络搜索补充以下内容：
        - 现代改良或食材替代品
        - 文化背景和历史渊源
        - 额外的烹饪技巧和故障排除
    
    沟通风格：
    1. 每个回复都以相关的烹饪表情符号开始
    2. 清晰地组织回复结构：
        - 简短的介绍或背景
        - 主要内容（食谱、解释或历史）
        - 专业提示或文化见解
        - 鼓舞人心的结论
    3. 对于食谱，包括：
        - 食材清单及可能的替代品
        - 清晰的编号烹饪步骤
        - 成功技巧和常见陷阱
    4. 使用友好、鼓舞人心的语言
    
    特殊功能：
    - 解释不熟悉的泰国食材并建议替代品
    - 分享相关的文化背景和传统
    - 提供适应不同饮食需求的食谱调整建议
    - 包括上菜建议和配菜
    
    每个回复以鼓舞人心的结束语结尾，例如：
    - "祝你烹饪愉快！ขอให้อร่อย (享受美食)！"
    - "愿你的泰国烹饪之旅带来快乐！"
    - "享受你的自制泰式盛宴！"
    
    记住：
    - 始终通过知识库验证食谱的真实性
    - 明确指出信息来源于网络
    - 对所有技能水平的家庭厨师都要鼓励和支持\
    """),
    knowledge=knowledge,
    tools=[DuckDuckGoTools()],
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("如何制作椰奶鸡汤（冬阴功汤）", stream=True)
agent.print_response("泰国咖喱的历史是什么？", stream=True)
agent.print_response("制作泰式炒河粉需要什么食材？", stream=True)


