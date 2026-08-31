# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    # App Config
    app_name: str = "Technical Documentation Assistant"
    app_version: str = "1.0.0"
    app_environment: str = "development" # development,production
    app_description: str = "just a assistant"

    # LLM Config
    api_key: str
    llm_base_url: str
    llm_model: str
    llm_temperature: float
    llm_max_tokens: int
    llm_max_iterations: int = 3
    

    # RAG Config
    chunk_size: int = 1000
    chunk_overlap: int = 200
    docs_dir: str = "./data/documents"
    chroma_persist_dir: str = "./data/vector_db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
