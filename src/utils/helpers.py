"""
Helper Functions for Gambler's Ruin Simulation

This module provides utility functions used across the application.
"""

import time
from typing import Dict, Callable, Any


def time_execution(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    Measure execution time of a function.
    
    Args:
        func: Function to execute
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Dict containing function result and execution time
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    
    # If result is a dict, add execution time to it
    if isinstance(result, dict):
        result['execution_time'] = execution_time
        return result
    
    # Otherwise, return a new dict with result and execution time
    return {
        'result': result,
        'execution_time': execution_time
    }


def format_probability(probability: float) -> str:
    """
    Format a probability as a percentage string.
    
    Args:
        probability: Probability value between 0 and 1
        
    Returns:
        Formatted string representing the probability as a percentage
    """
    return f"{probability * 100:.2f}%" 