from agno.agent import Agent

from models.models import QWEN3_OMNI_FLASH_2025_09_15


def get_instructions(session_state):
    if session_state and session_state.get("current_user_id"):
        return f"把故事讲成关于 {session_state.get('current_user_id')}."
    return "制作关于用户的故事。"


agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    instructions=get_instructions,
    debug_mode=True,
    debug_level=2,
    telemetry=False,
)
agent.print_response("写一个2句话的故事", user_id="StarryZeng")