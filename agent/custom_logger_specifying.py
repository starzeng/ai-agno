import logging

from agno.agent import Agent
from agno.utils.log import configure_agno_logging, log_info

from models.models import QWEN3_OMNI_FLASH_2025_09_15

# 设置自定义记录器
custom_logger = logging.getLogger("custom_logger")
handler = logging.StreamHandler()
formatter = logging.Formatter("[CUSTOM_LOGGER] %(levelname)s: %(message)s")
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
custom_logger.setLevel(logging.DEBUG)  # 将级别设置为 INFO 以显示信息消息
custom_logger.propagate = False

# 配置 Agno 以使用我们的自定义记录器。它将用于所有日志记录。
configure_agno_logging(custom_default_logger=custom_logger)

# 现在，每次使用 agno.utils.log 中的日志记录功能都将使用我们的自定义记录器。
log_info("这是使用我们的自定义记录器！")

# 现在让我们设置一个代理并运行它。
# 来自代理的所有日志记录都将使用我们的自定义记录器。
agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    instructions="中文回答所有问题",
)
agent.print_response("我可以做什么来改善睡眠？")
