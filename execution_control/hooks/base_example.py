from agno.agent import Agent
from agno.exceptions import CheckTrigger, InputCheckError
from agno.run.agent import RunInput

from models.models import QWEN3_MAX


def validate_input_length(
        run_input: RunInput,
) -> None:
    """Pre-hook to validate input length."""
    max_length = 10
    if len(run_input.input_content) > max_length:
        raise InputCheckError(
            f"Input too long. Max {max_length} characters allowed",
            check_trigger=CheckTrigger.INPUT_NOT_ALLOWED,
        )


agent = Agent(
    name="My Agent",
    model=QWEN3_MAX,
    pre_hooks=[validate_input_length],
    debug_mode=True,
    debug_level=2,
    telemetry=False,
)

agent.print_response(
    input="你是一个助手，请回答我的问题。你可以回答任何问题。你好!"
)
