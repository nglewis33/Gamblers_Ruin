"""
Gambler's Ruin API Application

This module sets up the Flask application for the Gambler's Ruin API.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import routes
from src.api.routes import api_bp

# Create Flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True) 