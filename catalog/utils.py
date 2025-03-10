"""
Utility functions for the catalog app.
"""
import json
import requests
import os
import time
from django.http import HttpResponse
from django.conf import settings
import random

# Get API keys from environment variables (or set defaults for demo)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')

class AIService:
    """Service class for handling AI API interactions."""
    
    @staticmethod
    def call_openai_api(prompt, model="gpt-3.5-turbo"):
        """
        Call OpenAI API with the provided prompt.
        
        Args:
            prompt (str): The message to send to the API
            model (str): The OpenAI model name to use
            
        Returns:
            dict: Response with success status and data/error
        """
        # If no API key set, return a simulated response
        if not OPENAI_API_KEY:
            return AIService.simulate_ai_response("openai", prompt)
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            response_data = response.json()
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response_data["choices"][0]["message"]["content"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response_data.get('error', {}).get('message', 'Unknown error')}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception: {str(e)}"
            }
    
    @staticmethod
    def call_huggingface_api(prompt, model="google/flan-t5-base"):
        """
        Call Hugging Face API with the provided prompt.
        
        Args:
            prompt (str): The message to send to the API
            model (str): The Hugging Face model name to use
            
        Returns:
            dict: Response with success status and data/error
        """
        # If no API key set, return a simulated response
        if not HUGGINGFACE_API_KEY:
            return AIService.simulate_ai_response("huggingface", prompt)
        
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
            }
            
            payload = {
                "inputs": prompt,
            }
            
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()[0]["generated_text"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception: {str(e)}"
            }
    
    @staticmethod
    def simulate_ai_response(service_type, prompt):
        """
        Simulate an AI response for demo purposes when API keys aren't available.
        
        Args:
            service_type (str): The type of AI service ('openai' or 'huggingface')
            prompt (str): The user's prompt
            
        Returns:
            dict: Simulated response with success status and data
        """
        # Add a slight delay to simulate API call
        time.sleep(1)
        
        # Generic responses based on prompt keywords
        responses = [
            "I'm a simulated AI response since no API key was provided. Your question seems interesting!",
            "This is a placeholder response. To get real AI responses, please configure the API keys.",
            "I'm a demo response. In production, this would connect to the actual AI service.",
            "Thanks for your prompt! This is a simulated response for testing purposes.",
            "I understand you're asking about something, but I'm just a simulated response."
        ]
        
        # Try to make responses slightly contextual based on prompt
        if "hello" in prompt.lower() or "hi" in prompt.lower():
            response = "Hello! I'm a simulated AI response. How can I help you today?"
        elif "help" in prompt.lower():
            response = "I'd be happy to help! However, I'm currently running in simulation mode without API access."
        elif "weather" in prompt.lower():
            response = "I can't check the weather right now as I'm running in simulation mode."
        elif "code" in prompt.lower() or "programming" in prompt.lower():
            response = "Here's a simulated response about coding. In production, I could help with actual programming questions."
        elif "?" in prompt:
            response = "That's an interesting question! In production mode with API keys configured, I could provide a real answer."
        else:
            # Pick a random generic response
            response = random.choice(responses)
            
        return {
            "success": True,
            "data": response + f"\n\n[Note: This is a simulated {service_type} response]"
        }
    
    @staticmethod
    def send_to_ai_service(prompt, service_config):
        """
        Route the prompt to the appropriate AI service based on configuration.
        
        Args:
            prompt (str): The user's message
            service_config (dict): Configuration for the AI service
            
        Returns:
            dict: Response with success status and data/error
        """
        service_type = service_config.get('api_type', 'none')
        model = service_config.get('api_model', '')
        
        if service_type == 'openai':
            # Use default model if none specified
            if not model:
                model = "gpt-3.5-turbo"
            return AIService.call_openai_api(prompt, model)
            
        elif service_type == 'huggingface':
            # Use default model if none specified
            if not model:
                model = "google/flan-t5-base"
            return AIService.call_huggingface_api(prompt, model)
            
        elif service_type == 'custom':
            # For custom integrations, we'd implement specific logic here
            # This is a placeholder for future custom integrations
            return {
                "success": False,
                "error": "Custom integrations are not yet implemented"
            }
            
        else:
            # For 'none' or any other type, return simulated response
            return AIService.simulate_ai_response("generic", prompt)

# Legacy function wrappers for backward compatibility
def call_openai_api(prompt, model="gpt-3.5-turbo"):
    return AIService.call_openai_api(prompt, model)

def call_huggingface_api(prompt, model="google/flan-t5-base"):
    return AIService.call_huggingface_api(prompt, model)

def simulate_ai_response(service_type, prompt):
    return AIService.simulate_ai_response(service_type, prompt)

def send_to_ai_service(prompt, service_config):
    return AIService.send_to_ai_service(prompt, service_config)

# Utility function for formatting conversation downloads
def format_conversation_for_download(conversation, format_type='json'):
    """
    Format a conversation for download in the specified format.
    
    Args:
        conversation: The Conversation object to format
        format_type (str): The format type ('json', 'txt', or 'csv')
        
    Returns:
        tuple: (formatted_content, content_type, file_extension)
    """
    messages = conversation.get_messages()
    
    if format_type == 'json':
        # Use the built-in to_json method
        content = conversation.to_json()
        content_type = 'application/json'
        file_ext = 'json'
        
    elif format_type == 'txt':
        # Simple text format
        lines = [f"Conversation: {conversation.title}"]
        lines.append(f"AI Tool: {conversation.ai_tool.name}")
        lines.append(f"Date: {conversation.created_at.strftime('%Y-%m-%d %H:%M')}")
        lines.append("-" * 40)
        
        for msg in messages:
            sender = "You" if msg.is_user else conversation.ai_tool.name
            timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M')
            lines.append(f"{sender} ({timestamp}):")
            lines.append(msg.content)
            lines.append("")
            
        content = "\n".join(lines)
        content_type = 'text/plain'
        file_ext = 'txt'
        
    elif format_type == 'csv':
        # CSV format
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Timestamp', 'Sender', 'Message'])
        
        for msg in messages:
            sender = "User" if msg.is_user else conversation.ai_tool.name
            writer.writerow([
                msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                sender,
                msg.content
            ])
            
        content = output.getvalue()
        content_type = 'text/csv'
        file_ext = 'csv'
        
    else:
        # Default to JSON if format not recognized
        content = conversation.to_json()
        content_type = 'application/json'
        file_ext = 'json'
        
    return content, content_type, file_ext