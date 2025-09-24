import uvicorn
from fastapi import FastAPI, APIRouter, Depends

from fastapi_auth_test import Auth

app = FastAPI(
    title="三层架构示例API",
    version="1.0.0",
    description="基于FastAPI的三层架构示例",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

api_router = APIRouter(prefix="/api")
verify_router = APIRouter(prefix="/verify", dependencies=[Depends(Auth.verify_token)])


@api_router.get("/")
async def root():
    return "欢迎使用三层架构示例API"


@api_router.get("/health")
async def health_check():
    return "healthy"


@verify_router.get("/protected")
def protected_route():
    return "protected"


app.include_router(api_router)
app.include_router(verify_router)

if __name__ == "__main__":
    uvicorn.run("fastapi_test:app", host="127.0.0.1", port=8000, reload=False)
