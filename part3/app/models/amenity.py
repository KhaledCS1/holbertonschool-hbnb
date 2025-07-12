"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy-mapped Amenity entity with relationships.
"""
from app import db
from .base_model import BaseModel


class Amenity(BaseModel):
    """Amenities such as Wi-Fi, Pool, etc."""

    __tablename__ = "amenities"

    name = db.Column(db.String(100), nullable=False, unique=True)

    # ── Relationships (many-to-many) ────────────────────────────────────
    places = db.relationship(
        "Place",
        secondary="place_amenity",
        back_populates="amenities",
        lazy="selectin",
    )
