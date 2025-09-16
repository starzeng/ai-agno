import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="三层架构示例API",
    description="基于FastAPI的三层架构示例",
    version="1.0.0"
)


@app.get("/")
async def root():
    return "欢迎使用三层架构示例API"


@app.get("/health")
async def health_check():
    return "healthy"


if __name__ == "__main__":
    uvicorn.run("fastapi_test:app", host="127.0.0.1", port=8000, reload=False)
