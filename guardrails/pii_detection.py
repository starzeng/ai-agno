import asyncio

from agno.agent import Agent
from agno.exceptions import InputCheckError
from agno.guardrails import PIIDetectionGuardrail
from agno.models.openai import OpenAIChat

from models.models import QWEN3_MAX


async def main():
    print("🛡️ PII检测防护演示")
    print("=" * 50)

    agent = Agent(
        name="隐私保护代理",
        model=QWEN3_MAX,
        pre_hooks=[PIIDetectionGuardrail()],
        description="一个在保护隐私的同时帮助客户服务的代理。",
        instructions="你是一个乐于助人的客户服务助理。始终保护用户隐私并适当处理敏感信息。",
    )

    # Test 1: Normal request without PII (should work)
    print("\n✅ 测试1: 不含PII的正常请求")
    print("-" * 30)
    try:
        agent.print_response(
            input="你能帮我理解你们的退货政策吗？",
        )
        print("✅ 正常请求处理成功")
    except InputCheckError as e:
        print(f"❌ 意外错误: {e}")

    # Test 2: Request with SSN (should be blocked)
    print("\n🔴 测试2: 包含社会安全号码的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="你好，我的社会安全号码是123-45-6789。你能帮助我处理账户问题吗？",
        )
        print("⚠️ 这应该被阻止！")
    except InputCheckError as e:
        print(f"✅ PII已阻止: {e.message}")
        print(f"   触发器: {e.check_trigger}")

    # Test 3: Request with credit card (should be blocked)
    print("\n🔴 测试3: 包含信用卡的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="我想更新我的付款方式。我的新卡号是4532 1234 5678 9012。",
        )
        print("⚠️ 这应该被阻止！")
    except InputCheckError as e:
        print(f"✅ PII已阻止: {e.message}")
        print(f"   触发器: {e.check_trigger}")

    # Test 4: Request with email address (should be blocked)
    print("\n🔴 测试4: 包含邮箱地址的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="请将收据发送到john.doe@example.com，这是我的最近购买。",
        )
        print("⚠️ 这应该被阻止！")
    except InputCheckError as e:
        print(f"✅ PII已阻止: {e.message}")
        print(f"   触发器: {e.check_trigger}")

    # Test 5: Request with phone number (should be blocked)
    print("\n🔴 测试5: 包含电话号码的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="我的电话号码是555-123-4567。请打电话告诉我订单状态。",
        )
        print("⚠️ 这应该被阻止！")
    except InputCheckError as e:
        print(f"✅ PII已阻止: {e.message}")
        print(f"   触发器: {e.check_trigger}")

    # Test 6: Mixed PII in context (should be blocked)
    print("\n🔴 测试6: 单个请求中的多种PII类型")
    print("-" * 30)
    try:
        agent.print_response(
            input="你好，我是约翰·史密斯。我的邮箱是john@company.com，电话是555.987.6543。我需要账户帮助。",
        )
        print("⚠️ 这应该被阻止！")
    except InputCheckError as e:
        print(f"✅ PII已阻止: {e.message}")
        print(f"   触发器: {e.check_trigger}")

    # Test 7: Edge case - formatted differently (should still be blocked)
    print("\n🔴 测试7: 不同格式的PII")
    print("-" * 30)
    try:
        agent.print_response(
            input="你能验证我以4532123456789012结尾的信用卡吗？",
        )
        print("⚠️ 这应该被阻止！")
    except InputCheckError as e:
        print(f"✅ PII已阻止: {e.message}")
        print(f"   触发器: {e.check_trigger}")

    print("\n" + "=" * 50)
    print("🎯 PII检测演示完成")
    print("所有敏感信息均已成功阻止！")

    agent = Agent(
        name="隐私保护代理（已屏蔽）",
        model=QWEN3_MAX,
        pre_hooks=[PIIDetectionGuardrail(mask_pii=True)],
        description="一个在保护隐私的同时帮助客户服务的代理。",
        instructions="你是一个乐于助人的客户服务助理。始终保护用户隐私并适当处理敏感信息。",
    )

    print("\n🔴 测试8: 包含社会安全号码的输入")
    print("-" * 30)
    agent.print_response(
        input="你好，我的社会安全号码是123-45-6789。你能帮助我处理账户问题吗？",
    )


if __name__ == "__main__":
    asyncio.run(main())
