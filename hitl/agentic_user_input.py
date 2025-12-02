from typing import Any, Dict, List

from agno.agent import Agent
from agno.tools import Toolkit
from agno.tools.function import UserInputField
from agno.tools.user_control_flow import UserControlFlowTools
from agno.utils import pprint

from models.models import QWEN3_MAX


class EmailTools(Toolkit):
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="EmailTools", tools=[self.send_email, self.get_emails], *args, **kwargs
        )

    def send_email(self, subject: str, body: str, to_address: str) -> str:
        """向指定地址发送具有给定主题和内容的电子邮件。

        Args:
            subject (str): 邮件的主题。
            body (str): 邮件的内容。
            to_address (str): 要发送邮件的地址。
        """
        return f"已向 {to_address} 发送主题为 {subject} 内容为 {body} 的邮件"

    def get_emails(self, date_from: str, date_to: str) -> list[dict[str, str]]:
        """获取指定日期之间的所有邮件。

        Args:
            date_from (str): 开始日期 (格式 YYYY-MM-DD)。
            date_to (str): 结束日期 (格式 YYYY-MM-DD)。
        """
        return [
            {
                "subject": "你好",
                "body": "你好，世界！",
                "to_address": "test@test.com",
                "date": date_from,
            },
            {
                "subject": "其他随机邮件",
                "body": "这是一封其他随机邮件",
                "to_address": "john@doe.com",
                "date": date_to,
            },
        ]


agent = Agent(
    model=QWEN3_MAX,
    tools=[EmailTools(), UserControlFlowTools()],
    markdown=True,
    debug_level=2,
    debug_mode=True,
    telemetry=False,
)

run_response = agent.run("发送一封内容为'北京天气如何？'的邮件")

while run_response.is_paused:
    for tool in run_response.tools_requiring_user_input:
        input_schema: List[UserInputField] = tool.user_input_schema

        for field in input_schema:
            # 获取模式中每个字段的用户输入
            field_type = field.field_type
            field_description = field.description

            # 向用户显示字段信息
            print(f"\n字段: {field.name}")
            print(f"描述: {field_description}")
            print(f"类型: {field_type}")

            # 获取用户输入
            if field.value is None:
                user_value = input(f"请输入 {field.name} 的值: ")
            else:
                print(f"值: {field.value}")
                user_value = field.value

                # 更新字段值
            field.value = user_value

    run_response = agent.continue_run(run_response=run_response)
    if not run_response.is_paused:
        pprint.pprint_run_response(run_response)
        break

run_response = agent.run("获取我所有的邮件")

while run_response.is_paused:
    for tool in run_response.tools_requiring_user_input:
        input_schema: Dict[str, Any] = tool.user_input_schema

        for field in input_schema:
            # 获取模式中每个字段的用户输入
            field_type = field.field_type
            field_description = field.description

            # 向用户显示字段信息
            print(f"\n字段: {field.name}")
            print(f"描述: {field_description}")
            print(f"类型: {field_type}")

            # 获取用户输入
            if field.value is None:
                user_value = input(f"请输入 {field.name} 的值: ")
            else:
                print(f"值: {field.value}")
                user_value = field.value

                # 更新字段值
            field.value = user_value

    run_response = agent.continue_run(run_response=run_response)
    if not run_response.is_paused:
        pprint.pprint_run_response(run_response)
        break
