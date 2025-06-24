"""Amenity API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade

# Create namespace
api = Namespace('amenities', description='Amenity operations')

# Define models for API documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})


@api.route('/')
class AmenityList(Resource):
    """Amenity collection operations"""
    
    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created', amenity_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat()
            }, 201
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.doc('list_amenities')
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            } for amenity in amenities
        ], 200


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    """Individual amenity operations"""
    
    @api.doc('get_amenity')
    @api.response(200, 'Amenity details retrieved successfully', amenity_response_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }, 200
    
    @api.doc('update_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                api.abort(404, "Amenity not found")
            
            return {
                'message': 'Amenity updated successfully'
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
