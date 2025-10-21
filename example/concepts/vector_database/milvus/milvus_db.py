import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.milvus import Milvus

from models.models import TEXT_EMBEDDING_V4, QWEN3_MAX

vector_db = Milvus(
    collection="recipes",
    # uri="./tmp/milvus.db",
    embedder=TEXT_EMBEDDING_V4,

)

knowledge = Knowledge(
    name="我的 Milvus 知识库",
    description="这是一个使用 Milvus DB 的知识库",
    vector_db=vector_db,

)

asyncio.run(
    knowledge.add_content_async(
        name="Recipes",
        # url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        # metadata={"doc_type": "recipe_book"},
        text_content="""
        ## 番茄炒蛋食谱

### 所需食材
- 鸡蛋 3-4个
- 番茄 2个（中等大小）
- 葱花 适量
- 盐 适量
- 糖 少许
- 食用油 适量

### 制作步骤

1. **准备工作**
   - 番茄用开水烫一下，去皮切块
   - 鸡蛋打散，加入少许盐调味

2. **炒鸡蛋**
   - 热锅下油，油温稍高
   - 倒入蛋液，快速炒至半熟盛起备用

3. **炒番茄**
   - 锅内留少许油，下葱花爆香
   - 放入番茄块，炒出汁水
   - 加入少许糖和盐调味

4. **合炒**
   - 将炒好的鸡蛋倒回锅中
   - 快速翻炒均匀即可出锅

### 小贴士
- 番茄要选择熟透的，口感更佳
- 炒鸡蛋时火候要快，保持嫩滑
- 可根据个人喜好调整酸甜口味
        """
    )
)

agent = Agent(
    model=QWEN3_MAX,
    knowledge=knowledge,
    debug_mode=True,
    debug_level=2,
)
agent.print_response("如何制作番茄炒蛋", markdown=True)

# vector_db.delete_by_name("Recipes")

# vector_db.delete_by_metadata({"doc_type": "recipe_book"})
