"""Flask application factory"""
from flask import Flask
from flask_restx import Api
from config import config

def create_app(config_name='default'):
    """Create and configure the Flask application"""
    # Create Flask instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
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
