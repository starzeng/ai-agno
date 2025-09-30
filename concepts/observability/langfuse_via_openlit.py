import base64
import os

from agno.agent import Agent
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from models.models import QWEN3_OMNI_FLASH_2025_09_15

AUTH = f"{os.getenv('LANGFUSE_PUBLIC_KEY')}:{os.getenv('LANGFUSE_SECRET_KEY')}"
LANGFUSE_AUTH = base64.b64encode(AUTH.encode()).decode()

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://cloud.langfuse.com/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(trace_provider)
# 由全球示踪剂提供商创建示踪剂
tracer = trace.get_tracer(__name__)

import openlit

# 初始化开放式仪器。 Disable_batch标志设置为TRUE以立即为过程轨迹。
openlit.init(tracer=tracer, disable_batch=True)

agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)

agent.print_response("最近有什么我国相关话题")
