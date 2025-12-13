from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API keys (optional) — leave empty if you won't call providers directly
    openai_api_key: str | None = None
    google_api_key: str | None = None
    huggingface_api_key: str | None = None

    # Vector store
    chroma_db_path: str = "data/chroma"
    collection_name: str = "genai_suite"

    # Default LLM + embedding models
    default_llm_provider: str = "openai"  # one of: openai|gemini|hf
    default_llm_model: str = "gpt-4o-mini"
    default_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()