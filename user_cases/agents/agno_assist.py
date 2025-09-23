from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from models.gpu_stack import QWEN3_30B_128K, BGE_M3

knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="agno_assist_knowledge",
        uri="./tmp/lancedb",
        # search_type=SearchType.hybrid,
        embedder=BGE_M3,
    ),
)

knowledge.add_content(name="Agno 文档", url="https://docs.agno.com/llms-full.txt")
print(QWEN3_30B_128K.get_request_params())
agno_assist = Agent(
    name="Agno 助手",
    model=QWEN3_30B_128K,
    description="你帮助回答有关 Agno 框架的问题。",
    instructions="在回答问题之前先搜索你的知识库。翻译成中文回答",
    knowledge=knowledge,
    db=SqliteDb(session_table="agno_assist_sessions", db_file="tmp/agents.db"),
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
    stream=True,
    # debug_mode=True,
    telemetry=False,
)

if __name__ == "__main__":
    agno_assist.print_response("什么是 Agno？")
