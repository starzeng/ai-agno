from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.file_generation import FileGenerationTools

from models.models import QWEN3_MAX_PREVIEW

agent = Agent(
    model=QWEN3_MAX_PREVIEW,
    db=SqliteDb(db_file="./tmp/test.db"),
    tools=[FileGenerationTools(output_directory="./tmp")],
    description="您是一位得力助手，可以生成各种格式的文件。",
    instructions=[
        "当被要求创建文件时，请使用适当的文件生成工具。",
        "始终提供有意义的内容和合适的文件名。",
        "解释你创建了什么以及如何使用它。",
    ],
    markdown=True,
    debug_level=2,
    debug_mode=True,
    telemetry=False,
)


def process_file_generation_output(response, example_name: str):
    """处理并显示文件生成输出"""
    print(f"=== {example_name} ===")
    print(response.content)
    if response.files:
        for file in response.files:
            print(f"生成的文件: {file.filename} ({file.size} 字节)")
            if file.url:
                print(f"文件位置: {file.url}")
    print()


if __name__ == "__main__":
    print("文件生成工具示例集")
    print("=" * 50)

    # JSON 文件生成示例
    response = agent.run(
        "创建一个包含3位虚构员工信息的JSON文件，包括姓名、职位、部门和薪资。"
    )
    process_file_generation_output(response, "JSON 文件生成示例")

    # 文本文件生成示例
    response = agent.run(
        "创建一个包含远程工作效率最佳实践列表的文本文件。"
    )
    process_file_generation_output(response, "文本文件生成示例")
