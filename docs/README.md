# Gambler's Ruin Simulation
# Technical Documentation and Methodology

## Table of Contents
1. [Introduction](#introduction)
2. [Project Architecture](#project-architecture)
3. [Simulation Methodology](#simulation-methodology)
4. [Technical Implementation](#technical-implementation)
5. [Infrastructure](#infrastructure)
6. [API Reference](#api-reference)
7. [Data Visualization](#data-visualization)
8. [Development Notes](#development-notes)

## Introduction

The Gambler's Ruin is a classic problem in probability theory that models a gambler who starts with an initial fortune and plays a sequence of bets against an opponent (typically a casino), resulting in either achieving a target fortune or going broke. This project implements various computational simulations of the Gambler's Ruin problem, offering both Monte Carlo simulations and theoretical probability calculations.

## Project Architecture

The project follows a clean, modular architecture designed around separation of concerns:

```
gamblers-ruin/
├── src/                    # Core source code
│   ├── simulation/         # Simulation logic modules
│   │   ├── basic_simulation.py     # Problem 1: Basic simulation
│   │   ├── general_simulation.py   # Problem 2: Generalized simulation
│   │   └── extended_simulation.py  # Problem 3: Extended simulation
│   ├── api/                # API layer
│   │   ├── app.py          # Flask application initialization
│   │   ├── routes.py       # API endpoints
│   │   └── validation.py   # Input validation
│   └── utils/              # Utility functions
├── web/                    # Web interface
│   ├── serve.py            # Web server
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JavaScript, and other static assets
├── tests/                  # Test suite
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── start.ps1               # PowerShell startup script
├── start.bat               # Batch startup script
├── stop.ps1                # PowerShell stop script
└── stop.bat                # Batch stop script
```

This architecture separates the core simulation logic from the web and API interfaces, allowing each component to be maintained and tested independently.

## Simulation Methodology

The project implements three levels of simulation for the Gambler's Ruin problem:

### 1. Basic Simulation (Problem 1)

The classic Gambler's Ruin scenario with fixed constraints:
- 50% probability of winning each bet
- Bet amount is fixed at $1
- On winning, the gambler doubles their money (gets back $2)
- The gambler continues until they either reach the goal amount or go broke

Theoretical win probability: P(win) = i/n, where:
- i = initial amount
- n = goal amount

```python
def run_single_simulation(i: int, n: int) -> bool:
    current_amount = i
    
    while 0 < current_amount < n:
        bet = 1
        if random.random() < 0.5:
            current_amount += bet  # Win (double the money)
        else:
            current_amount -= bet  # Lose
    
    return current_amount >= n
```

### 2. Generalized Simulation (Problem 2)

Extended version with customizable parameters:
- Variable probability of winning (p)
- Variable payout multiplier (q)
- Variable bet size (j)
- Customizable starting amount (i)
- Customizable goal amount (n)

Theoretical win probability:
- For fair games (p=0.5): P(win) = i/n
- For unfair games (p≠0.5): P(win) = (1-(q/p)^i)/(1-(q/p)^n) where q=1-p

```python
def run_general_simulation(i: int, n: int, p: float, q: float, j: int) -> bool:
    current_amount = i
    
    while 0 < current_amount < n:
        bet = min(j, current_amount)  # Ensure bet is not larger than current amount
        
        if random.random() < p:
            current_amount += bet * (q - 1)  # Win: get back bet plus q-1 times bet
        else:
            current_amount -= bet  # Lose: lose the bet
    
    return current_amount >= n
```

### 3. Extended Simulation (Problem 3)

Further extensions adding more realistic conditions:
- **Credit Line**: Allows the gambler to borrow up to k dollars
- **Dynamic Betting Strategy**: Adjust bet size based on current fortune
- **Maximum Bet Limitation**: Restricts the maximum bet size to m dollars

Each extension is implemented individually and can be combined for a full simulation:

```python
# Example: Running simulation with credit line
def run_with_credit(i, n, p, q, j, k, trials):
    # Implementation details in extended_simulation.py
    
# Example: Running full simulation with all extensions
def run_full_extension(i, n, p, q, j, k, m, trials):
    # Implementation details in extended_simulation.py
```

### Monte Carlo Method

All simulations are run using the Monte Carlo method, which involves:
1. Simulating a large number of individual games
2. Calculating the proportion of successful outcomes
3. As the number of trials increases, the estimated probability converges to the true probability

```python
def monte_carlo_simulation(i, n, trials=10000):
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
```

## Technical Implementation

### Core Simulation Logic

The simulation logic is implemented in three Python modules, each handling a different level of complexity:

1. `basic_simulation.py`: Implements the classic Gambler's Ruin problem
2. `general_simulation.py`: Extends the basic simulation with customizable parameters
3. `extended_simulation.py`: Adds realistic extensions like credit line, dynamic betting, and maximum bet limitation

Each module provides functions for:
- Running a single simulation
- Running multiple simulations (Monte Carlo)
- Calculating theoretical probabilities when possible

### API Layer

The API is built using Flask and provides RESTful endpoints for accessing the simulation functionality:

- `/api/basic-simulation`: Runs the basic simulation
- `/api/general-simulation`: Runs the generalized simulation
- `/api/extended-simulation`: Runs the extended simulation with selected extensions
- `/api/docs`: Provides API documentation

The API implements proper validation of input parameters and error handling:

```python
@api_bp.route('/basic-simulation', methods=['POST'])
def basic_simulation_endpoint():
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
```

### Web Interface

The web interface is also built with Flask and provides a user-friendly way to interact with the simulations. It consists of:

- HTML templates for different simulation types
- JavaScript for dynamic form handling and visualization
- CSS for styling and responsive design

The web server runs separately from the API server to maintain separation of concerns and allow independent scaling.

## Infrastructure

The project utilizes a dual-server architecture:

1. **API Server**:
   - Flask application serving the REST API endpoints
   - Runs on port 5000 by default
   - Handles simulation logic and results processing

2. **Web Server**:
   - Flask application serving the web interface
   - Runs on port 5050 by default
   - Makes AJAX calls to the API server to run simulations

### Automation Scripts

To simplify deployment and operation, the project includes automation scripts:

1. **Start Scripts**:
   - `start.ps1` (PowerShell): Sets up the environment and starts both servers
   - `start.bat` (Windows Batch): Alternative for Command Prompt users

2. **Stop Scripts**:
   - `stop.ps1` (PowerShell): Safely terminates both servers
   - `stop.bat` (Windows Batch): Alternative for Command Prompt users

These scripts handle:
- Virtual environment activation
- Dependency installation
- Server startup in separate windows
- Browser launching
- Process termination

Example start script functionality:
```powershell
# Check if virtual environment exists
if (-not (Test-Path ".\venv\Scripts\activate.ps1")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\activate.ps1

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start servers in separate windows
Write-Host "Starting API server on port 5000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$scriptPath'; & .\venv\Scripts\activate.ps1; python -m src.api.app}"

# Start web server in a new window
Write-Host "Starting web server on port 5050..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$scriptPath'; & .\venv\Scripts\activate.ps1; python -m web.serve}"
```

## API Reference

The API provides the following endpoints:

### Basic Simulation

**Endpoint**: `POST /api/basic-simulation`

**Parameters**:
- `i`: Starting amount (dollars)
- `n`: Goal amount (dollars)
- `trials`: Number of simulations to run (default: 10000)

**Example Request**:
```json
{
  "i": 10,
  "n": 20,
  "trials": 5000
}
```

**Example Response**:
```json
{
  "win_probability": 0.5,
  "broke_probability": 0.5
}
```

### General Simulation

**Endpoint**: `POST /api/general-simulation`

**Parameters**:
- `i`: Starting amount (dollars)
- `n`: Goal amount (dollars)
- `p`: Probability of winning (0 < p < 1)
- `q`: Payout multiplier (q > 1)
- `j`: Bet size (j > 0)
- `trials`: Number of simulations to run (default: 10000)

**Example Request**:
```json
{
  "i": 10,
  "n": 20,
  "p": 0.4,
  "q": 1.5,
  "j": 2,
  "trials": 5000
}
```

### Extended Simulation

**Endpoint**: `POST /api/extended-simulation`

**Parameters**:
- `i`: Starting amount (dollars)
- `n`: Goal amount (dollars)
- `p`: Probability of winning (0 < p < 1)
- `q`: Payout multiplier (q > 1)
- `j`: Bet size (j > 0)
- `k`: Credit line amount (required if use_credit=true)
- `m`: Maximum bet (required if use_max_bet=true)
- `use_credit`: Enable line of credit (boolean)
- `use_dynamic_betting`: Enable dynamic betting (boolean)
- `use_max_bet`: Enable maximum bet limit (boolean)
- `trials`: Number of simulations to run (default: 10000)

## Development Notes

### Dependencies

The project uses the following main dependencies:
- Flask: Web framework
- NumPy: Numerical operations
- Werkzeug: WSGI utilities

### Testing

Tests are organized in the `tests/` directory and can be run using pytest:
```
pytest
```

### Future Improvements

Potential enhancements for the project:
1. More advanced betting strategies
2. Visualization of simulation results using plotting libraries
3. Batch simulation capabilities for parameter sweeps
4. Expanded theoretical analysis
5. More sophisticated UI with real-time updates 