import asyncio
from datetime import datetime
from typing import Any


class ExampleAgent:
    """用于并发执行的示例智能体。"""

    def __init__(self, name: str) -> None:
        """使用智能体名称初始化智能体。"""
        self.name = name

    async def reply(self, *args: Any, **kwargs: Any) -> None:
        """回复消息。"""
        start_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{self.name} 开始于 {start_time}")
        await asyncio.sleep(3)  # 模拟长时间运行的任务
        end_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{self.name} 结束于 {end_time}")


async def run_concurrent_agents() -> None:
    """运行并发智能体。"""
    agent1 = ExampleAgent("智能体 1")
    agent2 = ExampleAgent("智能体 2")

    while True:
        await asyncio.sleep(1)
        await asyncio.gather(agent1.reply(), agent2.reply())


try:
    asyncio.run(run_concurrent_agents())
except KeyboardInterrupt:
    print("已退出")
