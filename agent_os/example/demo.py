from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge.knowledge import Knowledge
from agno.os import AgentOS
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.mcp import MCPTools
from agno.vectordb.pgvector import PgVector

from models.gpu_stack import BGE_M3
from models.models import QWEN_PLUS_2025_07_14

# Database connection
db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"

# Create Postgres-backed memory store
db = PostgresDb(db_url=db_url)

# Create Postgres-backed vector store
vector_db = PgVector(
    db_url=db_url,
    table_name="agno_docs",
    embedder=BGE_M3,
)
knowledge = Knowledge(
    name="Agno Docs",
    contents_db=db,
    vector_db=vector_db,
)

# Create your agents
agno_agent = Agent(
    name="Agno Agent",
    model=QWEN_PLUS_2025_07_14,
    tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
    db=db,
    enable_user_memories=True,
    knowledge=knowledge,
    markdown=True,
)

simple_agent = Agent(
    name="Simple Agent",
    role="Simple agent",
    id="simple_agent",
    model=QWEN_PLUS_2025_07_14,
    instructions=["You are a simple agent"],
    db=db,
    enable_user_memories=True,
)

research_agent = Agent(
    name="Research Agent",
    role="Research agent",
    id="research_agent",
    model=QWEN_PLUS_2025_07_14,
    instructions=["You are a research agent"],
    tools=[DuckDuckGoTools()],
    db=db,
    enable_user_memories=True,
)

# Create a team
research_team = Team(
    name="Research Team",
    description="A team of agents that research the web",
    members=[research_agent, simple_agent],
    model=QWEN_PLUS_2025_07_14,
    id="research_team",
    instructions=[
        "You are the lead researcher of a research team! 🔍",
    ],
    db=db,
    enable_user_memories=True,
    add_datetime_to_context=True,
    markdown=True,
)

# Create the AgentOS
agent_os = AgentOS(
    os_id="agentos-demo",
    agents=[agno_agent],
    teams=[research_team],
)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="demo:app", port=7777)
