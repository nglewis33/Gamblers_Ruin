"""
Basic Gambler's Ruin Simulation Module (Problem 1)

This module implements the classic Gambler's Ruin problem where:
1. A gambler plays a fair game with a 1/2 chance of winning
2. Winning causes them to double their money
3. The minimum bet is 1 dollar
4. The gambler starts with i and will continue until either they have 0 dollars or achieve n dollars
"""

import random
import numpy as np
from typing import Tuple, Dict


def run_single_simulation(i: int, n: int) -> bool:
    """
    Run a single simulation of the Gambler's Ruin problem.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        
    Returns:
        bool: True if the gambler wins (reaches n dollars), False if they go broke
    """
    current_amount = i
    
    while 0 < current_amount < n:
        # Place a bet of 1 dollar
        bet = 1
        
        # Win with probability 0.5
        if random.random() < 0.5:
            current_amount += bet  # Win (double the money)
        else:
            current_amount -= bet  # Lose
    
    # Return True if the gambler reached their goal
    return current_amount >= n


def monte_carlo_simulation(i: int, n: int, trials: int = 10000) -> Dict[str, float]:
    """
    Run multiple simulations of the Gambler's Ruin problem to estimate probabilities.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        trials: Number of simulations to run
        
    Returns:
        Dict with keys 'win_probability' and 'broke_probability'
    """
    # Validate inputs
    if i <= 0 or n <= i or trials <= 0:
        raise ValueError("Invalid input parameters. Must have 0 < i < n and trials > 0.")
    
    wins = 0
    
    for _ in range(trials):
        if run_single_simulation(i, n):
            wins += 1
    
    win_probability = wins / trials
    broke_probability = 1 - win_probability
    
    return {
        'win_probability': win_probability,
        'broke_probability': broke_probability
    }


def theoretical_win_probability(i: int, n: int) -> float:
    """
    Calculate the theoretical win probability for the Gambler's Ruin problem.
    For a fair game (p=0.5), the win probability is i/n.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        
    Returns:
        float: Theoretical probability of winning
    """
    return i / n 