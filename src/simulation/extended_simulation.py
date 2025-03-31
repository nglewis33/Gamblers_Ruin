"""
Extended Gambler's Ruin Simulation Module (Problem 3)

This module implements realistic extensions to the Gambler's Ruin problem:
(a) The gambler has a line of credit up to an amount k if they hit 0
(b) The gambler increases bet by a factor of 1/p after each loss (dynamic betting)
(c) The house implements a maximum bet per table of m dollars
"""

import random
import numpy as np
from typing import Dict, Tuple


def run_with_credit(i: int, n: int, p: float, q: float, j: int, k: int, trials: int = 10000) -> Dict[str, float]:
    """
    Run simulation with line of credit extension.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        p: Probability of winning
        q: Payout multiplier
        j: Bet size
        k: Credit line amount
        trials: Number of simulations to run
        
    Returns:
        Dict with win_probability and broke_probability
    """
    wins = 0
    
    for _ in range(trials):
        current_amount = i
        credit_used = 0
        
        while current_amount + credit_used < n and credit_used <= k:
            # Determine bet size (not exceeding current amount)
            if current_amount > 0:
                bet = min(j, current_amount)
            else:
                # Use credit if needed and available
                bet = min(j, k - credit_used)
                if bet <= 0:
                    break  # No more credit available
                credit_used += bet
            
            # Win with probability p
            if random.random() < p:
                winnings = bet * (q - 1)
                
                # Pay back credit first if any is used
                if credit_used > 0:
                    repayment = min(winnings, credit_used)
                    credit_used -= repayment
                    winnings -= repayment
                
                current_amount += winnings
            else:
                # If using current funds
                if current_amount >= bet:
                    current_amount -= bet
                # Credit was already accounted for above
            
        # Win if reached goal
        if current_amount + credit_used >= n:
            wins += 1
    
    win_probability = wins / trials
    broke_probability = 1 - win_probability
    
    return {
        'win_probability': win_probability,
        'broke_probability': broke_probability
    }


def run_with_dynamic_betting(i: int, n: int, p: float, q: float, j: int, trials: int = 10000) -> Dict[str, float]:
    """
    Run simulation with dynamic betting strategy.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        p: Probability of winning
        q: Payout multiplier
        j: Initial bet size
        trials: Number of simulations to run
        
    Returns:
        Dict with win_probability and broke_probability
    """
    wins = 0
    
    for _ in range(trials):
        current_amount = i
        current_bet = j
        losing_streak = 0
        
        while 0 < current_amount < n:
            # Ensure bet doesn't exceed current amount
            actual_bet = min(current_bet, current_amount)
            
            # Win with probability p
            if random.random() < p:
                current_amount += actual_bet * (q - 1)
                current_bet = j  # Reset bet size after win
                losing_streak = 0
            else:
                current_amount -= actual_bet
                losing_streak += 1
                # Increase bet by factor of 1/p after loss
                current_bet = j * (1/p) ** losing_streak
            
        # Win if reached goal
        if current_amount >= n:
            wins += 1
    
    win_probability = wins / trials
    broke_probability = 1 - win_probability
    
    return {
        'win_probability': win_probability,
        'broke_probability': broke_probability
    }


def run_with_max_bet(i: int, n: int, p: float, q: float, j: int, m: int, trials: int = 10000) -> Dict[str, float]:
    """
    Run simulation with maximum bet limitation.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        p: Probability of winning
        q: Payout multiplier
        j: Bet size
        m: Maximum bet
        trials: Number of simulations to run
        
    Returns:
        Dict with win_probability and broke_probability
    """
    wins = 0
    
    for _ in range(trials):
        current_amount = i
        
        while 0 < current_amount < n:
            # Apply bet limits
            bet = min(j, current_amount, m)
            
            # Win with probability p
            if random.random() < p:
                current_amount += bet * (q - 1)
            else:
                current_amount -= bet
            
        # Win if reached goal
        if current_amount >= n:
            wins += 1
    
    win_probability = wins / trials
    broke_probability = 1 - win_probability
    
    return {
        'win_probability': win_probability,
        'broke_probability': broke_probability
    }


def run_full_extension(i: int, n: int, p: float, q: float, j: int, k: int, m: int, trials: int = 10000) -> Dict[str, float]:
    """
    Run simulation with all extensions enabled.
    
    Args:
        i: Starting amount (dollars)
        n: Goal amount (dollars)
        p: Probability of winning
        q: Payout multiplier
        j: Initial bet size
        k: Credit line amount
        m: Maximum bet
        trials: Number of simulations to run
        
    Returns:
        Dict with win_probability and broke_probability
    """
    wins = 0
    
    for _ in range(trials):
        current_amount = i
        credit_used = 0
        current_bet = j
        losing_streak = 0
        
        while (current_amount + credit_used < n) and (credit_used <= k):
            # Apply dynamic betting based on losing streak
            if losing_streak > 0:
                current_bet = j * (1/p) ** losing_streak
            else:
                current_bet = j
            
            # Apply maximum bet limitation
            current_bet = min(current_bet, m)
            
            # Determine actual bet based on available funds
            if current_amount > 0:
                actual_bet = min(current_bet, current_amount)
            else:
                # Use credit if needed and available
                actual_bet = min(current_bet, k - credit_used)
                if actual_bet <= 0:
                    break  # No more credit available
                credit_used += actual_bet
            
            # Win with probability p
            if random.random() < p:
                winnings = actual_bet * (q - 1)
                
                # Pay back credit first if any is used
                if credit_used > 0:
                    repayment = min(winnings, credit_used)
                    credit_used -= repayment
                    winnings -= repayment
                
                current_amount += winnings
                current_bet = j  # Reset bet size after win
                losing_streak = 0
            else:
                # If using current funds
                if current_amount >= actual_bet:
                    current_amount -= actual_bet
                # Credit was already accounted for above
                losing_streak += 1
            
        # Win if reached goal
        if current_amount + credit_used >= n:
            wins += 1
    
    win_probability = wins / trials
    broke_probability = 1 - win_probability
    
    return {
        'win_probability': win_probability,
        'broke_probability': broke_probability
    } 