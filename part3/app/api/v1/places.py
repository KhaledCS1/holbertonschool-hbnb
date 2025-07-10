"""Place API endpoints"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Define models
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def post(self):
        """Create a new place (Authenticated users only)"""
        try:
            current_user_id = get_jwt_identity()
            place_data = api.payload
            
            # Set the owner_id to the authenticated user
            place_data['owner_id'] = current_user_id
            
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id
            }, 201
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Get all places (Public endpoint)"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (Public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id if place.owner else None,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name
            } if place.owner else None,
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities],
            'reviews': [{
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id
            } for review in place.reviews]
        }, 200
    
    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def put(self, place_id):
        """Update a place (Owner or Admin only)"""
        try:
            current_user_id = get_jwt_identity()
            current_user_claims = get_jwt()
            is_admin = current_user_claims.get('is_admin', False)
            
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, "Place not found")
            
            # Check if the current user is the owner OR admin
            if not is_admin and place.owner.id != current_user_id:
                api.abort(403, "Unauthorized action")
            
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)
            
            return {
                'message': 'Place updated successfully',
                'place': {
                    'id': updated_place.id,
                    'title': updated_place.title,
                    'description': updated_place.description,
                    'price': updated_place.price
                }
            }, 200
        except ValueError as e:
            api.abort(400, str(e))