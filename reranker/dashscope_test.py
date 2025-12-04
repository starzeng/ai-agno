from http import HTTPStatus
from os import getenv

import dotenv
from dashscope import TextReRank

dotenv.load_dotenv()

resp = TextReRank.call(
    model="qwen3-rerank",
    api_key=getenv("DASHSCOPE_API_KEY"),
    query="什么是文本排序模型",
    documents=[
        "量子计算是计算科学的一个前沿领域",
        "预训练语言模型的发展给文本排序模型带来了新的进展",
        "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序",
    ],
    top_n=10,
    return_documents=False,
)

if resp.status_code == HTTPStatus.OK:
    for result in resp.output.results:
        print(result)
else:
    print(resp)
