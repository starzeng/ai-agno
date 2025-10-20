from agno.agent import Agent
from agno.tools.local_file_system import LocalFileSystemTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    instructions=[
        "你是一个文件管理助手，帮助将内容保存到本地文件",
        "创建具有适当名称和扩展名的文件",
        "按照指定的目录结构组织文件",
    ],
    tools=[LocalFileSystemTools(target_directory="./tmp")],
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("将此会议摘要保存到文件：“讨论第四季度目标和预算分配”")