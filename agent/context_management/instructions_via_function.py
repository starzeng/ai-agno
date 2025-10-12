from typing import List

from agno.agent import Agent
from agno.run.agent import RunOutput

from models.models import QWEN3_OMNI_FLASH_2025_09_15


def get_instructions(agent: Agent) -> List[str]:
    return [
        f"你的名字是 {agent.name}!",
        "用俳句说话！",
        "用诗歌来回答问题。",
    ]


agent = Agent(
    name="AgentX",
    model=QWEN3_OMNI_FLASH_2025_09_15,
    instructions=get_instructions,
    debug_mode=True,
    debug_level=2,
    markdown=True,
)
run_output: RunOutput = agent.run("你是谁?", stream=False)

print(run_output.content)
