"""
此示例演示如何将 additional_input 与 Agent 一起使用
通过少量示例来教授正确的应答模式。
"""

from agno.agent import Agent
from agno.models.message import Message

from models.models import QWEN3_OMNI_FLASH_2025_09_15

# 少量示例展示良好的客服支持模式
support_examples = [
    # 示例 1：简单问题解决
    Message(role="user", content="我忘记了密码，无法登录"),
    Message(
        role="assistant",
        content="""
    我会立即帮助你重置密码。

    **重置密码步骤：**
    1. 前往登录页面并点击“忘记密码”
    2. 输入你的邮箱地址
    3. 检查邮箱中的重置链接
    4. 点击链接并创建新密码
    5. 使用包含大写字母、小写字母、数字和符号的强密码

    如果 5 分钟内未收到邮件，请检查垃圾邮件文件夹。  
    如需进一步帮助，请告诉我！
    """.strip(),
    ),

    # 示例 2：账单问题模式
    Message(
        role="user",
        content="我为同一个订单被收取了两次费用，我很生气！",
    ),
    Message(
        role="assistant",
        content="""
    对于账单错误和由此造成的不便，我深表歉意。

    **立即处理方案：**
    1. 我将检查你的账户以确认重复扣费
    2. 处理重复交易的全额退款
    3. 检查支付方式设置，防止此类问题再次发生
    4. 退款处理后提供确认编号

    退款通常需要 3–5 个工作日显示在账单中。  
    为表达歉意，我将为你的下次订单提供 10% 折扣。

    请问这个问题还有其他我可以帮忙的地方吗？
    """.strip(),
    ),

    # 示例 3：技术支持模式
    Message(role="user", content="你们的应用在我上传照片时总是崩溃"),
    Message(
        role="assistant",
        content="""
    很抱歉你在上传照片时遇到崩溃问题，我会帮你排查。

    **排查步骤：**
    1. **检查应用版本：** 请确保已更新到最新版本
    2. **重启应用：** 完全关闭并重新打开应用
    3. **检查存储空间：** 确保设备剩余空间至少 1GB
    4. **照片大小：** 尝试上传小于 10MB 的照片
    5. **网络连接：** 确保网络稳定

    **如果问题仍然存在：**
    - 尝试一次只上传一张照片  
    - 在设备设置中清除应用缓存  
    - 重启设备  

    若问题依然未解决，请告知你的设备型号和系统版本，  
    我将把问题升级给技术团队进一步调查。
    """.strip(),
    ),
]

if __name__ == "__main__":
    # 使用少量示例进行学习的 Agent
    agent = Agent(
        name="客户支持专员",
        model=QWEN3_OMNI_FLASH_2025_09_15,
        add_name_to_context=True,
        additional_input=support_examples,  # 少样本学习示例
        instructions=[
            "你是一名专业的客户支持专员。",
            "始终保持同理心、专业性，并以解决问题为导向。",
            "提供清晰且可执行的步骤以解决客户问题。",
            "遵循既定模式，确保回复一致且高质量。",
        ],
        debug_mode=True,
        debug_level=2,
        markdown=True,
    )

    support_examples = [
        # 示例 1：简单问题解决
        Message(role="user", content="我忘记了密码，无法登录"),

        # 示例 2：账单问题模式
        Message(role="user", content="我为同一个订单被收取了两次费用，我很生气！", ),

        # 示例 3：技术支持模式
        Message(role="user", content="你们的应用在我上传照片时总是崩溃"),
    ]

    for i, example in enumerate(support_examples, 1):
        print("=" * 150)
        print("=" * 150)
        print("=" * 150)
        print(f"📞 示例 {i}: {example}")
        agent.print_response(example)
