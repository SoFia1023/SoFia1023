import json
import os
import time
import logging
from typing import Dict, Any, Optional, Union

import requests
from dotenv import load_dotenv

# Import secure API key management and logging utilities
from core.security import get_api_key
from core.logging_utils import log_api_request, log_exception

# Get a logger for this module
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def call_openai_api(prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
    """
    Call the OpenAI API for text generation.
    
    Args:
        prompt (str): The prompt to send to the API
        max_tokens (int): Maximum number of tokens to generate
        
    Returns:
        dict: Response from the API or error message
    """
    # Log the API call attempt
    logger.info(f"Calling OpenAI API with prompt length: {len(prompt)} chars")
    
    # Get API key securely
    api_key = get_api_key('OPENAI_API_KEY')
    
    if not api_key:
        error_msg = 'API key not found. Please set OPENAI_API_KEY in environment variables.'
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg
        }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        'model': 'gpt-3.5-turbo-instruct',
        'prompt': prompt,
        'max_tokens': max_tokens,
        'temperature': 0.7
    }
    
    start_time = time.time()
    status_code = None
    error_message = None
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers=headers,
            data=json.dumps(data),
            timeout=10
        )
        
        status_code = response.status_code
        response_time = time.time() - start_time
        
        # Log the API request with details
        log_api_request(
            logger=logger,
            service_name="OpenAI",
            endpoint="/v1/completions",
            method="POST",
            status_code=status_code,
            response_time=response_time,
            request_data={
                'model': data['model'],
                'max_tokens': data['max_tokens'],
                'temperature': data['temperature'],
                'prompt_length': len(prompt)
            }
        )
        
        if status_code == 200:
            logger.debug("OpenAI API request successful")
            return {
                'success': True,
                'data': response.json()
            }
        else:
            error_message = f'API Error: {status_code} - {response.text}'
            logger.warning(f"OpenAI API request failed: {error_message}")
            return {
                'success': False,
                'error': f'API Error: {status_code}',
                'message': response.text
            }
    except Exception as e:
        response_time = time.time() - start_time
        error_message = str(e)
        
        # Log the exception with context
        log_exception(
            logger=logger,
            exc=e,
            message="OpenAI API request failed with exception",
            extra={
                'service': 'OpenAI',
                'endpoint': '/v1/completions',
                'response_time': f"{response_time:.3f}s",
                'prompt_length': len(prompt)
            }
        )
        
        return {
            'success': False,
            'error': f'Request failed: {error_message}'
        }

def call_huggingface_api(prompt: str, model: str = "google/flan-t5-small") -> Dict[str, Any]:
    """
    Call the Hugging Face Inference API.
    
    Args:
        prompt (str): The prompt to send to the API
        model (str): The model to use for inference
        
    Returns:
        dict: Response from the API or error message
    """
    # Log the API call attempt
    logger.info(f"Calling Hugging Face API with model: {model}")
    
    # Get API key securely
    api_key = get_api_key('HUGGINGFACE_API_KEY')
    
    if not api_key:
        error_msg = 'API key not found. Please set HUGGINGFACE_API_KEY in environment variables.'
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg
        }
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'inputs': prompt,
        'options': {
            'wait_for_model': True
        }
    }
    
    start_time = time.time()
    status_code = None
    error_message = None
    endpoint = f'/models/{model}'
    
    try:
        response = requests.post(
            f'https://api-inference.huggingface.co/models/{model}',
            headers=headers,
            data=json.dumps(data),
            timeout=10
        )
        
        status_code = response.status_code
        response_time = time.time() - start_time
        
        # Log the API request with details
        log_api_request(
            logger=logger,
            service_name="HuggingFace",
            endpoint=endpoint,
            method="POST",
            status_code=status_code,
            response_time=response_time,
            request_data={
                'model': model,
                'wait_for_model': True,
                'prompt_length': len(prompt)
            }
        )
        
        if status_code == 200:
            logger.debug(f"Hugging Face API request successful for model: {model}")
            return {
                'success': True,
                'data': response.json()
            }
        else:
            error_message = f'API Error: {status_code} - {response.text}'
            logger.warning(f"Hugging Face API request failed: {error_message}")
            return {
                'success': False,
                'error': f'API Error: {status_code}',
                'message': response.text
            }
    except Exception as e:
        response_time = time.time() - start_time
        error_message = str(e)
        
        # Log the exception with context
        log_exception(
            logger=logger,
            exc=e,
            message=f"Hugging Face API request failed with exception for model: {model}",
            extra={
                'service': 'HuggingFace',
                'endpoint': endpoint,
                'model': model,
                'response_time': f"{response_time:.3f}s",
                'prompt_length': len(prompt)
            }
        )
        
        return {
            'success': False,
            'error': f'Request failed: {error_message}'
        }