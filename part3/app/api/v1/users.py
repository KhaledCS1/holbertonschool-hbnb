"""User API endpoints"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

# Create namespace
api = Namespace('users', description='User operations')

# Create facade instance
facade = HBnBFacade()

# Define models for API documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user', min_length=6)
})

admin_user_model = api.model('AdminUser', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user', min_length=6),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='New password', min_length=6)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user (Public - for self-registration)"""
        try:
            user_data = api.payload
            # Regular users cannot set is_admin
            user_data['is_admin'] = False
            
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users (Public)"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200

@api.route('/admin')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(admin_user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def post(self):
        """Create a new user (Admin only - can set admin status)"""
        try:
            # Check if current user is admin
            current_user_claims = get_jwt()
            if not current_user_claims.get('is_admin', False):
                api.abort(403, "Admin privileges required")
            
            user_data = api.payload
            new_user = facade.create_user(user_data)
            
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin,
                'message': 'User successfully created by admin'
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (Public)"""
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
    
    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.doc(security='Bearer')
    def put(self, user_id):
        """Update user information"""
        try:
            current_user_id = get_jwt_identity()
            current_user_claims = get_jwt()
            is_admin = current_user_claims.get('is_admin', False)
            
            # Regular users can only modify their own data (excluding email/password)
            if not is_admin and user_id != current_user_id:
                api.abort(403, "Unauthorized action")
            
            user_data = api.payload
            
            # Regular users cannot modify email or password
            if not is_admin:
                if 'email' in user_data:
                    api.abort(400, "You cannot modify email or password")
                if 'password' in user_data:
                    api.abort(400, "You cannot modify email or password")
            
            # Admins can modify everything
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                api.abort(404, "User not found")
            
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'message': 'User updated successfully'
            }, 200
        except ValueError as e:
            api.abort(400, str(e))