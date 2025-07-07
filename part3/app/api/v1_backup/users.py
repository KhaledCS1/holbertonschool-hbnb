"""User API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace
api = Namespace('users', description='User operations')

# Create facade instance
facade = HBnBFacade()

# Create facade instance
facade = HBnBFacade()

# Define models for API documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})


@api.route('/')
class UserList(Resource):
    """User collection operations"""
    
    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', user_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        
        try:
            # Create new user
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'created_at': new_user.created_at.isoformat(),
                'updated_at': new_user.updated_at.isoformat()
            }, 201
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.doc('list_users')
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users
        ], 200


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """Individual user operations"""
    
    @api.doc('get_user')
    @api.response(200, 'User details retrieved successfully', user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }, 200
    
    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully', user_response_model)
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user's information"""
        user_data = api.payload
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                api.abort(404, "User not found")
            
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'created_at': updated_user.created_at.isoformat(),
                'updated_at': updated_user.updated_at.isoformat()
            }, 200
        except ValueError as e:
            api.abort(400, str(e))

users_ns = api

