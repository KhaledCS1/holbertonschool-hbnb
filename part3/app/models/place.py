"""
Suhail Al-aboud <10675@holbertonstudents.com>
SQLAlchemy‑mapped Place entity (no relationships yet).
"""
from app import db
from .base_model import BaseModel


class Place(BaseModel):
    """Core fields for a rental place / listing."""

    __tablename__ = "places"

    # ── Basic info ───────────────────────────────────────────────────────
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # ── Pricing & location ───────────────────────────────────────────────
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # ── Owner (to be related later) ──────────────────────────────────────
    owner_id = db.Column(db.String(36), nullable=True)  # FK added in later task
