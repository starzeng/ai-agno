from typing import List

from agno.agent.agent import Agent
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from pydantic import BaseModel, Field

from models.models import QWEN3_MAX_PREVIEW


class MovieScript(BaseModel):
    setting: str = Field(
        ..., description="Provide a nice setting for a blockbuster movie."
    )
    ending: str = Field(
        ...,
        description="Ending of the movie. If not available, provide a happy ending.",
    )
    genre: str = Field(
        ...,
        description="Genre of the movie. If not available, select action, thriller or romantic comedy.",
    )
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(
        ..., description="3 sentence storyline for the movie. Make it exciting!"
    )


chat_agent = Agent(
    name="Output Schema Agent",
    model=QWEN3_MAX_PREVIEW,
    description="You write movie scripts.",
    instructions="中文回答所有问题",
    markdown=True,
    output_schema=MovieScript,
    use_json_mode=True,
    debug_mode=True,
    debug_level=2,
    telemetry=False,
)

agent_os = AgentOS(
    agents=[chat_agent],
    interfaces=[AGUI(agent=chat_agent)],
)
app = agent_os.get_app()

if __name__ == "__main__":
    """http://localhost:9001/config"""

    agent_os.serve(app="structured_output:app", port=9001, reload=False)
