"""Application Configuration Module.

Loads and validates configuration settings from environment variables and `.env` file
using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global application settings and configuration schema.

    Attributes:
        app_name (str): The name of the application.
        app_version (str): The current release version of the application.
        app_environment (str): Operational environment ('development', 'production', etc.).
        app_description (str): Short description of the service for OpenAPI docs.
        api_key (str): API key for the LLM provider (e.g. OpenAI / OpenRouter).
        llm_base_url (str): Base URL endpoint for the LLM API.
        llm_model (str): Name of the language model to invoke.
        llm_temperature (float): Sampling temperature for response generation.
        llm_max_tokens (int): Maximum output tokens per LLM completion.
        llm_max_iterations (int): Maximum agent reasoning iterations before termination.
        chunk_size (int): Character chunk size for splitting markdown documents.
        chunk_overlap (int): Overlap character count between consecutive chunks.
        docs_dir (str): Filepath directory containing raw documentation markdown files.
        chroma_persist_dir (str): Directory path where the Chroma vector store is persisted.
    """

    # App Config
    app_name: str = "Technical Documentation Assistant"
    app_version: str = "1.0.0"
    app_environment: str = "development"  # Options: development, staging, production
    app_description: str = "An intelligent RAG-powered technical documentation assistant."

    # LLM Config
    api_key: str
    llm_base_url: str
    llm_model: str
    llm_temperature: float = 0.0
    llm_max_tokens: int = 2048
    llm_max_iterations: int = 3

    # RAG & Vector Store Config
    chunk_size: int = 1000
    chunk_overlap: int = 200
    docs_dir: str = "./data/documents"
    chroma_persist_dir: str = "./data/vector_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Singleton instance of application settings
settings = Settings()

