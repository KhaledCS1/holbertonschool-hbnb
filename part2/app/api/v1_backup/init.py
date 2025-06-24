"""API v1 package - Export all namespaces"""
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns

__all__ = ['users_ns', 'places_ns', 'reviews_ns', 'amenities_ns']
