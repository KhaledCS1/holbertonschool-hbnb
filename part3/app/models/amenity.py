"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy‑mapped Amenity entity (core only).
"""
from app import db
from .base_model import BaseModel


class Amenity(BaseModel):
    """Amenities such as Wi‑Fi, Pool, etc. (no relations yet)."""

    __tablename__ = "amenities"

    name = db.Column(db.String(100), nullable=False, unique=True)
