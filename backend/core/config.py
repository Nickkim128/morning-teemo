import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./morning_news.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # News APIs
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    GUARDIAN_API_KEY: str = os.getenv("GUARDIAN_API_KEY", "")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Application
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # News API URLs
    NEWS_API_BASE_URL: str = "https://newsapi.org/v2"
    GUARDIAN_API_BASE_URL: str = "https://content.guardianapis.com"
    
    # AI Configuration
    OPENAI_MODEL: str = "gpt-4"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    
    # Cache settings
    CACHE_TTL: int = 3600  # 1 hour
    NEWS_REFRESH_INTERVAL: int = 1800  # 30 minutes
    
    class Config:
        env_file = ".env"

settings = Settings() 