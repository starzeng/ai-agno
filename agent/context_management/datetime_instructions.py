from agno.agent import Agent

from models.models import QWEN3_OMNI_FLASH_2025_09_15

agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    add_datetime_to_context=True,
    timezone_identifier="Asia/Shanghai",
    debug_mode=True,
    debug_level=2,
    telemetry=False,
)
agent.print_response(
    "当前日期和时间是几点？现在在武汉几点钟了？"
)