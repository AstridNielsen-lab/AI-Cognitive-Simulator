import requests
import json
from . import get_module_emoji, get_module_description, format_module_response

class CognitiveChain:
    """
    Manages the chain of cognitive processing through different brain modules.
    Each module simulates a different part of the brain and its function.
    """
    
    def __init__(self):
        """Initialize the cognitive chain with the sequence of brain modules."""
        self.modules = [
            "prefrontal_cortex",
            "amygdala",
            "hippocampus",
            "thalamus",
            "sensory_cortex",
            "auditory_cortex",
            "visual_cortex",
            "motor_cortex",
            "hypothalamus",
            "cerebellum",
            "brain_stem"
        ]
        
        # Initialize the prompt templates for each module
        self._init_prompt_templates()
    
    def _init_prompt_templates(self):
        """Initialize the prompt templates for each brain module."""
        self.prompt_templates = {
            "prefrontal_cortex": """You are a simulation of the part of the brain called: Prefrontal Cortex {emoji}. 
Your function is to plan, make decisions and analyze social behavior. 
Receive the following phrase and begin the initial analysis from the perspective of this brain function: 
"{input_text}"
Give a reflective interpretation based on decisions and planning, and send the result to the next simulated brain function.""",

            "amygdala": """You are a simulation of the part of the brain called: Amygdala {emoji}.
Your function is to process emotions such as fear, pleasure, and anxiety.
Continuing from the previous brain module's analysis:
"{previous_output}"
Now analyze the emotional components in this context: "{input_text}"
Provide an emotional interpretation and send the result to the next simulated brain function.""",

            "hippocampus": """You are a simulation of the part of the brain called: Hippocampus {emoji}.
Your function is to process memories and establish contextual relationships.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now relate this to memories and experiences: "{input_text}"
Provide a contextual interpretation based on memory and send the result to the next simulated brain function.""",

            "thalamus": """You are a simulation of the part of the brain called: Thalamus {emoji}.
Your function is to relay and integrate information from different parts of the brain.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now centralize and distribute this information: "{input_text}"
Provide an integrated interpretation and send the result to the next simulated brain function.""",

            "sensory_cortex": """You are a simulation of the part of the brain called: Sensory Cortex {emoji}.
Your function is to process physical sensations like touch, temperature, and pain.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now transform this into sensory experiences: "{input_text}"
Provide a tactile and sensory interpretation and send the result to the next simulated brain function.""",

            "auditory_cortex": """You are a simulation of the part of the brain called: Auditory Cortex {emoji}.
Your function is to process sounds and auditory information.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now interpret this as if it were heard - focus on tone, emphasis, and sound: "{input_text}"
Provide an auditory interpretation and send the result to the next simulated brain function.""",

            "visual_cortex": """You are a simulation of the part of the brain called: Visual Cortex {emoji}.
Your function is to process visual information and create mental images.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now create mental images based on this content: "{input_text}"
Provide a visual interpretation and send the result to the next simulated brain function.""",

            "motor_cortex": """You are a simulation of the part of the brain called: Motor Cortex {emoji}.
Your function is to plan and execute movements and actions.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now determine possible actions implied by this: "{input_text}"
Provide an action-oriented interpretation and send the result to the next simulated brain function.""",

            "hypothalamus": """You are a simulation of the part of the brain called: Hypothalamus {emoji}.
Your function is to regulate physiological processes and instinctive behaviors.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now generate physiological and instinctive reactions: "{input_text}"
Provide an interpretation based on basic drives and physical states and send the result to the next simulated brain function.""",

            "cerebellum": """You are a simulation of the part of the brain called: Cerebellum {emoji}.
Your function is to coordinate movements and maintain balance.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now refine and balance this conclusion: "{input_text}"
Provide a well-coordinated interpretation and send the result to the next simulated brain function.""",

            "brain_stem": """You are a simulation of the part of the brain called: Brain Stem {emoji}.
Your function is to control vital functions and basic survival.
Continuing from the previous brain modules' analyses:
"{previous_output}"
Now finalize this as a vital response - a fundamental action to take: "{input_text}"
Provide a final, survival-oriented conclusion that integrates all the previous processing."""
        }
    
    def get_module_prompt(self, module, input_text, previous_output=""):
        """Get the prompt for a specific brain module."""
        if module not in self.prompt_templates:
            raise ValueError(f"Unknown module: {module}")
            
        emoji = get_module_emoji(module)
        return self.prompt_templates[module].format(
            emoji=emoji,
            input_text=input_text,
            previous_output=previous_output
        )
    
    def process_module(self, module, input_text, previous_output, api_url, api_key):
        """Process a single module in the cognitive chain."""
        prompt = self.get_module_prompt(module, input_text, previous_output)
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        response = requests.post(
            f"{api_url}?key={api_key}",
            json=data,
            headers=headers
        )
        
        if response.status_code != 200:
            return f"Error: {response.text}"
        
        response_data = response.json()
        if 'candidates' not in response_data or not response_data['candidates']:
            return "No response from API"
            
        output = response_data['candidates'][0]['content']['parts'][0]['text']
        return output
    
    def process(self, input_text, api_url, api_key):
        """Process the input through the entire cognitive chain."""
        results = []
        previous_output = ""
        
        for module in self.modules:
            module_output = self.process_module(
                module, 
                input_text, 
                previous_output, 
                api_url, 
                api_key
            )
            
            results.append({
                "module": module,
                "emoji": get_module_emoji(module),
                "description": get_module_description(module),
                "input": input_text,
                "previous": previous_output,
                "output": module_output
            })
            
            previous_output = module_output
        
        # Generate a final integrated response
        final_prompt = f"""You are a cognitive AI that has analyzed the following input through 11 simulated brain functions: "{input_text}"
After all the processing through different brain areas, synthesize a final, human-like cognitive conclusion that integrates all perspectives.
Make this response sound like a complete thought process that a human might have.
Previous processing: {previous_output}"""
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": final_prompt
                }]
            }]
        }
        
        response = requests.post(
            f"{api_url}?key={api_key}",
            json=data,
            headers=headers
        )
        
        final_output = "Could not generate final response."
        if response.status_code == 200:
            response_data = response.json()
            if 'candidates' in response_data and response_data['candidates']:
                final_output = response_data['candidates'][0]['content']['parts'][0]['text']
        
        return {
            "input": input_text,
            "module_results": results,
            "final_output": final_output
        }

