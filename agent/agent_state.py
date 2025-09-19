from agno.agent import Agent

from models.models import QWEN_PLUS_2025_07_28


def increment_counter(session_state) -> str:
    """在会话状态中递增计数器。"""
    # 如果计数器不存在则初始化
    if "count" not in session_state:
        session_state["count"] = 0

    # 递增计数器
    session_state["count"] += 1

    return f"计数器已递增！当前计数为: {session_state['count']}"


def get_counter(session_state) -> str:
    """获取当前计数器值。"""
    count = session_state.get("count", 0)
    return f"当前计数为: {count}"


# 创建一个维护状态的智能体
agent = Agent(
    model=QWEN_PLUS_2025_07_28,
    # 用初始值 0 初始化会话状态中的计数器
    session_state={"count": 0},
    add_session_state_to_context=True,
    tools=[increment_counter, get_counter],
    # 在指令中使用会话状态中的变量
    instructions="你可以递增和查看计数器。当前计数为: {count}",
    # 重要：在消息中解析状态，让智能体能看到状态变化
    resolve_in_context=True,
    markdown=True,
    debug_mode=True,
    debug_level=2
)

# 测试计数器功能
print("正在测试计数器功能...")
agent.print_response(
    "让我们递增计数器 3 次并观察状态变化！", stream=True
)
