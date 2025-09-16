import uvicorn
from agno.agent import Agent
from agno.os import AgentOS
from fastapi import FastAPI

from models.models import QWEN3_MAX_PREVIEW

# Create your custom FastAPI app
app = FastAPI(title="My Custom App")


# Add your custom routes
@app.get("/status")
async def status_check():
    return {"status": "healthy"}


# Pass your app to AgentOS
agent_os = AgentOS(
    agents=[
        Agent(
            id="basic-agent",
            model=QWEN3_MAX_PREVIEW,
        )
    ],
    fastapi_app=app  # Your custom FastAPI app
)

# Get the combined app with both AgentOS and your routes
app = agent_os.get_app()

if __name__ == "__main__":
    uvicorn.run(app="agno_fastapi_test:app", port=8001, reload=False)
