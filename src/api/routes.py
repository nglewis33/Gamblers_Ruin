"""
API Routes for Gambler's Ruin Simulation

This module defines the API endpoints for the Gambler's Ruin simulation.
"""

from flask import Blueprint, request, jsonify

# Import simulation functions
from src.simulation.basic_simulation import monte_carlo_simulation
from src.simulation.general_simulation import monte_carlo_general
from src.simulation.extended_simulation import (
    run_with_credit,
    run_with_dynamic_betting,
    run_with_max_bet,
    run_full_extension
)

# Import validation functions
from src.api.validation import (
    validate_basic_params,
    validate_general_params,
    validate_extended_params
)

# Create blueprint
api_bp = Blueprint('api', __name__)


@api_bp.route('/basic-simulation', methods=['POST'])
def basic_simulation_endpoint():
    """Endpoint for basic Gambler's Ruin simulation (Problem 1)"""
    # Get request data
    data = request.get_json()
    
    # Validate parameters
    try:
        params = validate_basic_params(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # Run simulation
    try:
        result = monte_carlo_simulation(
            i=params['i'],
            n=params['n'],
            trials=params.get('trials', 10000)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Simulation error: {str(e)}'}), 500


@api_bp.route('/general-simulation', methods=['POST'])
def general_simulation_endpoint():
    """Endpoint for generalized Gambler's Ruin simulation (Problem 2)"""
    # Get request data
    data = request.get_json()
    
    # Validate parameters
    try:
        params = validate_general_params(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # Run simulation
    try:
        result = monte_carlo_general(
            i=params['i'],
            n=params['n'],
            p=params['p'],
            q=params['q'],
            j=params['j'],
            trials=params.get('trials', 10000)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Simulation error: {str(e)}'}), 500


@api_bp.route('/extended-simulation', methods=['POST'])
def extended_simulation_endpoint():
    """Endpoint for extended Gambler's Ruin simulation (Problem 3)"""
    # Get request data
    data = request.get_json()
    
    # Validate parameters
    try:
        params = validate_extended_params(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # Run simulation
    try:
        # Determine which extension to run
        if params.get('use_credit', False) and params.get('use_dynamic_betting', False) and params.get('use_max_bet', False):
            # All extensions
            result = run_full_extension(
                i=params['i'],
                n=params['n'],
                p=params['p'],
                q=params['q'],
                j=params['j'],
                k=params['k'],
                m=params['m'],
                trials=params.get('trials', 10000)
            )
        elif params.get('use_credit', False):
            # Line of credit only
            result = run_with_credit(
                i=params['i'],
                n=params['n'],
                p=params['p'],
                q=params['q'],
                j=params['j'],
                k=params['k'],
                trials=params.get('trials', 10000)
            )
        elif params.get('use_dynamic_betting', False):
            # Dynamic betting only
            result = run_with_dynamic_betting(
                i=params['i'],
                n=params['n'],
                p=params['p'],
                q=params['q'],
                j=params['j'],
                trials=params.get('trials', 10000)
            )
        elif params.get('use_max_bet', False):
            # Maximum bet only
            result = run_with_max_bet(
                i=params['i'],
                n=params['n'],
                p=params['p'],
                q=params['q'],
                j=params['j'],
                m=params['m'],
                trials=params.get('trials', 10000)
            )
        else:
            return jsonify({'error': 'No extensions selected'}), 400
            
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Simulation error: {str(e)}'}), 500


@api_bp.route('/docs', methods=['GET'])
def api_docs():
    """API documentation endpoint"""
    docs = {
        'endpoints': [
            {
                'path': '/api/basic-simulation',
                'method': 'POST',
                'description': 'Basic Gambler\'s Ruin simulation',
                'parameters': {
                    'i': 'Starting amount (dollars)',
                    'n': 'Goal amount (dollars)',
                    'trials': 'Number of simulations to run (default: 10000)'
                },
                'example': {
                    'request': {'i': 10, 'n': 20, 'trials': 5000},
                    'response': {'win_probability': 0.5, 'broke_probability': 0.5}
                }
            },
            {
                'path': '/api/general-simulation',
                'method': 'POST',
                'description': 'Generalized Gambler\'s Ruin simulation',
                'parameters': {
                    'i': 'Starting amount (dollars)',
                    'n': 'Goal amount (dollars)',
                    'p': 'Probability of winning',
                    'q': 'Payout multiplier',
                    'j': 'Bet size',
                    'trials': 'Number of simulations to run (default: 10000)'
                },
                'example': {
                    'request': {'i': 10, 'n': 20, 'p': 0.4, 'q': 1.5, 'j': 2, 'trials': 5000},
                    'response': {'win_probability': 0.3, 'broke_probability': 0.7}
                }
            },
            {
                'path': '/api/extended-simulation',
                'method': 'POST',
                'description': 'Extended Gambler\'s Ruin simulation',
                'parameters': {
                    'i': 'Starting amount (dollars)',
                    'n': 'Goal amount (dollars)',
                    'p': 'Probability of winning',
                    'q': 'Payout multiplier',
                    'j': 'Bet size',
                    'k': 'Credit line amount (required if use_credit=true)',
                    'm': 'Maximum bet (required if use_max_bet=true)',
                    'use_credit': 'Enable line of credit (boolean)',
                    'use_dynamic_betting': 'Enable dynamic betting (boolean)',
                    'use_max_bet': 'Enable maximum bet limit (boolean)',
                    'trials': 'Number of simulations to run (default: 10000)'
                }
            }
        ]
    }
    return jsonify(docs) 