from agno.agent import Agent
from agno.tools.calculator import CalculatorTools

from models.models import QWEN3_235B_A22B

agent = Agent(
    model=QWEN3_235B_A22B,
    tools=[
        CalculatorTools()
    ],
    markdown=True,
    debug_level=2,
    debug_mode=True,
)
agent.print_response("10*5的2次方是多少，一步步做")
