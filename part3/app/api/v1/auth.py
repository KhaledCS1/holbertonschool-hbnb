"""Authentication API endpoints"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade

# Create namespace
api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'is_admin': user.is_admin,
                'email': user.email
            }
        )
        
        # Step 4: Return the JWT token to the client
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.doc(security='Bearer')
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user_id = get_jwt_identity()
        current_user_claims = get_jwt()
        
        return {
            'message': f'Hello, user {current_user_id}',
            'user_id': current_user_id,
            'is_admin': current_user_claims.get('is_admin', False),
            'email': current_user_claims.get('email', '')
        }, 200

@api.route('/create-first-admin')
class CreateFirstAdmin(Resource):
    def post(self):
        """Create first admin user (TEMPORARY - Remove in production)"""
        # Check if any admin exists
        users = facade.get_all_users()
        for user in users:
            if user.is_admin:
                return {'error': 'Admin already exists'}, 400
        
        # Create admin user
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@hbnb.com',
            'password': 'admin123',
            'is_admin': True
        }
        
        admin = facade.create_user(admin_data)
        return {
            'message': 'Admin user created',
            'email': admin.email,
            'password': 'admin123'  # Remove in production!
        }, 201