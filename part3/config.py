"""part3/config.py
Centralized configuration module for the HBnB project.
All environment‑specific settings live in subclasses of ``Config``.
"""
import os
from datetime import timedelta


class Config:
    """Base (shared) configuration."""

    # ── Core Flask ─────────────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG: bool = False
    TESTING: bool = False

    # ── Security / Bcrypt ─────────────────────────────────────────────────
    BCRYPT_LOG_ROUNDS: int = int(os.getenv("BCRYPT_LOG_ROUNDS", 12))

    # ── JWT Settings ──────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "jwt-dev-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM: str = "HS256"

    # ── SQLAlchemy ────────────────────────────────────────────────────────
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False  # SQL debug echo (overridden per‑env)


class DevelopmentConfig(Config):
    """Local development settings."""

    DEBUG = True
    SQLALCHEMY_ECHO = True  # verbose SQL output for debugging
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///development.db",  # lightweight local DB
    )


class TestingConfig(Config):
    """Pytest / CI settings (in‑memory DB & shorter token life)."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(Config):
    """Production / Docker / Cloud settings."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://user:password@localhost/hbnb_prod",  # sensible default
    )
    # Override secrets from env if provided
    SECRET_KEY = os.getenv("SECRET_KEY", Config.SECRET_KEY)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", Config.JWT_SECRET_KEY)


# ── Mapping helper for ``create_app`` factory ─────────────────────────────
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
