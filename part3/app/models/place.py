"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy-mapped Place entity with relationships.
"""
from app import db
from .base_model import BaseModel

# ────────────────────────────────────────────────────────────────────────
# Association table (many-to-many) between places and amenities
# ────────────────────────────────────────────────────────────────────────
place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id",  db.String(36), db.ForeignKey("places.id"),     primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True),
)


class Place(BaseModel):
    """Core fields for a rental place / listing, linked to owner, reviews, amenities."""

    __tablename__ = "places"

    # ── Basic info ───────────────────────────────────────────────────────
    title       = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text,          nullable=True)

    # ── Pricing & location ───────────────────────────────────────────────
    price     = db.Column(db.Float, nullable=False)
    latitude  = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # ── Ownership ────────────────────────────────────────────────────────
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    owner    = db.relationship("User", back_populates="places", lazy="joined")

    # ── Reviews one-to-many ──────────────────────────────────────────────
    reviews = db.relationship(
        "Review",
        back_populates="place",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    # ── Amenities many-to-many ───────────────────────────────────────────
    amenities = db.relationship(
        "Amenity",
        secondary="place_amenity",
        back_populates="places",
        lazy="selectin",
    )

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def add_review(self, review):
        """Append a review (for API parity)."""
        self.reviews.append(review)
