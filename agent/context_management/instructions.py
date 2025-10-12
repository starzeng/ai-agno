from agno.agent import Agent

from models.models import QWEN3_OMNI_FLASH_2025_09_15

agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    instructions="分享一个2句话的故事",
    markdown=False,
    debug_mode=True,
    debug_level=2,
)
agent.print_response("12000年后的爱情。")