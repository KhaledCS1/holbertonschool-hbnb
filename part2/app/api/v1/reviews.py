"""Review API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    def get(self):
        """Get all reviews"""
        return []
