"""
Utility functions for the interaction app.
"""
import json
import re
from io import StringIO
import csv
from django.utils import timezone
from typing import Dict, Any, List, Tuple, Optional, Union, Pattern
from catalog.models import AITool
from interaction.models import Conversation

def route_message_to_ai_tool(message_content: str) -> Optional[AITool]:
    """
    Analyze message content and route to the most appropriate AI tool.
    
    Args:
        message_content (str): The user's message content
        
    Returns:
        Optional[AITool]: The most appropriate AI tool for handling the message, or None if no tool is found
    """
    # Convert to lowercase for case-insensitive matching
    content_lower = message_content.lower()
    
    # Define patterns for different AI tool categories
    patterns = {
        'Image Generator': [
            r'(create|generate|make|draw|design|produce) (a|an|some)? ?(image|picture|photo|illustration|artwork|drawing)',
            r'(image|picture|photo) of',
            r'(visualize|visualise|imagine|envision)',
            r'(render|sketch|paint|illustrate)',
            r'(image|picture|photo|visual) (generation|creation)'
        ],
        'Video Generator': [
            r'(create|generate|make|produce) (a|an|some)? ?(video|animation|clip|movie)',
            r'(video|animation) of',
            r'(animate|animating)',
            r'(video|animation|clip|movie) (generation|creation)'
        ],
        'Code Generator': [
            r'(write|generate|create|code|program|implement|develop) (a|an|some)? ?(code|function|class|method|algorithm|program|script)',
            r'(python|javascript|java|c\+\+|html|css|sql|php|ruby|swift|typescript|go|rust|kotlin)',
            r'(programming|coding|development|software)',
            r'(function|class|method|api|endpoint|algorithm)',
            r'(debug|fix|solve) (this|my|the) (code|bug|error|issue|problem)'
        ],
        'Transcription': [
            r'(transcribe|transcription|convert speech to text|speech-to-text)',
            r'(audio|speech|voice) (to|into) (text|transcript)',
            r'(extract|get|pull) text from (audio|speech|recording)'
        ],
        'Word Processor': [
            r'(summarize|summarise|summary)',
            r'(proofread|edit|revise|check|correct) (my|this|the) (text|document|essay|paper|article|content)',
            r'(grammar|spelling|punctuation) (check|correction)',
            r'(rewrite|rephrase|paraphrase)',
            r'(translate|translation)'
        ]
    }
    
    # Default to Text Generator if no specific patterns match
    best_category = 'Text Generator'
    highest_score = 0
    
    # Check each category's patterns
    for category, category_patterns in patterns.items():
        score = 0
        for pattern in category_patterns:
            matches = re.findall(pattern, content_lower)
            score += len(matches)
        
        # If this category has a higher score, update the best match
        if score > highest_score:
            highest_score = score
            best_category = category
    
    # Get the most popular AI tool in the best matching category
    ai_tool = AITool.objects.filter(
        category=best_category
    ).order_by('-popularity').first()
    
    # Fallback to the most popular Text Generator if no tool found in the matched category
    if not ai_tool:
        ai_tool = AITool.objects.filter(
            category='Text Generator'
        ).order_by('-popularity').first()
    
    # Ultimate fallback to any AI tool if still nothing found
    if not ai_tool:
        ai_tool = AITool.objects.all().order_by('-popularity').first()
    
    return ai_tool

def format_conversation_for_download(conversation: Conversation, format_type: str = 'json') -> Tuple[str, str, str]:
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
