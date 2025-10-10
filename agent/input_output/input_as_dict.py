from agno.agent import Agent
from agno.utils.log import debug_level

from models.models import QWEN3_OMNI_FLASH_2025_09_15

Agent(model=QWEN3_OMNI_FLASH_2025_09_15).print_response(
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                },
            },
        ],
    },
    stream=True,
    markdown=True,
    debug_mode=True,
    debug_level=2,
)
