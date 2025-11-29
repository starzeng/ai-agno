"""
[记忆压缩提示词]
你是一个记忆压缩助手。你的任务是将关于用户的多个记忆
总结成一个全面的摘要，同时保留所有关键事实。

要求：
- 合并所有记忆中的相关信息
- 保留所有事实信息
- 删除冗余信息并整合重复的事实
- 创建关于用户的连贯叙述
- 保持第三人称视角
- 不要添加原始记忆中不存在的信息

只返回总结的记忆文本，不要返回其他内容。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager, SummarizeStrategy
from agno.memory.strategies.types import MemoryOptimizationStrategyType

from models.models import QWEN3_MAX

db_file = "./memory_summarize_strategy.db"
db = SqliteDb(db_file=db_file)

# 创建记忆管理器并优化记忆
memory_manager = MemoryManager(
    model=QWEN3_MAX,
    db=db,
    debug_mode=True,
)

user_id = "user2"

# 创建启用记忆功能的代理
agent = Agent(
    model=QWEN3_MAX,
    db=db,
    memory_manager=memory_manager,
    enable_user_memories=True,
    debug_level=2,
    debug_mode=True,
)



# 为用户创建一些记忆
# print("正在创建记忆...")
# agent.print_response(
#     "我有一只很棒的宠物狗叫Max，它已经3岁了。它是一只金毛寻回犬，非常友好且充满活力。"
#     "我们8周大的时候就把它带回家了。它喜欢在公园里玩接球游戏和长途散步。"
#     "Max很聪明——它知道大约15个不同的指令和技巧。照顾它是我生命中最值得的经历之一。"
#     "它现在基本上是我们家庭的一员了。",
#     user_id=user_id,
# )
# agent.print_response(
#     "我现在住在旧金山，尽管面临各种挑战，但这是一座令人惊叹的城市。我已经在这里住了大约5年。"
#     "我在一家中等规模的软件公司担任产品经理。这里的科技氛围非常棒——"
#     "有很多聪明的人在解决有趣的问题。生活成本确实很高，但机会和社区氛围让这一切都值得。"
#     "我住在米慎区，那里有很棒的食物和充满活力的文化。",
#     user_id=user_id,
# )
# agent.print_response(
#     "周末时，我真的很喜欢在湾区周围徒步旅行。有很多令人惊叹的小径——"
#     "从塔马尔佩斯山到大盆地红杉林。我通常会和一群朋友去徒步，我们每个月都会尝试探索新的小径。"
#     "我也喜欢尝试新餐厅。旧金山有着令人难以置信的美食场景，来自世界各地的美食。"
#     "我总是在寻找隐藏的宝藏和新地方。我最喜欢的食物类型是日本料理、泰国菜和墨西哥菜。",
#     user_id=user_id,
# )
# agent.print_response(
#     "我学钢琴大约一年半了。这是我一直想做但从未有时间做的事情。"
#     "我最终决定投入其中，几乎每天都会练习，通常是30-45分钟。"
#     "我现在正在学习古典作品——我能演奏一些简单的巴赫和莫扎特作品。"
#     "我的目标是最终能够演奏一些爵士钢琴。拥有这样的创造性爱好对我的心理健康很有好处，"
#     "而且很高兴有一些完全不同于日常工作的事情。",
#     user_id=user_id,
# )

# 检查当前记忆
memories_before = agent.get_user_memories(user_id=user_id)
if memories_before:
    print("\n优化前:")
    print(f"  记忆数量: {len(memories_before)}")

    # 优化前统计令牌数
    strategy = SummarizeStrategy()
    tokens_before = strategy.count_tokens(memories_before)
    print(f"  令牌数量: {tokens_before} 个令牌")

    print("\n单个记忆:")
    for i, memory in enumerate(memories_before, 1):
        print(f"  {i}. {memory.memory}")


    print("\n使用'summarize'策略优化记忆...")
    memory_manager.optimize_memories(
        user_id=user_id,
        strategy=MemoryOptimizationStrategyType.SUMMARIZE,  # 将所有记忆合并为一个
        apply=True,  # 应用更改到数据库
    )

    # 检查优化后的记忆
    print("\n优化后:")
    memories_after = agent.get_user_memories(user_id=user_id)
    print(f"  记忆数量: {len(memories_after)}")

    # 优化后统计令牌数
    tokens_after = strategy.count_tokens(memories_after)
    print(f"  令牌数量: {tokens_after} 个令牌")

    # 计算减少量
    if tokens_before > 0:
        reduction_pct = ((tokens_before - tokens_after) / tokens_before) * 100
        tokens_saved = tokens_before - tokens_after
        print(f"  减少量: {reduction_pct:.1f}% ({tokens_saved} 个令牌节省)")

    if memories_after:
        print("\n总结的记忆:")
        print(f"  {memories_after[0].memory}")
    else:
        print("\n 优化后未找到记忆")

agent.print_response("以标签的形式介绍我", user_id=user_id)