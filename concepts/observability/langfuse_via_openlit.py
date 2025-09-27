import base64
import os

import dotenv
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN3_OMNI_FLASH_2025_09_15

dotenv.load_dotenv()

LANGFUSE_AUTH = base64.b64encode(
    f"{os.getenv('LANGFUSE_PUBLIC_KEY')}:{os.getenv('LANGFUSE_SECRET_KEY')}".encode()
).decode()

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ("https://cloud.langfuse.com/api/public/otel")
# os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"]="http://localhost:3000/api/public/otel"

os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (  # noqa: E402
    OTLPSpanExporter,
)
from opentelemetry.sdk.trace import TracerProvider  # noqa: E402
from opentelemetry.sdk.trace.export import SimpleSpanProcessor  # noqa: E402

trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

# Sets the global default tracer provider
from opentelemetry import trace  # noqa: E402

trace.set_tracer_provider(trace_provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)

import openlit  # noqa: E402

# Initialize OpenLIT instrumentation. The disable_batch flag is set to true to process traces immediately.
openlit.init(tracer=tracer, disable_batch=True)

agent = Agent(
    model=QWEN3_OMNI_FLASH_2025_09_15,
    tools=[DuckDuckGoTools()],
    markdown=True,
    debug_mode=True,
)

agent.print_response("阿里云栖大会讲了写什么？简要回答.")
