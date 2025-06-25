from flask import Flask
from flask_restx import Api
from app.api.v1 import users_ns, places_ns, reviews_ns, amenities_ns
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Apply config
    app.config.from_object(config[config_name])

    # Init API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        prefix='/api/v1',
        doc='/api/v1/'  # Swagger UI location
    )

    # Register namespaces
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')

    return app
