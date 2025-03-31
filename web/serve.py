"""
Simple web server for Gambler's Ruin Simulation UI

This module serves the web frontend for the Gambler's Ruin simulation.
"""

import os
import sys
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading index.html: {str(e)}", 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    try:
        return send_from_directory('static', path)
    except Exception as e:
        return jsonify({'error': f"Error serving static file: {str(e)}"}), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5050))
    
    # Print startup information
    print(f"Starting web server on http://localhost:{port}")
    print(f"API server should be running on http://localhost:5000")
    print(f"Templates directory: {os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))}")
    print(f"Static directory: {os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))}")
    print("Make sure both servers are running to use the application.")
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=True) 