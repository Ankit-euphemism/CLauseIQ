from pydantic import Field
from pydantic_settings import BaseSettings
# Settings for the application, including OpenRouter API key, model name, chunk size, overlap, and top-k retrieval settings.
class Settings(BaseSettings):
    openrouter_api_key: str = Field(default="", validation_alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = Field(default="openrouter/auto", validation_alias="OPENROUTER_MODEL")
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5

    class Config:
        env_file = ".env"

settings = Settings()