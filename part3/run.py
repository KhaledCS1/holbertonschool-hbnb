#!/usr/bin/env python3
"""Entry point for the HBnB application"""
import os
from app import create_app

# Get configuration from environment variable
config_name = os.getenv('FLASK_ENV', 'development')

# Map environment names to configuration classes
config_mapping = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig'
}

# Get configuration class
config_class = config_mapping.get(config_name, 'config.DevelopmentConfig')

# Create Flask application with configuration
app = create_app(config_class)

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Run the application
    app.run(host=host, port=port)