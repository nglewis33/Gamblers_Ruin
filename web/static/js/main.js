/**
 * Main JavaScript for Gambler's Ruin Simulation UI
 * 
 * This module handles form submissions and UI interactions.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const basicForm = document.getElementById('basic-form');
    const generalForm = document.getElementById('general-form');
    const extendedForm = document.getElementById('extended-form');
    
    // Basic simulation form handling
    if (basicForm) {
        basicForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Show loading state
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.textContent = 'Running...';
            submitButton.disabled = true;
            
            try {
                // Get form values
                const i = parseInt(document.getElementById('basic-i').value);
                const n = parseInt(document.getElementById('basic-n').value);
                const trials = parseInt(document.getElementById('basic-trials').value);
                
                // Validate input
                if (i <= 0 || n <= i || trials <= 0) {
                    throw new Error('Invalid input parameters. Must have 0 < i < n and trials > 0.');
                }
                
                // Run simulation
                const result = await runBasicSimulation({ i, n, trials });
                
                // Display results
                document.getElementById('basic-win-prob').textContent = (result.win_probability * 100).toFixed(2) + '%';
                document.getElementById('basic-broke-prob').textContent = (result.broke_probability * 100).toFixed(2) + '%';
                
                // Show results section
                document.getElementById('basic-result').classList.remove('d-none');
                
                // Create chart
                createProbabilityChart('basic-chart', result);
            } catch (error) {
                alert('Error: ' + error.message);
                console.error(error);
            } finally {
                // Restore button state
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            }
        });
    }
    
    // General simulation form handling
    if (generalForm) {
        generalForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Show loading state
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.textContent = 'Running...';
            submitButton.disabled = true;
            
            try {
                // Get form values
                const i = parseInt(document.getElementById('general-i').value);
                const n = parseInt(document.getElementById('general-n').value);
                const p = parseFloat(document.getElementById('general-p').value);
                const q = parseFloat(document.getElementById('general-q').value);
                const j = parseInt(document.getElementById('general-j').value);
                const trials = parseInt(document.getElementById('general-trials').value);
                
                // Validate input
                if (i <= 0 || n <= i || p <= 0 || p >= 1 || q <= 1 || j <= 0 || trials <= 0) {
                    throw new Error('Invalid input parameters.');
                }
                
                // Run simulation
                const result = await runGeneralSimulation({ i, n, p, q, j, trials });
                
                // Display results
                document.getElementById('general-win-prob').textContent = (result.win_probability * 100).toFixed(2) + '%';
                document.getElementById('general-broke-prob').textContent = (result.broke_probability * 100).toFixed(2) + '%';
                
                // Show results section
                document.getElementById('general-result').classList.remove('d-none');
                
                // Create chart
                createProbabilityChart('general-chart', result);
            } catch (error) {
                alert('Error: ' + error.message);
                console.error(error);
            } finally {
                // Restore button state
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            }
        });
    }
    
    // Extended simulation form handling
    if (extendedForm) {
        // Toggle visibility of credit amount input based on checkbox
        const useCreditCheckbox = document.getElementById('use-credit');
        const creditAmountContainer = document.getElementById('credit-amount-container');
        
        useCreditCheckbox.addEventListener('change', function() {
            creditAmountContainer.classList.toggle('d-none', !this.checked);
        });
        
        // Toggle visibility of max bet input based on checkbox
        const useMaxBetCheckbox = document.getElementById('use-max-bet');
        const maxBetContainer = document.getElementById('max-bet-container');
        
        useMaxBetCheckbox.addEventListener('change', function() {
            maxBetContainer.classList.toggle('d-none', !this.checked);
        });
        
        // Form submission
        extendedForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Show loading state
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.textContent = 'Running...';
            submitButton.disabled = true;
            
            try {
                // Get form values
                const i = parseInt(document.getElementById('extended-i').value);
                const n = parseInt(document.getElementById('extended-n').value);
                const p = parseFloat(document.getElementById('extended-p').value);
                const q = parseFloat(document.getElementById('extended-q').value);
                const j = parseInt(document.getElementById('extended-j').value);
                const trials = parseInt(document.getElementById('extended-trials').value);
                
                // Get extension options
                const useCredit = document.getElementById('use-credit').checked;
                const useDynamicBetting = document.getElementById('use-dynamic-betting').checked;
                const useMaxBet = document.getElementById('use-max-bet').checked;
                
                // Get conditional parameters
                let params = { i, n, p, q, j, trials, use_credit: useCredit, use_dynamic_betting: useDynamicBetting, use_max_bet: useMaxBet };
                
                // Add credit amount if credit is used
                if (useCredit) {
                    params.k = parseInt(document.getElementById('extended-k').value);
                }
                
                // Add max bet if max bet is used
                if (useMaxBet) {
                    params.m = parseInt(document.getElementById('extended-m').value);
                }
                
                // Check if at least one extension is enabled
                if (!useCredit && !useDynamicBetting && !useMaxBet) {
                    throw new Error('Please select at least one extension.');
                }
                
                // Run simulation
                const result = await runExtendedSimulation(params);
                
                // Display results
                document.getElementById('extended-win-prob').textContent = (result.win_probability * 100).toFixed(2) + '%';
                document.getElementById('extended-broke-prob').textContent = (result.broke_probability * 100).toFixed(2) + '%';
                
                // Show results section
                document.getElementById('extended-result').classList.remove('d-none');
                
                // Create chart
                createProbabilityChart('extended-chart', result);
            } catch (error) {
                alert('Error: ' + error.message);
                console.error(error);
            } finally {
                // Restore button state
                submitButton.textContent = originalButtonText;
                submitButton.disabled = false;
            }
        });
    }
});

/**
 * Smooth scrolling for navigation links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 70, // Offset for navbar
                behavior: 'smooth'
            });
            
            // Update active link
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        }
    });
}); 