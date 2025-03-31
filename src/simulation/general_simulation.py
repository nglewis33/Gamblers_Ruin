"""
Generalized Gambler's Ruin Simulation Module (Problem 2)

This module extends the basic simulation with additional parameters:
(a) Win probability (p)
(b) Payout multiplier (q)
(c) Bet size (j)
(d) Starting amount (i)
(e) Goal amount (n)
"""

import random
import numpy as np
from typing import Dict


def run_general_simulation(i: int, n: int, p: float, q: float, j: int) -> bool:
    """
    Run a single simulation of the generalized Gambler's Ruin problem.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        p: Probability of winning
        q: Payout multiplier
        j: Bet size
        
    Returns:
        bool: True if the gambler wins (reaches n dollars), False if they go broke
    """
    current_amount = i
    
    while 0 < current_amount < n:
        # Place a bet of j dollars
        bet = min(j, current_amount)  # Ensure bet is not larger than current amount
        
        # Win with probability p
        if random.random() < p:
            current_amount += bet * (q - 1)  # Win: get back bet plus q-1 times bet
        else:
            current_amount -= bet  # Lose: lose the bet
    
    # Return True if the gambler reached their goal
    return current_amount >= n


def monte_carlo_general(i: int, n: int, p: float, q: float, j: int, trials: int = 10000) -> Dict[str, float]:
    """
    Run multiple simulations of the generalized Gambler's Ruin problem to estimate probabilities.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        p: Probability of winning
        q: Payout multiplier
        j: Bet size
        trials: Number of simulations to run
        
    Returns:
        Dict with keys 'win_probability' and 'broke_probability'
    """
    # Validate inputs
    if i <= 0 or n <= i or p <= 0 or p >= 1 or q <= 1 or j <= 0 or trials <= 0:
        raise ValueError("Invalid input parameters. Must have 0 < i < n, 0 < p < 1, q > 1, j > 0, and trials > 0.")
    
    wins = 0
    
    for _ in range(trials):
        if run_general_simulation(i, n, p, q, j):
            wins += 1
    
    win_probability = wins / trials
    broke_probability = 1 - win_probability
    
    return {
        'win_probability': win_probability,
        'broke_probability': broke_probability
    }


def theoretical_win_probability(i: int, n: int, p: float) -> float:
    """
    Calculate the theoretical win probability for the Gambler's Ruin problem.
    For a fair game (p=0.5), the win probability is i/n.
    For an unfair game, it's (1-(q/p)^i)/(1-(q/p)^n) where q=1-p.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        p: Probability of winning
        
    Returns:
        float: Theoretical probability of winning
    """
    if p == 0.5:
        return i / n
    
    q = 1 - p
    ratio = q / p
    return (1 - ratio**i) / (1 - ratio**n) 