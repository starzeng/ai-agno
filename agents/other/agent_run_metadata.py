from datetime import datetime

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN3_MAX

agent = Agent(
    model=QWEN3_MAX,
    tools=[DuckDuckGoTools()],
    instructions="您是客户支持agent。您能高效地帮助处理客户咨询。",
    markdown=True,
    debug_mode=True,
    debug_level=2,
    telemetry=False,
)

response = agent.run(
    "一位客户报告说他们的高级订阅功能无法使用。他们急需帮助，因为他们在2小时内有一个演示。",
    metadata={
        "ticket_id": "SUP-2024-001234",
        "priority": "高",
        "request_type": "客户支持",
        "sla_deadline": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "escalation_level": 2,
        "customer_tier": "企业",
        "department": "customer_success",
        "agent_id": "support_agent_v1",
        "business_impact": "revenue_critical",
        "estimated_resolution_time_minutes": 30,
    },
    debug_mode=True,
    debug_level=2,
)
