"""
Suhail Al-aboud <10675@holbertonstudents.com>
Flask application factory
"""
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
# SQLAlchemy instance reused across the project
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure the Flask application.

    Args:
        config_class: Python path or class object pointing to the configuration
                       (default: "config.DevelopmentConfig").

    Returns:
        Configured :class:`flask.Flask` application instance.
    """
    # ── 1. Create core Flask app ────────────────────────────────────────────
    app = Flask(__name__)

    # ── 2. Load configuration object ───────────────────────────────────────
    app.config.from_object(config_class)

    # ── 3. Bind extensions ─────────────────────────────────────────────────
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)  # <‑‑ SQLAlchemy ready (tables will be created later)

    # ── 4. Configure RESTX API shell ───────────────────────────────────────
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API with JWT Authentication",
        doc="/api/v1/",
        prefix="/api/v1",
        authorizations={
            "Bearer": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": (
                    "JWT Authorization header using the Bearer scheme. "
                    "Example: \"Bearer {token}\""
                ),
            }
        },
        security="Bearer",
    )

    # ── 5. Register blueprints/namespaces ──────────────────────────────────
    # Import inside function to avoid circular dependencies
    from app.api.v1 import (
        auth_ns,
        users_ns,
        places_ns,
        reviews_ns,
        amenities_ns,
    )

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(reviews_ns, path="/reviews")
    api.add_namespace(amenities_ns, path="/amenities")

    return app
