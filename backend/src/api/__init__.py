"""API blueprints package."""
from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import routes
from src.api import bible, fihirana


# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint for monitoring"""
    return {'status': 'healthy', 'message': 'API is running'}, 200
