"""
Utility functions for the interaction app.
"""
import re
from typing import Dict, Any, List, Optional, Union, Pattern
from catalog.models import AITool
from interaction.models import Conversation

def route_message_to_ai_tool(message_content: str) -> Optional[AITool]:
    """
    Analyze message content and route to the most appropriate AI tool based on content patterns.
    
    This function uses regex pattern matching to determine the most appropriate AI tool category
    for the given message content, then returns the most popular tool in that category.
    
    Args:
        message_content (str): The user's message content to analyze
        
    Returns:
        Optional[AITool]: The most appropriate AI tool for handling the message, or None if no tool is found
        
    Example:
        >>> tool = route_message_to_ai_tool("Generate an image of a sunset")
        >>> print(tool.category)
        'Image Generator'
    """
    # Convert to lowercase for case-insensitive matching to ensure consistent pattern matching
    # regardless of the user's capitalization style
    content_lower = message_content.lower()
    
    # Define regex patterns for different AI tool categories
    # Each category has multiple patterns to increase the chance of a correct match
    # The patterns are designed to capture common ways users might request specific types of content
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
    # This serves as our fallback category for general text-based queries
    best_category = 'Text Generator'
    highest_score = 0
    
    # Check each category's patterns against the user message
    # We calculate a score based on how many pattern matches are found
    for category, category_patterns in patterns.items():
        score = 0
        for pattern in category_patterns:
            # Find all instances of the pattern in the message
            # Each match increases the category's score
            matches = re.findall(pattern, content_lower)
            score += len(matches)
        
        # If this category has a higher score than previous categories,
        # update our best match. This ensures we select the most relevant tool.
        if score > highest_score:
            highest_score = score
            best_category = category
    
    # Get the most popular AI tool in the best matching category
    # We sort by popularity to ensure users get the most reliable tool in that category
    ai_tool = AITool.objects.filter(
        category=best_category
    ).order_by('-popularity').first()
    
    # Fallback mechanism #1: If no tool is found in the matched category,
    # default to the most popular Text Generator, which can handle general queries
    if not ai_tool:
        ai_tool = AITool.objects.filter(
            category='Text Generator'
        ).order_by('-popularity').first()
    
    # Fallback mechanism #2: If still no tool is found (database might be empty in that category),
    # select any available AI tool to ensure the user gets a response
    if not ai_tool:
        ai_tool = AITool.objects.all().order_by('-popularity').first()
    
    return ai_tool

# This function has been moved to core.utils to avoid code duplication
