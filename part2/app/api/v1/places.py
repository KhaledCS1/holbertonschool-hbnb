"""Place API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    def get(self):
        """Get all places"""
        return []
