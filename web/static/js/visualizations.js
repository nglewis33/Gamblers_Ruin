/**
 * Visualizations for Gambler's Ruin Simulation
 * 
 * This module provides functions for creating data visualizations
 * of simulation results using Chart.js.
 */

/**
 * Create a pie chart showing win and broke probabilities
 * @param {string} canvasId - ID of the canvas element
 * @param {Object} data - Simulation results with win_probability and broke_probability
 */
function createProbabilityChart(canvasId, data) {
    // Get canvas element
    const canvas = document.getElementById(canvasId);
    
    // Check if a chart already exists on this canvas
    if (canvas._chart) {
        canvas._chart.destroy();
    }
    
    // Create pie chart
    canvas._chart = new Chart(canvas, {
        type: 'pie',
        data: {
            labels: ['Win', 'Broke'],
            datasets: [{
                data: [
                    data.win_probability * 100, 
                    data.broke_probability * 100
                ],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 99, 132, 0.8)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.raw.toFixed(2) + '%';
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Probability Distribution'
                }
            }
        }
    });
}

/**
 * Create a bar chart comparing multiple simulation results
 * @param {string} canvasId - ID of the canvas element
 * @param {Array<Object>} dataArray - Array of simulation results
 * @param {Array<string>} labels - Labels for each dataset
 */
function createComparisonChart(canvasId, dataArray, labels) {
    // Get canvas element
    const canvas = document.getElementById(canvasId);
    
    // Check if a chart already exists on this canvas
    if (canvas._chart) {
        canvas._chart.destroy();
    }
    
    // Extract win probabilities
    const winProbabilities = dataArray.map(data => data.win_probability * 100);
    const brokeProbabilities = dataArray.map(data => data.broke_probability * 100);
    
    // Create chart
    canvas._chart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Win Probability',
                    data: winProbabilities,
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Broke Probability',
                    data: brokeProbabilities,
                    backgroundColor: 'rgba(255, 99, 132, 0.8)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Probability (%)'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Comparison of Simulation Results'
                }
            }
        }
    });
}

/**
 * Create a line chart showing how probabilities change with parameter variations
 * @param {string} canvasId - ID of the canvas element
 * @param {Array<number>} xValues - X-axis values (parameter values)
 * @param {Array<Object>} results - Array of simulation results
 * @param {string} xLabel - Label for x-axis
 */
function createParameterSensitivityChart(canvasId, xValues, results, xLabel) {
    // Get canvas element
    const canvas = document.getElementById(canvasId);
    
    // Check if a chart already exists on this canvas
    if (canvas._chart) {
        canvas._chart.destroy();
    }
    
    // Extract win probabilities
    const winProbabilities = results.map(result => result.win_probability * 100);
    
    // Create chart
    canvas._chart = new Chart(canvas, {
        type: 'line',
        data: {
            labels: xValues,
            datasets: [{
                label: 'Win Probability',
                data: winProbabilities,
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Win Probability (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: xLabel
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Parameter Sensitivity Analysis'
                }
            }
        }
    });
} 