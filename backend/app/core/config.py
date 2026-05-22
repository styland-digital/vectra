"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change-me-in-production"
    APP_URL: str = "http://localhost:3000"  # Frontend URL for email links

    # Database
    DATABASE_URL: str = "postgresql+psycopg://vectra:vectra@localhost:5432/vectra"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET: str = "your-jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    # LLM — Claude (Anthropic) is the primary provider
    LLM_PROVIDER: str = "claude"
    ANTHROPIC_API_KEY: str = ""  # Set via environment variable
    CLAUDE_MODEL: str = "claude-haiku-4-5-20251001"  # Fast + cheap for agents
    # Legacy Ollama (kept for optional fallback)
    OLLAMA_BASE_URL: str = ""
    OLLAMA_MODEL: str = "llama2:7b"
    OLLAMA_API_KEY: str = ""
    OLLAMA_CLOUD_HOST: str = "https://ollama.com"
    CLAUDE_API_KEY: str = ""  # Alias, prefer ANTHROPIC_API_KEY

    # External APIs
    ROCKETREACH_API_KEY: str = ""  # Set via environment variable
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = "noreply@vectra.io"
    RESEND_API_KEY: str = ""  # Set via environment variable
    RESEND_FROM_EMAIL: str = "noreply@vectra.io"
    CALENDLY_API_KEY: str = ""  # Set via environment variable
    HUBSPOT_API_KEY: str = ""

    # Stripe Payment Processing
    STRIPE_SECRET_KEY: str = ""  # Set via environment variable
    STRIPE_PUBLISHABLE_KEY: str = ""  # Set via environment variable
    STRIPE_WEBHOOK_SECRET: str = ""  # Set via environment variable
    STRIPE_PRICE_ID_STARTER: str = ""  # Set via environment variable
    STRIPE_PRICE_ID_GROWTH: str = ""  # Set via environment variable
    STRIPE_PRICE_ID_SCALE: str = ""  # Set via environment variable
    FRONTEND_URL: str = "http://localhost:3000"  # For Stripe redirects

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    EMAIL_DAILY_LIMIT: int = 50

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://app.vectra.io",
    ]

    # Monitoring
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    SENTRY_DSN: str = ""

    # Platform Admin
    PLATFORM_ADMIN_EMAIL: str = "admin@vectra.io"  # Configurable via env

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
