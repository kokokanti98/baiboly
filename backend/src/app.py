"""Flask application factory."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel
from flask_cors import CORS

from src.config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
babel = Babel()


def create_app(config_name="default"):
    """
    Create and configure Flask application.

    Args:
        config_name: Configuration name (development, testing, production)

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    # Configure Babel locale selector (inside app context)
    def get_locale():
        """Determine the best matching locale for the user."""
        return "mg"  # Always return Malagasy for now

    app.babel_locale_selector = get_locale

    # Register blueprints
    from src.api.bible import bible_bp
    app.register_blueprint(bible_bp, url_prefix="/api/bible")
    # from src.api.fihirana import fihirana_bp
    # app.register_blueprint(fihirana_bp, url_prefix="/api/fihirana")

    @app.route("/api/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "message": "Baiboly API is running"}

    return app
