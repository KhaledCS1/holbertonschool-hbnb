"""Expose API v1 namespaces at package level"""

from .users import users_ns
from .places import places_ns
from .reviews import reviews_ns
from .amenities import amenities_ns

__all__ = (
    "users_ns",
    "places_ns",
    "reviews_ns",
    "amenities_ns",
)
