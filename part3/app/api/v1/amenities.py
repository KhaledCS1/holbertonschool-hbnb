"""Amenity API endpoints"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

# Define models
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def post(self):
        """Register a new amenity (Admin only)"""
        try:
            # Check if current user is admin
            current_user_claims = get_jwt()
            if not current_user_claims.get('is_admin', False):
                api.abort(403, "Admin privileges required")
            
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities (Public)"""
        amenities = facade.get_all_amenities()
        return [{
            'id': amenity.id,
            'name': amenity.name
        } for amenity in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID (Public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200
    
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""
        try:
            # Check if current user is admin
            current_user_claims = get_jwt()
            if not current_user_claims.get('is_admin', False):
                api.abort(403, "Admin privileges required")
            
            amenity_data = api.payload
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                api.abort(404, "Amenity not found")
            
            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            api.abort(400, str(e))