from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.run import RunContext

from models.models import QWEN3_MAX


def add_item(run_context: RunContext, item: str) -> str:
    """向购物清单中添加一项物品。"""
    run_context.session_state["shopping_list"].append(item)
    return f"已添加 {item}"

def get_item(run_context: RunContext) -> str:
    """查询购物车中的东西。"""
    return run_context.session_state["shopping_list"]

agent = Agent(
    model=QWEN3_MAX,
    db=SqliteDb(db_file="../state.db"),
    session_state={"shopping_list": []},  # 默认状态
    tools=[add_item, get_item],
    instructions="购物清单: {shopping_list}",  # 指令中的状态
)

agent.print_response("将牛奶和面包还有鸡蛋添加都购物车")
agent.print_response("购物车中有什么")
