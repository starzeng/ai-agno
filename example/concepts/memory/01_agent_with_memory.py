from uuid import uuid4

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from rich.pretty import pprint

from models.models import QWEN3_235B_A22B

db_url = "postgresql+psycopg://pgvector:pgvector@localhost:5432/pgvector"

db = PostgresDb(db_url=db_url)

db.clear_memories()

session_id = str(uuid4())
user_id = "starryzeng@ai.com"

agent = Agent(
    model=QWEN3_235B_A22B,
    db=db,
    instructions="您可以访问以前与用户交互的记忆,您可以使用这些记忆,全部使用中文,包括记忆.",
    enable_user_memories=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response(
    "我叫starryzeng，我喜欢周末在家和妹子玩。",
    stream=True,
    user_id=user_id,
    session_id=session_id,
)

print()
print("================================")
print()
agent.print_response(
    "我的周末喜欢做什么？",
    stream=True,
    user_id=user_id,
    session_id=session_id,
)

memories_1 = agent.get_user_memories(user_id=user_id)
print("我的记忆:")
pprint(memories_1)
print()
print("================================")
print()
agent.print_response(
    "我还喜欢和妹子一起互动",
    stream=True,
    user_id=user_id,
    session_id=session_id,
)

memories_2 = agent.get_user_memories(user_id=user_id)
print("我的记忆:")
pprint(memories_2)

db.clear_memories()