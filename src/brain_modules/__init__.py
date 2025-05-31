# Brain Modules Package
"""
This package contains all the brain modules used in the cognitive chain.
Each module simulates a different part of the brain and its function.
"""

# Common utility functions for brain modules

def format_module_response(module_name, response_text):
    """Format the response from a module for display."""
    return {
        "module": module_name,
        "response": response_text.strip()
    }

def get_module_emoji(module_name):
    """Get the emoji for a specific brain module."""
    emoji_map = {
        "prefrontal_cortex": "🧠",
        "amygdala": "😲",
        "hippocampus": "📚",
        "thalamus": "🔄",
        "sensory_cortex": "👐",
        "auditory_cortex": "👂",
        "visual_cortex": "👁️",
        "motor_cortex": "🏃",
        "hypothalamus": "🌡️",
        "cerebellum": "⚖️",
        "brain_stem": "⚡"
    }
    return emoji_map.get(module_name, "🧠")

def get_module_description(module_name):
    """Get the description for a specific brain module."""
    description_map = {
        "prefrontal_cortex": "Planning, decision-making, and social behavior analysis",
        "amygdala": "Emotional processing (fear, pleasure, anxiety)",
        "hippocampus": "Memory and contextual relationships",
        "thalamus": "Information relay and integration",
        "sensory_cortex": "Physical sensations and tactile imagery",
        "auditory_cortex": "Auditory processing and tone interpretation",
        "visual_cortex": "Visual imagery and perception",
        "motor_cortex": "Action planning and movement coordination",
        "hypothalamus": "Physiological and instinctive responses",
        "cerebellum": "Fine-tuning and balance",
        "brain_stem": "Vital responses and basic survival functions"
    }
    return description_map.get(module_name, "Brain processing")

def get_module_color(module_name):
    """Get the color associated with a specific brain module."""
    color_map = {
        "prefrontal_cortex": "#4a5568",  # Blue-gray
        "amygdala": "#e53e3e",  # Red
        "hippocampus": "#805ad5",  # Purple
        "thalamus": "#3182ce",  # Blue
        "sensory_cortex": "#38a169",  # Green
        "auditory_cortex": "#dd6b20",  # Orange
        "visual_cortex": "#d69e2e",  # Yellow
        "motor_cortex": "#319795",  # Teal
        "hypothalamus": "#d53f8c",  # Pink
        "cerebellum": "#718096",  # Gray
        "brain_stem": "#2c5282"   # Dark blue
    }
    return color_map.get(module_name, "#4a5568")

