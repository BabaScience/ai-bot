"""
Module for interacting with Ollama LLM service.
"""

import asyncio
import logging
import ollama
import time
import os
from typing import Dict, Any, Optional, List
import requests
import concurrent.futures

logger = logging.getLogger(__name__)

# Create a thread pool executor to use for sync operations
# Limit max workers to avoid overloading the system
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)

# Get Ollama host from environment or use default
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'localhost')
OLLAMA_PORT = os.environ.get('OLLAMA_PORT', '11434')
OLLAMA_BASE_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

# Configure Ollama client
ollama.host = OLLAMA_BASE_URL
logger.info(f"Configured Ollama client to use: {OLLAMA_BASE_URL}")

class OllamaConnector:
    """
    Connector class for the Ollama LLM service.
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialize Ollama connector with the specified model.
        
        Args:
            model_name (str): Name of the model to use (default: "llama3.2")
        """
        self.model_name = model_name
        logger.info(f"Initialized Ollama connector with model: {model_name}")
        logger.info(f"Using Ollama at: {OLLAMA_BASE_URL}")
        
        # Try to check connection to Ollama service
        try:
            # Use a minimal valid request to check if Ollama is running
            # We'll use a direct request instead of using asyncio here
            response = requests.get(f"{OLLAMA_BASE_URL}/api/version", timeout=5)
            if response.status_code == 200:
                logger.info(f"Successfully connected to Ollama service: {response.json()}")
            else:
                logger.warning(f"Ollama service responded with status code: {response.status_code}")
        except Exception as e:
            logger.warning(f"Could not verify Ollama service: {str(e)}. Some commands may not work until Ollama is running.")
        
    async def _run_in_executor(self, func, *args, **kwargs):
        """
        Run a synchronous function in the thread pool executor.
        
        This helper method ensures consistent handling of thread pool execution.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            thread_pool,
            lambda: func(*args, **kwargs)
        )
        
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from the LLM based on the given prompt.
        
        Args:
            prompt (str): The user prompt to send to the LLM
            system_prompt (Optional[str]): Optional system prompt to guide model behavior
            
        Returns:
            str: The generated response
        """
        try:
            # Create message format for ollama.chat() - as per 0.4.x API
            messages = [{"role": "user", "content": prompt}]
            
            # Add system prompt if provided
            if system_prompt:
                messages.insert(0, {"role": "system", "content": system_prompt})
            
            # Define the function to call Ollama    
            def call_ollama():
                return ollama.chat(
                    model=self.model_name,
                    messages=messages,
                    stream=False
                )
                
            # Use the executor to run the ollama.chat in a separate thread
            response = await self._run_in_executor(call_ollama)
            
            if response and "message" in response:
                return response["message"]["content"]
            else:
                logger.error(f"Unexpected response format: {response}")
                return "Sorry, I had trouble generating a response. Please try again."
                
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {str(e)}")
            return f"Error: {str(e)}"
            
    async def get_available_models(self) -> List[str]:
        """
        Get a list of available models from Ollama.
        
        Returns:
            List[str]: List of available model names
        """
        try:
            # The ollama.list API returns the list of models differently in newer versions
            models_response = await self._run_in_executor(ollama.list)
            
            logger.info(f"Raw models response: {models_response}")
            
            # Handle different response formats based on the Ollama API version
            if isinstance(models_response, dict):
                if "models" in models_response:
                    # Format for older versions
                    return [model["name"] for model in models_response["models"]]
                else:
                    # Some versions return a different format
                    return [model["name"] for model in models_response.get("models", [])]
            elif isinstance(models_response, list):
                # Format for newer versions (0.4.x+)
                return [model["name"] for model in models_response]
            else:
                logger.error(f"Unexpected response format: {models_response}")
                return []
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []

    async def check_ollama_running(self) -> bool:
        """
        Check if Ollama service is running and accessible.
        
        Returns:
            bool: True if Ollama is running, False otherwise
        """
        try:
            # Define the function to make the request
            def make_request():
                return requests.get(f"{OLLAMA_BASE_URL}/api/version", timeout=5)
                
            # Use direct HTTP request to Ollama's API
            response = await self._run_in_executor(make_request)
            
            if response.status_code == 200:
                logger.info(f"Ollama service is running: {response.json()}")
                return True
            else:
                logger.error(f"Ollama service returned status code: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Ollama service check failed: {str(e)}")
            return False 