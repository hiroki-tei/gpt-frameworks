"""
AgentCore Runtime Entrypoint

This is the main entrypoint for the AWS Bedrock AgentCore runtime.
It follows the official AgentCore pattern using BedrockAgentCoreApp.
"""

import sys
import os
import logging

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from examples.weather_agent import invoke as weather_invoke

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Debug output to confirm module is loading
print("=== INVOKE.PY MODULE LOADING ===")
logger.info("=== INVOKE.PY MODULE LOADING ===")
print(f"Module name: {__name__}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print(f"Available files: {os.listdir('.')}")
logger.info(f"Module name: {__name__}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python path: {sys.path}")
logger.info(f"Available files: {os.listdir('.')}")

# Create the AgentCore application
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """
    Main entrypoint for AgentCore runtime
    
    Args:
        payload: Request payload from AgentCore
        
    Returns:
        Response from the weather agent
    """
    logger.info("=== AgentCore Weather Demo Handler Invoked ===")
    logger.info(f"Received payload: {payload}")
    
    try:
        # Extract the user input from the payload
        user_input = payload.get("prompt", payload.get("input", ""))
        
        if not user_input:
            return {
                "error": "No input provided. Please provide a 'prompt' or 'input' field."
            }
        
        logger.info(f"Processing weather query: {user_input}")
        
        # Use the weather agent function
        result = weather_invoke(user_input)
        
        logger.info("Weather query processed successfully")
        
        # Return the result in the expected format
        return {
            "response": result,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return {
            "error": f"Failed to process weather query: {str(e)}",
            "status": "error"
        }

if __name__ == "__main__":
    logger.info("Starting AgentCore Weather Demo Application")
    logger.info("Running as main module - starting BedrockAgentCoreApp")
    app.run()
else:
    logger.info("Module imported - BedrockAgentCoreApp configured for entrypoint")