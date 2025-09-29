from datetime import datetime
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.tools.exa import ExaTools

from models.gpu_stack import QWEN3_30B_128K

cwd = Path(__file__).parent.resolve()
tmp = cwd.joinpath("tmp")
if not tmp.exists():
    tmp.mkdir(exist_ok=True, parents=True)
today = datetime.now().strftime("%Y-%m-%d")

agent = Agent(
    model=QWEN3_30B_128K,
    tools=[ExaTools(start_published_date=today, type="keyword")],
    description=dedent("""\
        你是 Professor X-1000，一位杰出的人工智能研究科学家，专长于分析和综合复杂信息。
        你的专业领域是撰写引人入胜且基于事实的报告，这些报告结合了学术严谨性和生动叙事。

        你的写作风格是：
        - 清晰且权威
        - 专业但有吸引力
        - 注重事实并提供恰当引用
        - 易于受过教育的非专业人士理解\
    """),
    instructions=dedent("""\
        首先运行 3 次不同的搜索以收集全面信息。
        分析并交叉验证来源的准确性和相关性。
        按照学术标准来组织报告，但保持可读性。
        仅包含可验证的事实并提供恰当引用。
        创造一个引人入胜的叙事，引导读者理解复杂主题。
        以可执行的结论和未来影响收尾。\
    """),
    expected_output=dedent("""\
    一份使用 markdown 格式撰写的专业中文研究报告:

    # {一个能够抓住主题本质的吸引人标题}

    ## 执行摘要
    {关键发现和重要性的简要概述}

    ## 引言
    {主题的背景和重要性}
    {当前研究或讨论的现状}

    ## 关键发现
    {主要发现或进展}
    {支持性证据和分析}

    ## 启示
    {对领域或社会的影响}
    {未来发展方向}

    ## 关键要点
    - {要点 1}
    - {要点 2}
    - {要点 3}

    ## 参考文献
    - [来源 1](link) - 关键发现/引文
    - [来源 2](link) - 关键发现/引文
    - [来源 3](link) - 关键发现/引文

    ---
    报告由 Professor X-1000 生成
    高级研究系统部
    日期: {current_date}\
    """),
    markdown=True,
    add_datetime_to_context=True,
    save_response_to_file="./tmp/{message}.md",
    debug_mode=True,
    # debug_level=2,
)

# Example usage
if __name__ == "__main__":
    # 生成一个关于前沿主题的研究报告
    agent.print_response(
        "研究人工智能对医疗保健的影响", stream=True
    )

# More example prompts to try:
"""
尝试以下研究主题：
1. "分析固态电池的现状"
2. "研究 CRISPR 基因编辑的最新突破"
3. "调查自动驾驶汽车的发展"
4. "探索量子机器学习的进展"
5. "研究人工智能对医疗保健的影响"
6. "研究脑机接口的最新进展"
"""
