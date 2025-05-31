// AI Cognitive Simulator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const cognitiveForm = document.getElementById('cognitive-form');
    const userInput = document.getElementById('user-input');
    const resultsContainer = document.getElementById('results-container');
    const loadingContainer = document.getElementById('loading-container');
    const initialMessage = document.getElementById('initial-message');
    const resultInput = document.getElementById('result-input');
    const moduleResults = document.getElementById('module-results');
    const finalOutput = document.getElementById('final-output');
    const brainRegions = document.getElementById('brain-regions');
    const currentModuleInfo = document.getElementById('current-module-info');
    const currentModuleName = document.getElementById('current-module-name');
    const currentModuleDescription = document.getElementById('current-module-description');
    const processingProgress = document.getElementById('processing-progress');
    
    // Brain module data
    const brainModules = [
        { id: 'prefrontal_cortex', name: 'Prefrontal Cortex', emoji: '🧠', description: 'Planning, decision-making, and social behavior analysis' },
        { id: 'amygdala', name: 'Amygdala', emoji: '😲', description: 'Emotional processing (fear, pleasure, anxiety)' },
        { id: 'hippocampus', name: 'Hippocampus', emoji: '📚', description: 'Memory and contextual relationships' },
        { id: 'thalamus', name: 'Thalamus', emoji: '🔄', description: 'Information relay and integration' },
        { id: 'sensory_cortex', name: 'Sensory Cortex', emoji: '👐', description: 'Physical sensations and tactile imagery' },
        { id: 'auditory_cortex', name: 'Auditory Cortex', emoji: '👂', description: 'Auditory processing and tone interpretation' },
        { id: 'visual_cortex', name: 'Visual Cortex', emoji: '👁️', description: 'Visual imagery and perception' },
        { id: 'motor_cortex', name: 'Motor Cortex', emoji: '🏃', description: 'Action planning and movement coordination' },
        { id: 'hypothalamus', name: 'Hypothalamus', emoji: '🌡️', description: 'Physiological and instinctive responses' },
        { id: 'cerebellum', name: 'Cerebellum', emoji: '⚖️', description: 'Fine-tuning and balance' },
        { id: 'brain_stem', name: 'Brain Stem', emoji: '⚡', description: 'Vital responses and basic survival functions' }
    ];
    
    // Initialize brain visualization
    initializeBrainVisualization();
    
    // Event listeners
    cognitiveForm.addEventListener('submit', handleFormSubmit);
    
    // Initialize brain visualization
    function initializeBrainVisualization() {
        // Create brain regions
        brainModules.forEach(module => {
            const region = document.createElement('div');
            region.id = `${module.id}-region`;
            region.className = 'brain-region';
            region.setAttribute('data-module', module.id);
            region.setAttribute('title', `${module.name}: ${module.description}`);
            
            region.addEventListener('click', () => {
                // Show module info on click
                showModuleInfo(module);
            });
            
            brainRegions.appendChild(region);
        });
        
        // Create neural connections between regions
        createNeuralConnections();
    }
    
    function createNeuralConnections() {
        // Create connections between consecutive brain regions
        for (let i = 0; i < brainModules.length - 1; i++) {
            const connection = document.createElement('div');
            connection.className = 'neural-connection';
            connection.id = `connection-${i}-${i+1}`;
            brainRegions.appendChild(connection);
            
            // Position will be set dynamically when processing starts
        }
    }
    
    function updateNeuralConnections() {
        // Update position of neural connections based on brain region positions
        for (let i = 0; i < brainModules.length - 1; i++) {
            const fromRegion = document.getElementById(`${brainModules[i].id}-region`);
            const toRegion = document.getElementById(`${brainModules[i+1].id}-region`);
            const connection = document.getElementById(`connection-${i}-${i+1}`);
            
            if (fromRegion && toRegion && connection) {
                const fromRect = fromRegion.getBoundingClientRect();
                const toRect = toRegion.getBoundingClientRect();
                const brainRect = brainRegions.getBoundingClientRect();
                
                // Calculate positions relative to the brain container
                const fromX = (fromRect.left + fromRect.width/2) - brainRect.left;
                const fromY = (fromRect.top + fromRect.height/2) - brainRect.top;
                const toX = (toRect.left + toRect.width/2) - brainRect.left;
                const toY = (toRect.top + toRect.height/2) - brainRect.top;
                
                // Calculate length and angle
                const length = Math.sqrt(Math.pow(toX - fromX, 2) + Math.pow(toY - fromY, 2));
                const angle = Math.atan2(toY - fromY, toX - fromX) * 180 / Math.PI;
                
                // Position the connection
                connection.style.width = `${length}px`;
                connection.style.left = `${fromX}px`;
                connection.style.top = `${fromY}px`;
                connection.style.transform = `rotate(${angle}deg)`;
            }
        }
    }
    
    function showModuleInfo(module) {
        // Display module information
        currentModuleInfo.classList.remove('hidden');
        currentModuleName.textContent = `${module.emoji} ${module.name}`;
        currentModuleDescription.textContent = module.description;
    }
    
    // Handle form submission
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        // Get user input
        const text = userInput.value.trim();
        if (!text) {
            alert('Please enter a phrase to process.');
            return;
        }
        
        // Show loading state
        initialMessage.classList.add('hidden');
        resultsContainer.classList.add('hidden');
        loadingContainer.classList.remove('hidden');
        
        // Clear previous results
        moduleResults.innerHTML = '';
        finalOutput.textContent = '';
        
        // Show current module info
        currentModuleInfo.classList.remove('hidden');
        
        try {
            // Process input through streaming API for better UX
            await processInputStreaming(text);
        } catch (error) {
            console.error('Error processing input:', error);
            alert('An error occurred while processing your input. Please try again.');
            
            // Hide loading state
            loadingContainer.classList.add('hidden');
            initialMessage.classList.remove('hidden');
        }
    }
    
    // Process input through streaming API
    async function processInputStreaming(text) {
        // Start with the first module
        const response = await fetch('/stream_process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        });
        
        if (!response.ok) {
            throw new Error('API request failed');
        }
        
        const data = await response.json();
        
        // Display input
        resultInput.textContent = text;
        
        // Process first module
        await displayModuleResult(data.module, data.result, 0);
        
        // Continue with remaining modules
        let previousOutput = data.result;
        let currentIndex = 1;
        
        for (const nextModule of data.next_modules) {
            const continueResponse = await fetch('/continue_process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text,
                    module: nextModule,
                    previous_output: previousOutput
                })
            });
            
            if (!continueResponse.ok) {
                throw new Error('API request failed');
            }
            
            const continueData = await continueResponse.json();
            
            // Display this module's result
            await displayModuleResult(nextModule, continueData.result, currentIndex);
            
            // Update for next iteration
            previousOutput = continueData.result;
            currentIndex++;
            
            // Check if complete
            if (continueData.complete) {
                // Display final output
                displayFinalOutput(previousOutput);
                break;
            }
        }
        
        // Show results container
        loadingContainer.classList.add('hidden');
        resultsContainer.classList.remove('hidden');
    }
    
    // Display a single module result with animation
    function displayModuleResult(moduleId, result, index) {
        return new Promise(resolve => {
            // Find module info
            const module = brainModules.find(m => m.id === moduleId);
            if (!module) {
                console.error('Module not found:', moduleId);
                resolve();
                return;
            }
            
            // Update progress
            const progress = ((index + 1) / brainModules.length) * 100;
            processingProgress.style.width = `${progress}%`;
            
            // Show current module info
            currentModuleName.textContent = `${module.emoji} ${module.name}`;
            currentModuleDescription.textContent = module.description;
            
            // Highlight current brain region
            resetBrainRegions();
            const region = document.getElementById(`${moduleId}-region`);
            if (region) {
                region.classList.add('active-processing');
            }
            
            // Activate neural connection if not the last module
            if (index < brainModules.length - 1) {
                const connection = document.getElementById(`connection-${index}-${index+1}`);
                if (connection) {
                    connection.classList.add('active');
                }
            }
            
            // Create module result element
            const moduleElement = document.createElement('div');
            moduleElement.className = 'module-result';
            moduleElement.setAttribute('data-module', moduleId);
            moduleElement.innerHTML = `
                <div class="module-header cursor-pointer">
                    <span class="module-emoji">${module.emoji}</span>
                    <span class="font-semibold">${module.name}</span>
                    <span class="module-arrow ml-auto">
                        <i class="fas fa-chevron-down"></i>
                    </span>
                </div>
                <div class="module-content">
                    <p>${result}</p>
                </div>
            `;
            
            // Add to module results container
            moduleResults.appendChild(moduleElement);
            
            // Add event listener for expanding/collapsing
            const header = moduleElement.querySelector('.module-header');
            header.addEventListener('click', () => {
                moduleElement.classList.toggle('expanded');
            });
            
            // Automatically expand first result
            if (index === 0) {
                setTimeout(() => {
                    moduleElement.classList.add('expanded');
                }, 500);
            }
            
            // Add slight delay for animation
            setTimeout(() => {
                // Update neural connections
                updateNeuralConnections();
                resolve();
            }, 800);
        });
    }
    
    // Reset all brain region highlights
    function resetBrainRegions() {
        document.querySelectorAll('.brain-region').forEach(region => {
            region.classList.remove('active-processing');
        });
        
        document.querySelectorAll('.neural-connection').forEach(connection => {
            connection.classList.remove('active');
        });
    }
    
    // Display final integrated output
    function displayFinalOutput(output) {
        finalOutput.textContent = output;
        
        // Reset brain region highlights
        resetBrainRegions();
        
        // Hide current module info
        currentModuleInfo.classList.add('hidden');
        
        // Scroll to final output
        finalOutput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});

