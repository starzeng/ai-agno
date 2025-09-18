from textwrap import dedent
from typing import List, Optional

import typer
from agno.agent import Agent
from agno.db.base import SessionType
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.session import AgentSession
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType
from rich import print

from models.models import QWEN3_235B_A22B_INSTRUCT_2507, TEXT_EMBEDDING_V4

agent_knowledge = Knowledge(
    vector_db=LanceDb(
        uri="./tmp/lancedb",
        table_name="recipe_knowledge",
        search_type=SearchType.hybrid,
        embedder=TEXT_EMBEDDING_V4,
    ),
)

# 向知识库添加内容
agent_knowledge.add_content(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
)

# 设置数据库
db = SqliteDb(db_file="./tmp/agents.db")


def recipe_agent(user: str = "user"):
    session_id: Optional[str] = None

    # 询问用户是否要开始一个新会话，还是继续一个已有会话
    new = typer.confirm("是否要开始一个新会话？")

    if not new:
        existing_sessions: List[AgentSession] = db.get_sessions(  # type: ignore
            user_id=user, session_type=SessionType.AGENT
        )
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0].session_id

    agent = Agent(
        user_id=user,
        session_id=session_id,
        model=QWEN3_235B_A22B_INSTRUCT_2507,
        instructions=dedent("""\
            你是一位充满热情且知识渊博的泰国料理专家！🧑‍🍳
            想象你是一个温暖、鼓励的烹饪导师，
            又是泰国美食历史学家和文化大使的结合体。

            回答问题时遵循以下步骤：
            1. 首先，在知识库中搜索正宗的泰国菜谱和烹饪信息
            2. 如果知识库中的信息不完整，或用户提出的问题更适合用网络查询，则使用网络搜索补充
            3. 如果在知识库中找到了信息，则无需搜索网络
            4. 永远优先使用知识库中的信息以保证正宗性
            5. 如有需要，用网络搜索补充：
               - 现代改编或食材替代
               - 文化背景和历史背景
               - 额外的烹饪技巧和排错方法

            沟通风格：
            1. 每个回答以一个相关的烹饪表情符号开头
            2. 回答要结构清晰：
               - 简短介绍或背景
               - 主要内容（菜谱、解释或历史）
               - 专业技巧或文化见解
               - 鼓励性的结尾
            3. 对于菜谱，要包括：
               - 食材列表及可能的替代品
               - 清晰、编号的烹饪步骤
               - 成功的小贴士和常见误区
            4. 使用友好、鼓励的语言

            特别功能：
            - 解释不熟悉的泰国食材并建议替代品
            - 分享相关的文化背景和传统
            - 提供适应不同饮食需求的菜谱建议
            - 包含上菜建议和配菜推荐

            每个回答结尾要有一个积极的祝福语，例如：
            - '烹饪愉快！ขอให้อร่อย (祝你用餐愉快)!'
            - '愿你的泰国料理冒险带来欢乐！'
            - '享受你自制的泰式盛宴吧！'

            记住：
            - 始终用知识库验证菜谱的正宗性
            - 明确说明哪些信息来自网络
            - 对所有水平的家庭厨师都要鼓励和支持\
        """),
        db=db,
        knowledge=agent_knowledge,
        tools=[DuckDuckGoTools()],
        # 为代理提供聊天历史记录
        # 我们可以选择：
        # 1. 给代理一个工具来读取聊天记录
        # 2. 自动把聊天记录添加到发给模型的消息中
        #
        # 1. 给代理一个工具来读取聊天记录
        read_chat_history=True,
        # 2. 自动把聊天记录添加到上下文中
        add_history_to_context=True,
        # 添加到消息中的历史响应数
        num_history_runs=5,
        markdown=True,
    )

    print("你即将与一个智能代理进行对话！")
    if session_id is None:
        session_id = agent.session_id
        if session_id is not None:
            print(f"已启动会话: {session_id}\n")
        else:
            print("已启动会话\n")
    else:
        print(f"继续会话: {session_id}\n")

    # 以命令行应用程序方式运行代理
    agent.cli_app(markdown=True)


if __name__ == "__main__":
    typer.run(recipe_agent)
