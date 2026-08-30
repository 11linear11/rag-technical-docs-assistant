# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    # App Config
    app_name: str = "Technical Documentation Assistant"
    app_version: str = "1.0.0"
    app_environment: str = "development" # development,production

    # LLM Config
    api_key: str
    model: str

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
