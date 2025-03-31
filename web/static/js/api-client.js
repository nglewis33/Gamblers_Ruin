/**
 * API Client for Gambler's Ruin Simulation
 * 
 * This module provides functions for interacting with the Gambler's Ruin API.
 */

// Use localhost instead of an IP address to avoid CORS issues
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Run the basic Gambler's Ruin simulation
 * @param {Object} params - Simulation parameters
 * @param {number} params.i - Starting amount
 * @param {number} params.n - Goal amount
 * @param {number} params.trials - Number of simulations
 * @returns {Promise<Object>} - Simulation results
 */
async function runBasicSimulation(params) {
    try {
        console.log('Calling API with params:', params);
        const response = await fetch(`${API_BASE_URL}/basic-simulation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `API request failed with status ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error in runBasicSimulation:', error);
        if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            throw new Error(`Network error: Could not connect to API server at ${API_BASE_URL}. Make sure the API server is running.`);
        }
        throw error;
    }
}

/**
 * Run the generalized Gambler's Ruin simulation
 * @param {Object} params - Simulation parameters
 * @param {number} params.i - Starting amount
 * @param {number} params.n - Goal amount
 * @param {number} params.p - Win probability
 * @param {number} params.q - Payout multiplier
 * @param {number} params.j - Bet size
 * @param {number} params.trials - Number of simulations
 * @returns {Promise<Object>} - Simulation results
 */
async function runGeneralSimulation(params) {
    try {
        console.log('Calling API with params:', params);
        const response = await fetch(`${API_BASE_URL}/general-simulation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `API request failed with status ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error in runGeneralSimulation:', error);
        if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            throw new Error(`Network error: Could not connect to API server at ${API_BASE_URL}. Make sure the API server is running.`);
        }
        throw error;
    }
}

/**
 * Run the extended Gambler's Ruin simulation
 * @param {Object} params - Simulation parameters
 * @param {number} params.i - Starting amount
 * @param {number} params.n - Goal amount
 * @param {number} params.p - Win probability
 * @param {number} params.q - Payout multiplier
 * @param {number} params.j - Bet size
 * @param {number} params.k - Credit line amount (optional)
 * @param {number} params.m - Maximum bet (optional)
 * @param {boolean} params.use_credit - Enable line of credit
 * @param {boolean} params.use_dynamic_betting - Enable dynamic betting
 * @param {boolean} params.use_max_bet - Enable maximum bet
 * @param {number} params.trials - Number of simulations
 * @returns {Promise<Object>} - Simulation results
 */
async function runExtendedSimulation(params) {
    try {
        console.log('Calling API with params:', params);
        const response = await fetch(`${API_BASE_URL}/extended-simulation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `API request failed with status ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error in runExtendedSimulation:', error);
        if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            throw new Error(`Network error: Could not connect to API server at ${API_BASE_URL}. Make sure the API server is running.`);
        }
        throw error;
    }
}

/**
 * Get API documentation
 * @returns {Promise<Object>} - API documentation
 */
async function getApiDocs() {
    try {
        const response = await fetch(`${API_BASE_URL}/docs`);

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error in getApiDocs:', error);
        if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            throw new Error(`Network error: Could not connect to API server at ${API_BASE_URL}. Make sure the API server is running.`);
        }
        throw error;
    }
} 