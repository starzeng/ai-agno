import asyncio
import json
from textwrap import dedent
from typing import Dict, Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.workflow.workflow import Workflow
from pydantic import BaseModel, Field


# --- Response Models ---
class NewsArticle(BaseModel):
    title: str = Field(..., description="文章标题。")
    url: str = Field(..., description="文章链接。")
    summary: Optional[str] = Field(
        ..., description="文章摘要（如果有）。"
    )


class SearchResults(BaseModel):
    articles: list[NewsArticle]


class ScrapedArticle(BaseModel):
    title: str = Field(..., description="文章标题。")
    url: str = Field(..., description="文章链接。")
    summary: Optional[str] = Field(
        ..., description="文章摘要（如果有）。"
    )
    content: Optional[str] = Field(
        ...,
        description="文章完整内容（Markdown 格式）。如果内容不可用则为 None。",
    )


# --- Agents ---
research_agent = Agent(
    name="博客调研Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[GoogleSearchTools()],
    description=dedent("""\
    你是 BlogResearch-X，一名专业的调研助理，擅长为优质博客内容发现来源。你的专长包括：

    - 找到权威和趋势来源
    - 评估内容的可信性和相关性
    - 识别多样观点和专家意见
    - 发现独特的切入点和洞见
    - 确保主题覆盖全面
    """),
    instructions=dedent("""\
    1. 搜索策略 🔍
       - 查找 10-15 个相关来源并筛选出 5-7 个最佳来源
       - 优先最近且权威的内容
       - 寻找独特的角度和专家洞见
    2. 来源评估 📊
       - 验证来源的可信度与专业性
       - 检查发布时间以保证时效性
       - 评估内容深度与独特性
    3. 观点多样性 🌐
       - 包括不同的观点
       - 汇集主流与专家意见
       - 寻找支持性数据与统计
    """),
    output_schema=SearchResults,
)

content_scraper_agent = Agent(
    name="内容抓取Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    tools=[Newspaper4kTools()],
    description=dedent("""\
    你是 ContentBot-X，专注于提取与处理数字内容以供博客写作。你的专长包括：

    - 高效的内容提取
    - 智能格式化与结构化
    - 识别关键信息
    - 保留引用与统计数据
    - 保持来源归属
    """),
    instructions=dedent("""\
    1. 内容提取 📑
       - 从文章中提取内容
       - 保留重要引用与统计数据
       - 保持正确的归属信息
       - 优雅处理付费墙
    2. 内容处理 🔄
       - 将文本格式化为干净的 Markdown
       - 保留关键信息
       - 合理组织结构
    3. 质量控制 ✅
       - 验证内容的相关性
       - 确保提取准确
       - 保持可读性
    """),
    output_schema=ScrapedArticle,
)

