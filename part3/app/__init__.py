"""Flask application factory"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application
    
    Args:
        config_class: Configuration class path (default: config.DevelopmentConfig)
        
    Returns:
        Flask application instance
    """
    # Create Flask instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize Flask-RESTX with authorization support
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API with JWT Authentication',
        doc='/api/v1/',
        prefix='/api/v1',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
            }
        },
        security='Bearer'
    )
    
    # Register namespaces
    from app.api.v1 import auth_ns, users_ns, places_ns, reviews_ns, amenities_ns
    
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    
    return app