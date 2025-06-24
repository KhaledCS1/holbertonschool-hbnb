"""Amenity API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    def get(self):
        """Get all amenities"""
        return []
