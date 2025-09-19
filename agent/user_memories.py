import json
from textwrap import dedent
from typing import List, Optional

import typer
from agno.agent import Agent
from agno.db.base import SessionType
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.session import AgentSession
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.prompt import Prompt

from models.models import QWEN_PLUS_2025_07_28


def create_agent(user: str = "user"):
    session_id: Optional[str] = None

    # 询问用户是否要开启新会话
    new = typer.confirm("是否要开启新的会话?")

    # 初始化存储（会话和记忆）
    db = SqliteDb(db_file="./tmp/agents.db")

    if not new:
        existing_sessions: List[AgentSession] = db.get_sessions(
            user_id=user, session_type=SessionType.AGENT
        )  # type: ignore
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0].session_id

    agent = Agent(
        model=QWEN_PLUS_2025_07_28,
        user_id=user,
        session_id=session_id,
        enable_user_memories=True,  # 启用用户记忆
        enable_session_summaries=True,  # 启用会话总结
        db=db,
        add_history_to_context=True,  # 将历史记录加入上下文
        num_history_runs=3,
        # 加强的系统提示词，用于更好地利用个性和记忆
        description=dedent("""\
        你是一名乐于助人、友好的 AI 助手，并且具有优秀的记忆能力。
        - 记住关于用户的重要细节，并自然地引用它们
        - 保持温暖积极的语气，同时准确和有帮助
        - 在合适的时候，回顾之前的对话和记忆
        - 始终如实说明你记得或不记得的内容"""),
    )

    if session_id is None:
        session_id = agent.session_id
        if session_id is not None:
            print(f"已开启新会话: {session_id}\n")
        else:
            print("已开启新会话\n")
    else:
        print(f"继续会话: {session_id}\n")

    return agent


def print_agent_memory(agent):
    """打印当前智能体的记忆系统状态"""
    console = Console()

    # 打印聊天历史
    messages = agent.get_messages_for_session()
    console.print(
        Panel(
            JSON(
                json.dumps(
                    [m.model_dump(include={"role", "content"}) for m in messages],
                    indent=4,
                ),
            ),
            title=f"会话历史 (session_id: {agent.session_id})",
            expand=True,
        )
    )

    # 打印用户记忆
    user_memories = agent.get_user_memories(user_id=agent.user_id)
    if user_memories:
        memories_data = [memory.to_dict() for memory in user_memories]
        console.print(
            Panel(
                JSON(json.dumps(memories_data, indent=4)),
                title=f"用户记忆 (user_id: {agent.user_id})",
                expand=True,
            )
        )

    # 打印会话总结
    try:
        session_summary = agent.get_session_summary()
        if session_summary:
            console.print(
                Panel(
                    JSON(
                        json.dumps(session_summary.to_dict(), indent=4),
                    ),
                    title=f"会话总结 (session_id: {agent.session_id})",
                    expand=True,
                )
            )
        else:
            console.print(
                "会话总结: 尚未生成（需要多次交互后才会创建）"
            )
    except Exception as e:
        console.print(f"会话总结错误: {e}")


def main(user: str = "user"):
    """交互式聊天循环，并展示记忆"""
    agent = create_agent(user)

    print("可以尝试以下示例输入：")
    print("- '我叫 [名字]，住在 [城市]'")
    print("- '我喜欢 [爱好/兴趣]'")
    print("- '你记得我什么？'")
    print("- '我们到目前为止聊了什么？'\n")

    exit_on = ["退出", "再见", "拜拜"]
    while True:
        message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
        if message in exit_on:
            break

        agent.print_response(input=message, stream=True, markdown=True)
        print_agent_memory(agent)


if __name__ == "__main__":
    typer.run(main)
