from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.baidusearch import BaiduSearchTools
from agno.tracing import setup_tracing

from models.models import QWEN3_MAX

db = SqliteDb(db_file="./traces.db")

setup_tracing(db=db)

agent = Agent(
    name="AI News Agent",
    model=QWEN3_MAX,
    tools=[BaiduSearchTools()],
    instructions="你是一名AI新闻记者。简洁地回答问题。",
    markdown=True,
    db=db,
    debug_mode=True,
    debug_level=2,
    telemetry=False,
)

agent.print_response("AI新闻的趋势是什么？")

traces, count = db.get_traces(agent_id=agent.id, limit=2)
print(f"\n {count} traces for agent '{agent.name}'")
for trace in traces:
    print(f"  - {trace.name}: {trace.duration_ms}ms ({trace.status})")
