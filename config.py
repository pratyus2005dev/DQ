import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class PipelineConfig:
    output_dir: str = "out"
    ai_sdk_base_url: str = ""
    ai_sdk_username: str = ""
    ai_sdk_password: str = ""

def get_config() -> PipelineConfig:
    out_dir = os.getenv("DQ_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    return PipelineConfig(
        output_dir=out_dir,
        ai_sdk_base_url=os.getenv("AI_SDK_BASE_URL", ""),
        ai_sdk_username=os.getenv("AI_SDK_USERNAME", ""),
        ai_sdk_password=os.getenv("AI_SDK_PASSWORD", ""),
    )
