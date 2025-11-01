from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyAgentResponse, AccuracyResult
from agno.tools.calculator import CalculatorTools

from models.models import QWEN3_MAX_PREVIEW

evaluation = AccuracyEval(
    name="计算器评估",
    # model=QWEN3_MAX_PREVIEW,
    evaluator_agent=Agent(
        model=QWEN3_MAX_PREVIEW,
        output_schema=AccuracyAgentResponse,
        use_json_mode=True,
        debug_level=2,
        debug_mode=True,
    ),
    agent=Agent(
        model=QWEN3_MAX_PREVIEW,
        tools=[CalculatorTools()],
        # debug_level=2,
        # debug_mode=True,
    ),
    input="10*5然后平方是多少？请逐步计算",

    expected_output="2500",
    additional_guidelines="Agent输出应包含步骤和最终答案。",
    num_iterations=1,
    debug_mode=True,
    print_summary=False,
    print_results=True,
)

result: Optional[AccuracyResult] = evaluation.run(print_results=True)
assert result is not None and result.avg_score >= 8
