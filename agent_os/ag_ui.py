from agno.agent.agent import Agent
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI

from models.models import QWEN3_MAX_PREVIEW

chat_agent = Agent(
    name="Assistant",
    model=QWEN3_MAX_PREVIEW,
    instructions="You are a helpful AI assistant.",
    add_datetime_to_context=True,
    markdown=True,
)

# Setup your AgentOS app
agent_os = AgentOS(
    agents=[chat_agent],
    interfaces=[AGUI(agent=chat_agent)],
)
app = agent_os.get_app()

if __name__ == "__main__":
    """Run your AgentOS.

    You can see the configuration and available apps at:
    http://localhost:9001/config

    """
    agent_os.serve(app="basic:app", reload=True, port=9001)
