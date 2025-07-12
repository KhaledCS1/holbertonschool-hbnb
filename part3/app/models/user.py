"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy-mapped User entity with relationships.
"""
from sqlalchemy.orm import relationship, validates

from app import db, bcrypt
from .base_model import BaseModel


class User(BaseModel):
    """User table with authentication helpers and relations."""

    __tablename__ = "users"

    # ── Core fields ──────────────────────────────────────────────────────
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False)

    # ── Relationships ────────────────────────────────────────────────────
    places = relationship(
        "Place",
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    reviews = relationship(
        "Review",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    # ------------------------------------------------------------------
    # Construction / validation
    # ------------------------------------------------------------------
    def __init__(self, **kwargs):
        raw_password = kwargs.pop("password", None)
        super().__init__(**kwargs)
        if raw_password is not None:
            self.hash_password(raw_password)

    @validates("email")
    def _lowercase_email(self, key, address):
        if not address:
            raise ValueError("Email is required")
        return address.lower()

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------
    def hash_password(self, plaintext: str):
        """Hash *plaintext* and store it."""
        self.password = bcrypt.generate_password_hash(plaintext).decode("utf-8")

    def verify_password(self, plaintext: str) -> bool:
        """Return True if *plaintext* matches the stored hash."""
        return bcrypt.check_password_hash(self.password, plaintext)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def add_place(self, place):
        """Append a place to this user's listings (for API parity)."""
        self.places.append(place)
