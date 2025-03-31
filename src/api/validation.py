"""
Parameter Validation for Gambler's Ruin API

This module provides functions for validating API request parameters.
"""

from typing import Dict, Any


def validate_basic_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for basic simulation.
    
    Args:
        data: Request data containing simulation parameters
        
    Returns:
        Dict with validated parameters
        
    Raises:
        ValueError: If any parameters are invalid
    """
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")
    
    # Check required parameters
    if 'i' not in data:
        raise ValueError("Missing required parameter: i (starting amount)")
    
    if 'n' not in data:
        raise ValueError("Missing required parameter: n (goal amount)")
    
    # Convert to appropriate types
    try:
        i = int(data['i'])
        n = int(data['n'])
        trials = int(data.get('trials', 10000))
    except (ValueError, TypeError):
        raise ValueError("Parameters i, n, and trials must be integers")
    
    # Validate parameter ranges
    if i <= 0:
        raise ValueError("Starting amount (i) must be greater than 0")
    
    if n <= i:
        raise ValueError("Goal amount (n) must be greater than starting amount (i)")
    
    if trials <= 0:
        raise ValueError("Number of trials must be greater than 0")
    
    if trials > 1000000:
        raise ValueError("Number of trials cannot exceed 1,000,000")
    
    # Return validated parameters
    return {
        'i': i,
        'n': n,
        'trials': trials
    }


def validate_general_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for generalized simulation.
    
    Args:
        data: Request data containing simulation parameters
        
    Returns:
        Dict with validated parameters
        
    Raises:
        ValueError: If any parameters are invalid
    """
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")
    
    # Check required parameters
    required_params = ['i', 'n', 'p', 'q', 'j']
    for param in required_params:
        if param not in data:
            raise ValueError(f"Missing required parameter: {param}")
    
    # Convert to appropriate types
    try:
        i = int(data['i'])
        n = int(data['n'])
        p = float(data['p'])
        q = float(data['q'])
        j = int(data['j'])
        trials = int(data.get('trials', 10000))
    except (ValueError, TypeError):
        raise ValueError("Invalid parameter types")
    
    # Validate parameter ranges
    if i <= 0:
        raise ValueError("Starting amount (i) must be greater than 0")
    
    if n <= i:
        raise ValueError("Goal amount (n) must be greater than starting amount (i)")
    
    if p <= 0 or p >= 1:
        raise ValueError("Win probability (p) must be between 0 and 1 (exclusive)")
    
    if q <= 1:
        raise ValueError("Payout multiplier (q) must be greater than 1")
    
    if j <= 0:
        raise ValueError("Bet size (j) must be greater than 0")
    
    if trials <= 0:
        raise ValueError("Number of trials must be greater than 0")
    
    if trials > 1000000:
        raise ValueError("Number of trials cannot exceed 1,000,000")
    
    # Return validated parameters
    return {
        'i': i,
        'n': n,
        'p': p,
        'q': q,
        'j': j,
        'trials': trials
    }


def validate_extended_params(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate parameters for extended simulation.
    
    Args:
        data: Request data containing simulation parameters
        
    Returns:
        Dict with validated parameters
        
    Raises:
        ValueError: If any parameters are invalid
    """
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object")
    
    # Start with general parameter validation
    params = validate_general_params(data)
    
    # Get extension flags
    use_credit = bool(data.get('use_credit', False))
    use_dynamic_betting = bool(data.get('use_dynamic_betting', False))
    use_max_bet = bool(data.get('use_max_bet', False))
    
    # Check extension-specific parameters
    if use_credit:
        if 'k' not in data:
            raise ValueError("Missing required parameter: k (credit line amount)")
        
        try:
            k = int(data['k'])
        except (ValueError, TypeError):
            raise ValueError("Credit line amount (k) must be an integer")
        
        if k <= 0:
            raise ValueError("Credit line amount (k) must be greater than 0")
        
        params['k'] = k
    
    if use_max_bet:
        if 'm' not in data:
            raise ValueError("Missing required parameter: m (maximum bet)")
        
        try:
            m = int(data['m'])
        except (ValueError, TypeError):
            raise ValueError("Maximum bet (m) must be an integer")
        
        if m <= 0:
            raise ValueError("Maximum bet (m) must be greater than 0")
        
        params['m'] = m
    
    # Add extension flags to params
    params['use_credit'] = use_credit
    params['use_dynamic_betting'] = use_dynamic_betting
    params['use_max_bet'] = use_max_bet
    
    return params 