blog_writer_agent = Agent(
    name="博客撰写Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    description=dedent("""\
    你是 BlogMaster-X，一名将新闻写作与数字营销结合的高级内容创作者。你的优势包括：

    - 打造病毒级标题
    - 写出吸引人的开头
    - 为数字阅读结构化内容
    - 无缝整合调研内容
    - 在保证质量的同时优化 SEO
    - 提供可分享的结论
    """),
    instructions=dedent("""\
    1. 内容策略 📝
       - 打造吸引注意力的标题
       - 写出引人入胜的引言
       - 结构化以提升参与度
       - 包含相关小标题
    2. 写作精炼 ✍️
       - 在专业性与易读性之间取得平衡
       - 使用清晰、吸引人的语言
       - 提供相关示例
       - 自然地融入统计数据
    3. 来源整合 🔍
       - 正确引用来源
       - 包含专家引用
       - 保持事实准确
    4. 数字优化 💻
       - 便于浏览的结构
       - 包含可分享的要点
       - 优化 SEO
       - 添加吸引人的小标题

    请按以下结构输出博客文章：
    # {病毒级标题}

    ## 引言
    {引人入胜的钩子和背景}

    ## {引人注目的部分 1}
    {关键见解与分析}
    {专家引用与统计数据}

    ## {引人入胜的部分 2}
    {更深入的探讨}
    {现实世界案例}

    ## {实用部分 3}
    {可操作的见解}
    {专家建议}

    ## 关键要点
    - {可分享的见解 1}
    - {实用要点 2}
    - {重要发现 3}

    ## 来源
    {带链接的正确归属来源}
    """),
    markdown=True,
)


# --- Helper Functions ---
def get_cached_blog_post(session_state, topic: str) -> Optional[str]:
    """从 workflow 会话状态中获取已缓存的博客文章"""
    logger.info("检查是否存在已缓存的博客文章")
    return session_state.get("blog_posts", {}).get(topic)


def cache_blog_post(session_state, topic: str, blog_post: str):
    """将博客文章缓存到 workflow 会话状态"""
    logger.info(f"保存博客文章，主题: {topic}")
    if "blog_posts" not in session_state:
        session_state["blog_posts"] = {}
    session_state["blog_posts"][topic] = blog_post


def get_cached_search_results(session_state, topic: str) -> Optional[SearchResults]:
    """从 workflow 会话状态中获取已缓存的搜索结果"""
    logger.info("检查是否存在已缓存的搜索结果")
    search_results = session_state.get("search_results", {}).get(topic)
    if search_results and isinstance(search_results, dict):
        try:
            return SearchResults.model_validate(search_results)
        except Exception as e:
            logger.warning(f"无法验证已缓存的搜索结果: {e}")
    return search_results if isinstance(search_results, SearchResults) else None


def cache_search_results(session_state, topic: str, search_results: SearchResults):
    """将搜索结果缓存到 workflow 会话状态"""
    logger.info(f"保存搜索结果，主题: {topic}")
    if "search_results" not in session_state:
        session_state["search_results"] = {}
    session_state["search_results"][topic] = search_results.model_dump()


def get_cached_scraped_articles(
        session_state, topic: str
) -> Optional[Dict[str, ScrapedArticle]]:
    """从 workflow 会话状态中获取已缓存的抓取文章"""
    logger.info("检查是否存在已缓存的抓取文章")
    scraped_articles = session_state.get("scraped_articles", {}).get(topic)
    if scraped_articles and isinstance(scraped_articles, dict):
        try:
            return {
                url: ScrapedArticle.model_validate(article)
                for url, article in scraped_articles.items()
            }
        except Exception as e:
            logger.warning(f"无法验证已缓存的抓取文章: {e}")
    return scraped_articles if isinstance(scraped_articles, dict) else None


def cache_scraped_articles(
        session_state, topic: str, scraped_articles: Dict[str, ScrapedArticle]
):
    """将抓取的文章缓存到 workflow 会话状态"""
    logger.info(f"保存抓取文章，主题: {topic}")
    if "scraped_articles" not in session_state:
        session_state["scraped_articles"] = {}
    session_state["scraped_articles"][topic] = {
        url: article.model_dump() for url, article in scraped_articles.items()
    }


async def get_search_results(
        session_state, topic: str, use_cache: bool = True, num_attempts: int = 3
) -> Optional[SearchResults]:
    """带缓存支持的搜索结果获取函数"""

    # 优先检查缓存
    if use_cache:
        cached_results = get_cached_search_results(session_state, topic)
        if cached_results:
            logger.info(f"在缓存中找到 {len(cached_results.articles)} 篇文章。")
            return cached_results

    # 搜索新结果
    for attempt in range(num_attempts):
        try:
            print(
                f"🔍 正在搜索有关主题的文章: {topic}（尝试 {attempt + 1}/{num_attempts}）"
            )
            response = await research_agent.arun(topic)

            if (
                    response
                    and response.content
                    and isinstance(response.content, SearchResults)
            ):
                article_count = len(response.content.articles)
                logger.info(f"在第 {attempt + 1} 次尝试中找到 {article_count} 篇文章")
                print(f"✅ 找到 {article_count} 篇相关文章")

                # 缓存结果
                cache_search_results(session_state, topic, response.content)
                return response.content
            else:
                logger.warning(
                    f"尝试 {attempt + 1}/{num_attempts} 失败: 返回类型无效"
                )

        except Exception as e:
            logger.warning(f"尝试 {attempt + 1}/{num_attempts} 失败: {str(e)}")

    logger.error(f"在 {num_attempts} 次尝试后未能获取搜索结果")
    return None


async def scrape_articles(
        session_state,
        topic: str,
        search_results: SearchResults,
        use_cache: bool = True,
) -> Dict[str, ScrapedArticle]:
    """带缓存支持的文章抓取函数"""

    # 优先检查缓存
    if use_cache:
        cached_articles = get_cached_scraped_articles(session_state, topic)
        if cached_articles:
            logger.info(f"在缓存中找到 {len(cached_articles)} 篇抓取文章。")
            return cached_articles

    scraped_articles: Dict[str, ScrapedArticle] = {}

    print(f"📄 正在抓取 {len(search_results.articles)} 篇文章...")

    for i, article in enumerate(search_results.articles, 1):
        try:
            print(
                f"📖 正在抓取第 {i}/{len(search_results.articles)} 篇文章: {article.title[:50]}..."
            )
            response = await content_scraper_agent.arun(article.url)

            if (
                    response
                    and response.content
                    and isinstance(response.content, ScrapedArticle)
            ):
                scraped_articles[response.content.url] = response.content
                logger.info(f"已抓取文章: {response.content.url}")
                print(f"✅ 成功抓取: {response.content.title[:50]}...")
            else:
                print(f"❌ 抓取失败: {article.title[:50]}...")

        except Exception as e:
            logger.warning(f"抓取 {article.url} 失败: {str(e)}")
            print(f"❌ 抓取出错: {article.title[:50]}...")

    # 缓存抓取到的文章
    cache_scraped_articles(session_state, topic, scraped_articles)
    return scraped_articles


# --- Main Execution Function ---
async def blog_generation_execution(
        session_state,
        topic: str = None,
        use_search_cache: bool = True,
        use_scrape_cache: bool = True,
        use_blog_cache: bool = True,
) -> str:
    """
    博客文章生成工作流执行函数。

    参数:
        session_state: 共享会话状态
        topic: 博客主题（若未提供，则使用 execution_input.input）
        use_search_cache: 是否使用已缓存的搜索结果
        use_scrape_cache: 是否使用已缓存的抓取文章
        use_blog_cache: 是否使用已缓存的博客文章
    """

    blog_topic = topic

    if not blog_topic:
        return "❌ 未提供博客主题。请指定一个主题。"

    print(f"🎨 正在为主题生成博客文章: {blog_topic}")
    print("=" * 60)

    # 优先检查已缓存的博客文章
    if use_blog_cache:
        cached_blog = get_cached_blog_post(session_state, blog_topic)
        if cached_blog:
            print("📋 找到已缓存的博客文章！")
            return cached_blog

    # 阶段 1: 调研并收集来源
    print("\n🔍 第 1 阶段：调研与来源收集")
    print("=" * 50)

    search_results = await get_search_results(
        session_state, blog_topic, use_search_cache
    )

    if not search_results or len(search_results.articles) == 0:
        return f"❌ 抱歉，未能找到与主题相关的文章: {blog_topic}"

    print(f"📊 找到了 {len(search_results.articles)} 个相关来源：")
    for i, article in enumerate(search_results.articles, 1):
        print(f"   {i}. {article.title[:60]}...")

    # 阶段 2: 内容提取
    print("\n📄 第 2 阶段：内容提取")
    print("=" * 50)

    scraped_articles = await scrape_articles(
        session_state, blog_topic, search_results, use_scrape_cache
    )

    if not scraped_articles:
        return f"❌ 未能从任何文章中提取到内容，主题: {blog_topic}"

    print(f"📖 成功从 {len(scraped_articles)} 篇文章提取内容")

    # 阶段 3: 博客撰写
    print("\n✍️ 第 3 阶段：博客撰写")
    print("=" * 50)

    # 为撰写器准备输入
    writer_input = {
        "topic": blog_topic,
        "articles": [article.model_dump() for article in scraped_articles.values()],
    }

    print("🤖 AI 正在为你撰写博客文章...")
    writer_response = await blog_writer_agent.arun(json.dumps(writer_input, indent=2))

    if not writer_response or not writer_response.content:
        return f"❌ 无法为主题生成博客文章: {blog_topic}"

    blog_post = writer_response.content

    # 缓存博客文章
    cache_blog_post(session_state, blog_topic, blog_post)

    print("✅ 博客文章生成成功！")
    print(f"📝 长度: {len(blog_post)} 字符")
    print(f"📚 来源数量: {len(scraped_articles)} 篇文章")

    return blog_post


# --- Workflow Definition ---
blog_generator_workflow = Workflow(
    name="博客文章生成器",
    description="具有调研与内容创作能力的高级博客生成器",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/blog_generator.db",
    ),
    steps=blog_generation_execution,
    session_state={},  # 初始化空的会话状态以用于缓存
)

if __name__ == "__main__":
    import random


    async def main():
        # 用来展示生成器多样性的示例主题
        example_topics = [
            "通用人工智能的崛起：最新突破",
            "量子计算如何革新网络安全",
            "2024 年的可持续生活：降低碳足迹的实用技巧",
            "工作的未来：人工智能与人类协作",
            "太空旅游：从科幻到现实",
            "数字时代的正念与心理健康",
            "电动汽车的演进：现状与未来趋势",
            "为什么猫悄然统治了互联网",
            "为什么比萨在凌晨两点吃起来更美味的科学",
            "橡胶鸭如何革新软件开发",
        ]

        # 随机测试一个主题
        topic = random.choice(example_topics)

        print("🧪 测试 博客生成器 v2.0")
        print("=" * 60)
        print(f"📝 主题: {topic}")
        print()

        # 生成博客文章
        resp = await blog_generator_workflow.arun(
            topic=topic,
            use_search_cache=True,
            use_scrape_cache=True,
            use_blog_cache=True,
        )

        pprint_run_response(resp, markdown=True, show_time=True)


    asyncio.run(main())

# TODO 未测试
