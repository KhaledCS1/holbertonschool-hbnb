"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy-mapped Review entity with relationships.
"""
from sqlalchemy import CheckConstraint

from app import db
from .base_model import BaseModel


class Review(BaseModel):
    """Guest review for a place (links to user & place)."""

    __tablename__ = "reviews"

    text   = db.Column(db.Text,    nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # ── Foreign keys ────────────────────────────────────────────────────
    user_id  = db.Column(db.String(36), db.ForeignKey("users.id"),  nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    # ── Relationships ───────────────────────────────────────────────────
    user  = db.relationship("User",  back_populates="reviews", lazy="joined")
    place = db.relationship("Place", back_populates="reviews", lazy="joined")

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="chk_rating_range"),
    )
