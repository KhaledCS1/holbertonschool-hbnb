"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy‑mapped User entity.
"""
from sqlalchemy.orm import validates

from app import db, bcrypt
from .base_model import BaseModel


class User(BaseModel):
    """User table with authentication helpers."""

    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # ------------------------------------------------------------------
    # Construction / validation
    # ------------------------------------------------------------------
    def __init__(self, **kwargs):
        # Pop raw password before super().__init__ to avoid plaintext storage
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
        """Hash *plaintext* and store it in *self.password*."""
        self.password = (
            bcrypt.generate_password_hash(plaintext).decode("utf-8")
        )

    def verify_password(self, plaintext: str) -> bool:
        """Return ``True`` if *plaintext* matches the stored hash."""
        return bcrypt.check_password_hash(self.password, plaintext)
