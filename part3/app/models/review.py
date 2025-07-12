"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy‑mapped Review entity (core only).
"""
from sqlalchemy import CheckConstraint

from app import db
from .base_model import BaseModel


class Review(BaseModel):
    """Guest review for a place (no relations yet)."""

    __tablename__ = "reviews"

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # IDs for future relationships (not FK for now)
    user_id = db.Column(db.String(36), nullable=True)
    place_id = db.Column(db.String(36), nullable=True)

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="chk_rating_range"),
    )
