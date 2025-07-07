"""Flask application factory"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt

# Initialize Bcrypt
bcrypt = Bcrypt()

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
    
    # Initialize Bcrypt with app
    bcrypt.init_app(app)
    
    # Initialize Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        prefix='/api/v1'
    )
    
    # Register namespaces
    from app.api.v1 import users_ns, places_ns, reviews_ns, amenities_ns
    
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')
    
    return app