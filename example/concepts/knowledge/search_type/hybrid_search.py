from agno.knowledge.knowledge import Knowledge
from agno.vectordb.milvus import Milvus
from agno.vectordb.pgvector import SearchType

from models.models import TEXT_EMBEDDING_V4

hybrid_db = Milvus(
    collection="search_types",
    search_type=SearchType.hybrid,
    embedder=TEXT_EMBEDDING_V4,
)
knowledge = Knowledge(
    name="Hybrid Search Knowledge Base",
    vector_db=hybrid_db,
)

# knowledge.add_contents(
#     text_contents=[
#         "今天天气真好，适合出去散步",
#         "人工智能正在改变我们的生活方式",
#         "我喜欢在周末阅读书籍",
#         "这个项目的进度比预期快了很多",
#         "昨晚的电影非常精彩，值得一看",
#         "健康饮食对身体非常重要",
#         "学习新技能总是充满挑战和乐趣",
#         "城市交通拥堵问题日益严重",
#         "音乐能够治愈人的心灵",
#         "环境保护是每个人的责任",
#         "科学技术的发展日新月异",
#         "旅行可以开阔视野增长见识",
#         "良好的沟通技巧在工作中很重要",
#         "数字化转型成为企业发展关键",
#         "运动有助于提高身体素质",
#         "传统文化需要传承和发扬",
#         "在线教育为学习提供更多便利",
#         "创新思维推动社会进步发展",
#         "团队合作能够提升工作效率",
#         "终身学习是适应时代变化的必要条件"
#     ]
# )

results = hybrid_db.search("团队合作能够提升工作效率", limit=10)
filtered_docs = [{k: v for k, v in doc.to_dict().items() if k != 'embedding'}
                 for doc in results]
for filtered_doc in filtered_docs:
    print(filtered_doc)
