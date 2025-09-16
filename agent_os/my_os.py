from agno.agent import Agent
from agno.os import AgentOS
from fastapi.middleware.cors import CORSMiddleware

from models.models import QWEN3_MAX_PREVIEW

assistant = Agent(
    id="a1",
    name="Assistant",
    model=QWEN3_MAX_PREVIEW,
    instructions=["You are a helpful AI assistant."],
    markdown=True,
)

agent_os = AgentOS(
    os_id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],

)

app = agent_os.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    agent_os.serve(app="my_os:app", port=7777, reload=False)
