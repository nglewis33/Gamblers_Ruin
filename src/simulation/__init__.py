"""
Gambler's Ruin Simulation Module

This module provides implementations for various versions of the Gambler's Ruin problem.
"""

from src.simulation.basic_simulation import monte_carlo_simulation
from src.simulation.general_simulation import monte_carlo_general
from src.simulation.extended_simulation import (
    run_with_credit,
    run_with_dynamic_betting,
    run_with_max_bet,
    run_full_extension
)

__all__ = [
    'monte_carlo_simulation',
    'monte_carlo_general',
    'run_with_credit',
    'run_with_dynamic_betting',
    'run_with_max_bet',
    'run_full_extension'
] 