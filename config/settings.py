"""Configuration management for the Mastodon CV Matcher extension."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # Mastodon Configuration
    mastodon_instance_url: str = Field(..., env="MASTODON_INSTANCE_URL")
    mastodon_access_token: str = Field(..., env="MASTODON_ACCESS_TOKEN")
    
    # AI Configuration
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    
    # Database Configuration
    chroma_persist_directory: str = Field("./data/chroma_db", env="CHROMA_PERSIST_DIRECTORY")
    
    # Application Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    temp_dir: str = Field("./temp", env="TEMP_DIR")
    
    # CV Processing
    supported_file_types: list = [".pdf", ".png", ".jpg", ".jpeg"]
    max_file_size_mb: int = 10
    
    # Matching Configuration
    similarity_threshold: float = 0.7
    max_matches: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure directories exist
Path(settings.temp_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_persist_directory).mkdir(parents=True, exist_ok=True)
