import json
from typing import List, Optional

import typer
from agno.agent import Agent
from agno.db.base import SessionType
from agno.db.sqlite import SqliteDb
from agno.session import AgentSession
from rich import print
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.prompt import Prompt

from models.models import QWEN_PLUS_2025_07_28

console = Console()


def create_agent(user: str = "user"):
    session_id: Optional[str] = None

    # 询问用户是否要开启新会话
    new = typer.confirm("是否要开启新的会话?")

    # 如果用户不想开启新会话，则尝试获取已有会话
    db = SqliteDb(db_file="./tmp/agents.db")

    if not new:
        existing_sessions: List[AgentSession] = db.get_sessions(
            user_id=user, session_type=SessionType.AGENT
        )  # type: ignore
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0].session_id

    agent = Agent(
        user_id=user,
        # 设置 session_id，以便继续之前的对话
        session_id=session_id,
        model=QWEN_PLUS_2025_07_28,
        db=db,
        # 将历史消息加入上下文
        add_history_to_context=True,
        num_history_runs=3,
        markdown=True,
        debug_level=2 ,
        debug_mode=True,
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


def print_messages(agent):
    """格式化打印当前的聊天历史"""
    console.print(
        Panel(
            JSON(
                json.dumps(
                    [
                        m.model_dump(include={"role", "content"})
                        for m in agent.get_messages_for_session()
                    ]
                ),
                indent=4,
            ),
            title=f"会话历史 (session_id: {agent.session_id})",
            expand=True,
        )
    )


def main(user: str = "user"):
    agent = create_agent(user)

    print("你正在和一个 OpenAI 智能体对话！")
    exit_on = ["退出", "再见", "拜拜"]
    while True:
        message = Prompt.ask(f"[bold] :sunglasses: {user} [/bold]")
        if message in exit_on:
            break

        agent.print_response(input=message, stream=True, markdown=True)
        print_messages(agent)


if __name__ == "__main__":
    typer.run(main)
