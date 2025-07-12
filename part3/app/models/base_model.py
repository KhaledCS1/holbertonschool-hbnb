"""
Suhail Al-aboud <10675@holbertonstudents.com>
BaseModel definition mapped to SQLAlchemy.
All other business-logic models should inherit from this class.
"""
from datetime import datetime
import uuid

from app import db


class BaseModel(db.Model):
    """Abstract base that adds *id*, *created_at*, *updated_at* columns."""

    __abstract__ = True  # prevents SQLAlchemy from creating a table for BaseModel

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def update(self, data: dict):
        """Bulk‑update attributes from *data* dict, ignoring unknown keys."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
