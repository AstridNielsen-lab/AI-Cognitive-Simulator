from flask import Flask, render_template, request, jsonify
import requests
import json
import time
import os
import sys
import importlib.util

# Add the parent directory to the Python path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the CognitiveChain class
from src.brain_modules.cognitive_chain import CognitiveChain

# Initialize Flask app
app = Flask(__name__, static_folder="../static", template_folder="../templates")

# Initialize the cognitive chain
cognitive_chain = CognitiveChain()

# Gemini API configuration - use environment variable if available
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAZAG4wnbcfKWJ_D4VyiJyf0Y3VgUESau8")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Process the user input through the cognitive chain."""
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'No text provided'}), 400
        
    user_input = request.json['text']
    
    # Process the input through the cognitive chain
    results = cognitive_chain.process(user_input, API_URL, API_KEY)
    
    return jsonify(results)

@app.route('/brain_module', methods=['POST'])
def brain_module():
    """Process text through a specific brain module."""
    if not request.json or 'text' not in request.json or 'module' not in request.json:
        return jsonify({'error': 'Required fields missing'}), 400
        
    text = request.json['text']
    module = request.json['module']
    previous_output = request.json.get('previous_output', '')
    
    # Call Gemini API for this specific module
    headers = {
        "Content-Type": "application/json"
    }
    
    # Construct the prompt based on the module
    prompt = cognitive_chain.get_module_prompt(module, text, previous_output)
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(
        f"{API_URL}?key={API_KEY}",
        json=data,
        headers=headers
    )
    
    if response.status_code != 200:
        return jsonify({'error': 'API request failed', 'details': response.text}), 500
    
    response_data = response.json()
    if 'candidates' not in response_data or not response_data['candidates']:
        return jsonify({'error': 'No response from API'}), 500
        
    output = response_data['candidates'][0]['content']['parts'][0]['text']
    
    return jsonify({
        'module': module,
        'input': text,
        'output': output
    })

@app.route('/stream_process', methods=['POST'])
def stream_process():
    """Process each module one by one and return results as they complete."""
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'No text provided'}), 400
        
    user_input = request.json['text']
    
    # Get the first module result to start the chain
    first_module = cognitive_chain.modules[0]
    result = call_module_api(first_module, user_input)
    
    return jsonify({
        'module': first_module,
        'result': result,
        'next_modules': cognitive_chain.modules[1:]
    })

def call_module_api(module, text, previous_output=""):
    """Call the API for a specific module."""
    headers = {
        "Content-Type": "application/json"
    }
    
    prompt = cognitive_chain.get_module_prompt(module, text, previous_output)
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(
        f"{API_URL}?key={API_KEY}",
        json=data,
        headers=headers
    )
    
    if response.status_code != 200:
        return f"Error: {response.text}"
    
    response_data = response.json()
    if 'candidates' not in response_data or not response_data['candidates']:
        return "No response from API"
        
    return response_data['candidates'][0]['content']['parts'][0]['text']

@app.route('/continue_process', methods=['POST'])
def continue_process():
    """Continue processing the next module in the chain."""
    if not request.json or 'text' not in request.json or 'module' not in request.json or 'previous_output' not in request.json:
        return jsonify({'error': 'Required fields missing'}), 400
        
    user_input = request.json['text']
    current_module = request.json['module']
    previous_output = request.json['previous_output']
    
    # Find the current module index
    try:
        module_index = cognitive_chain.modules.index(current_module)
    except ValueError:
        return jsonify({'error': 'Invalid module'}), 400
        
    # Check if we have more modules to process
    if module_index >= len(cognitive_chain.modules) - 1:
        return jsonify({
            'complete': True,
            'final_output': previous_output
        })
    
    # Get the next module
    next_module = cognitive_chain.modules[module_index + 1]
    
    # Process the next module
    result = call_module_api(next_module, user_input, previous_output)
    
    # Determine if there are more modules
    has_next = module_index + 1 < len(cognitive_chain.modules) - 1
    next_next_module = cognitive_chain.modules[module_index + 2] if has_next else None
    
    return jsonify({
        'module': next_module,
        'result': result,
        'next_module': next_next_module,
        'complete': not has_next
    })

# For local development
if __name__ == '__main__':
    app.run(debug=True)

# For Vercel serverless function
app = app

