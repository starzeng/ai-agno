from agno.agent import Agent
from agno.compression.manager import CompressionManager
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools

from models.models import QWEN3_MAX

compression_prompt = """
    你是一位压缩专家。你的目标是为AI技术研究员压缩网络搜索结果。

    你的目标：只提取最新的AI技术进展和研究成果，同时极度简洁。

    必须保留：
    - AI模型名称和具体技术突破（新架构、训练方法、性能提升）
    - 精确数字（准确率、参数量、训练时间、能耗数据）
    - 准确日期（发布日期、论文发表日期、开源日期）
    - 研究人员或机构的直接引述
    - 开源项目和技术文档链接

    必须删除：
    - 公司商业新闻和财务信息
    - 一般科技趋势（除非涉及具体AI技术）
    - 市场分析和预测（只保留技术事实）
    - 复杂的技术细节（只保留核心创新点）
    - 营销宣传语言

    输出格式：
    返回一个项目符号列表，每行遵循以下格式：
    "[技术/模型名称] - [日期]: [技术突破/研究发现] ([关键数据/详情])"

    总字数控制在200词以内。极度简洁。只保留事实。

    示例：
    - Transformer-X - 2024年3月15日: 提出新型注意力机制，在GLUE基准上提升2.3个百分点
    - Llama.cpp - 2024年2月10日: 实现8位量化推理，降低内存占用至原版的1/4
"""

compression_manager = CompressionManager(
    model=QWEN3_MAX,
    compress_tool_results_limit=1,
    compress_tool_call_instructions=compression_prompt,
)

agent = Agent(
    model=QWEN3_MAX,
    tools=[DuckDuckGoTools()],
    description="搜索AI相关信息",
    instructions="使用搜索工具并始终使用最新信息和数据。",
    db=SqliteDb(db_file="./dbs/tool_call_compression_with_manager.db"),
    compression_manager=compression_manager,
    debug_level=2,
    debug_mode=True,
)

agent.print_response(
    """
    使用搜索工具并始终获取最新信息和数据。
    研究这些AI相关的信息（过去一周）：

    图片生成

    对相关AI信息，找出带有日期和数字的具体技术进展。""",
    stream=True,
)
