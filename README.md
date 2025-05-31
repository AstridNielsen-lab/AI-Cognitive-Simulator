# AI Neural Network Cognitive Simulator

![Brain Visualization](https://neurosciencenews.com/files/2023/06/brain-memory-neurosinces.jpg)

## Overview

The AI Neural Network Cognitive Simulator is an interactive web application that demonstrates how artificial intelligence processes information through simulated brain regions. The system takes a user's input phrase and processes it through 11 different simulated brain modules, each representing a distinct cognitive function of the human brain.

This project aims to visualize and explain the complex cognitive processes that might occur in an artificial neural network, inspired by human brain function.

## Features

- **Interactive Brain Visualization**: Watch as your input gets processed through different regions of a simulated brain with real-time animations and visual feedback.

- **11 Simulated Brain Modules**:
  - 🧠 **Prefrontal Cortex**: Planning, decision-making, and social behavior analysis
  - 😲 **Amygdala**: Emotional processing (fear, pleasure, anxiety)
  - 📚 **Hippocampus**: Memory and contextual relationships
  - 🔄 **Thalamus**: Information relay and integration
  - 👐 **Sensory Cortex**: Physical sensations and tactile imagery
  - 👂 **Auditory Cortex**: Auditory processing and tone interpretation
  - 👁️ **Visual Cortex**: Visual imagery and perception
  - 🏃 **Motor Cortex**: Action planning and movement coordination
  - 🌡️ **Hypothalamus**: Physiological and instinctive responses
  - ⚖️ **Cerebellum**: Fine-tuning and balance
  - ⚡ **Brain Stem**: Vital responses and basic survival functions

- **Neural Processing Chain**: Visualize the flow of information between brain regions with animated neural connections.

- **Progressive Analysis**: See how each module builds upon the analyses of previous modules to form a complete cognitive process.

- **Final Integrated Output**: Receive a synthesized, human-like cognitive conclusion that integrates all perspectives.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/AstridNielsen-lab/AI-Cognitive-Simulator.git
   cd AI-Cognitive-Simulator
   ```

2. Install the required packages:
   ```
   pip install flask requests
   ```

3. Set up your API key:
   - The application uses the Google Gemini API. By default, it uses a provided API key for demonstration purposes.
   - For production use, you should replace the API key in `app.py` with your own key from the [Google AI Studio](https://ai.google.dev/).

### Running the Application

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage Guide

1. **Enter a Phrase**: Type any phrase or statement into the input box. This could be a simple statement, a question, or a complex idea.

2. **Process the Input**: Click the "Process Thought" button to start the cognitive simulation.

3. **Watch the Visualization**: Observe as your input is processed through different brain regions, with each region lighting up as it processes the information.

4. **Explore the Results**: Review the detailed analysis from each brain module. Click on each module to expand or collapse its analysis.

5. **Final Output**: Read the final integrated output, which synthesizes all the processing into a human-like cognitive conclusion.

## Technical Details

- **Frontend**: HTML, CSS, JavaScript with Tailwind CSS for styling
- **Backend**: Python with Flask framework
- **AI Processing**: Google Gemini API for neural language processing
- **Visualization**: Custom JavaScript animations and dynamic DOM manipulation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Inspired by neural network architectures and cognitive neuroscience
- Brain visualization based on current understanding of functional neuroanatomy
- Powered by Google's Gemini AI technology

