#!/usr/bin/env python3
"""Entry point for the HBnB application"""
from app import create_app
import os

# Get configuration from environment variable
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask application
app = create_app(config_name)

if __name__ == '__main__':
    # Run the application
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
