import json
import os
import random
from django.core.management.base import BaseCommand
from catalog.models import AITool
from django.conf import settings
from django.core.files.base import ContentFile
import requests
from io import BytesIO
from PIL import Image
import uuid

class Command(BaseCommand):
    help = 'Populates the database with AI tools'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing AI tools before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing AI tools...')
            AITool.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared existing AI tools'))

        # List of AI tools with their details
        ai_tools = [
            {
                'name': 'ChatGPT',
                'provider': 'OpenAI',
                'endpoint': 'https://chat.openai.com/',
                'category': 'Text Generator',
                'description': 'ChatGPT is an AI-powered chatbot developed by OpenAI, based on the GPT (Generative Pre-trained Transformer) language models. It can engage in conversational dialogue and provide responses that can appear surprisingly human.',
                'popularity': 95,
                'api_type': 'openai',
                'api_model': 'gpt-4',
                'api_endpoint': 'https://api.openai.com/v1/chat/completions',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png',
                'is_featured': True
            },
            {
                'name': 'DALL-E',
                'provider': 'OpenAI',
                'endpoint': 'https://labs.openai.com/',
                'category': 'Image Generator',
                'description': 'DALL-E is an AI system developed by OpenAI that can create realistic images and art from a description in natural language. The model can create anthropomorphized versions of animals and objects, combine unrelated concepts in plausible ways, and apply transformations to existing images.',
                'popularity': 88,
                'api_type': 'openai',
                'api_model': 'dall-e-3',
                'api_endpoint': 'https://api.openai.com/v1/images/generations',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/DALL-E_Logo.png/640px-DALL-E_Logo.png',
                'is_featured': True
            },
            {
                'name': 'Midjourney',
                'provider': 'Midjourney, Inc.',
                'endpoint': 'https://www.midjourney.com/',
                'category': 'Image Generator',
                'description': 'Midjourney is an AI program that generates images from textual descriptions, similar to OpenAI\'s DALL-E and Stable Diffusion. It is known for its artistic style and high-quality image generation capabilities.',
                'popularity': 85,
                'api_type': 'custom',
                'api_model': 'midjourney-v5',
                'api_endpoint': 'https://api.midjourney.com/v1/generation',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.png',
                'is_featured': False
            },
            {
                'name': 'Stable Diffusion',
                'provider': 'Stability AI',
                'endpoint': 'https://stability.ai/',
                'category': 'Image Generator',
                'description': 'Stable Diffusion is a deep learning, text-to-image model released in 2022. It is primarily used to generate detailed images conditioned on text descriptions, though it can also be applied to other tasks such as inpainting, outpainting, and generating image-to-image translations guided by a text prompt.',
                'popularity': 82,
                'api_type': 'huggingface',
                'api_model': 'stabilityai/stable-diffusion-xl-base-1.0',
                'api_endpoint': 'https://api.stability.ai/v1/generation',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Stable_Diffusion_logo.png/640px-Stable_Diffusion_logo.png',
                'is_featured': False
            },
            {
                'name': 'Claude',
                'provider': 'Anthropic',
                'endpoint': 'https://claude.ai/',
                'category': 'Text Generator',
                'description': 'Claude is an AI assistant created by Anthropic to be helpful, harmless, and honest. It excels at thoughtful dialogue and creative content generation with nuanced understanding and careful responses.',
                'popularity': 80,
                'api_type': 'custom',
                'api_model': 'claude-3-opus',
                'api_endpoint': 'https://api.anthropic.com/v1/messages',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Anthropic_Logo.png/640px-Anthropic_Logo.png',
                'is_featured': False
            },
            {
                'name': 'Gemini',
                'provider': 'Google',
                'endpoint': 'https://gemini.google.com/',
                'category': 'Text Generator',
                'description': 'Gemini is Google\'s largest and most capable AI model, designed to be multimodal, which means it can understand and combine different types of information including text, code, audio, image, and video.',
                'popularity': 78,
                'api_type': 'custom',
                'api_model': 'gemini-pro',
                'api_endpoint': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
                'image_url': 'https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini_1.width-1300.format-webp.webp',
                'is_featured': False
            },
            {
                'name': 'Whisper',
                'provider': 'OpenAI',
                'endpoint': 'https://platform.openai.com/docs/guides/speech-to-text',
                'category': 'Transcription',
                'description': 'Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. It is designed to transcribe speech in multiple languages and translate it to English.',
                'popularity': 75,
                'api_type': 'openai',
                'api_model': 'whisper-1',
                'api_endpoint': 'https://api.openai.com/v1/audio/transcriptions',
                'image_url': 'https://cdn.openai.com/whisper/draft-20220919a/asr-summary-of-model-architecture-light.svg',
                'is_featured': False
            },
            {
                'name': 'Copilot',
                'provider': 'GitHub',
                'endpoint': 'https://github.com/features/copilot',
                'category': 'Code Generator',
                'description': 'GitHub Copilot is an AI pair programmer that offers autocomplete-style suggestions as you code. It helps you write code faster and with less work by suggesting whole lines or entire functions based on the context of what you\'re working on.',
                'popularity': 85,
                'api_type': 'custom',
                'api_model': 'copilot',
                'api_endpoint': 'https://api.github.com/copilot/suggestions',
                'image_url': 'https://github.blog/wp-content/uploads/2022/06/GitHub-Copilot-GA_banner.png',
                'is_featured': False
            },
            {
                'name': 'Jasper',
                'provider': 'Jasper AI',
                'endpoint': 'https://www.jasper.ai/',
                'category': 'Word Processor',
                'description': 'Jasper is an AI content platform that helps teams create high-quality content faster. It can generate blog posts, social media content, marketing copy, and more based on your inputs and brand guidelines.',
                'popularity': 70,
                'api_type': 'custom',
                'api_model': 'jasper-v2',
                'api_endpoint': 'https://api.jasper.ai/v1/content',
                'image_url': 'https://assets-global.website-files.com/60e5f2de011b86acebc30db7/64b7a3e6e6c1a2e7f9c6c447_Jasper-Wordmark-Black.svg',
                'is_featured': False
            },
            {
                'name': 'Grammarly',
                'provider': 'Grammarly, Inc.',
                'endpoint': 'https://www.grammarly.com/',
                'category': 'Word Processor',
                'description': 'Grammarly is an AI-powered writing assistant that helps users improve their writing by checking for grammar, spelling, punctuation, clarity, engagement, and delivery mistakes. It offers suggestions to make writing clear and effective.',
                'popularity': 88,
                'api_type': 'custom',
                'api_model': 'grammarly-premium',
                'api_endpoint': 'https://api.grammarly.com/v1/check',
                'image_url': 'https://static.grammarly.com/assets/files/cb6ce17d281d15f2c819035bcd430b0e/grammarly_logo.svg',
                'is_featured': False
            },
            {
                'name': 'Hugging Face',
                'provider': 'Hugging Face Inc.',
                'endpoint': 'https://huggingface.co/',
                'category': 'AI Platform',
                'description': 'Hugging Face is an AI community and platform that provides tools for building, training, and deploying machine learning models. It\'s known for its Transformers library, which provides thousands of pretrained models for natural language processing, computer vision, and more.',
                'popularity': 75,
                'api_type': 'huggingface',
                'api_model': 'various',
                'api_endpoint': 'https://api-inference.huggingface.co/models/',
                'image_url': 'https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png',
                'is_featured': False
            },
            {
                'name': 'Runway',
                'provider': 'Runway AI, Inc.',
                'endpoint': 'https://runwayml.com/',
                'category': 'Video Generator',
                'description': 'Runway is an applied AI research company that creates next-generation creation tools. It offers tools for video editing, generation, and visual effects powered by machine learning models.',
                'popularity': 72,
                'api_type': 'custom',
                'api_model': 'gen-2',
                'api_endpoint': 'https://api.runwayml.com/v1/generate',
                'image_url': 'https://cdn.sanity.io/images/7p2w2wp6/production/5f3d4c8a4c6c9c9c9c9c9c9c9c9c9c9c9c9c9c9c.svg',
                'is_featured': False
            },
            {
                'name': 'Synthesia',
                'provider': 'Synthesia Ltd.',
                'endpoint': 'https://www.synthesia.io/',
                'category': 'Video Generator',
                'description': 'Synthesia is an AI video generation platform that allows users to create videos with AI avatars. It can turn text into videos with realistic AI avatars speaking in over 120 languages.',
                'popularity': 68,
                'api_type': 'custom',
                'api_model': 'synthesia-v2',
                'api_endpoint': 'https://api.synthesia.io/v2/videos',
                'image_url': 'https://assets-global.website-files.com/61dc0796f359b6145bc06581/6241ba3d7d3f8d3671a23d1e_OG%20image%20(1).png',
                'is_featured': False
            },
            {
                'name': 'Otter.ai',
                'provider': 'Otter.ai',
                'endpoint': 'https://otter.ai/',
                'category': 'Transcription',
                'description': 'Otter.ai is an AI-powered transcription and note-taking app that can transcribe audio in real-time. It\'s designed for meetings, interviews, lectures, and other conversations.',
                'popularity': 65,
                'api_type': 'custom',
                'api_model': 'otter-transcribe',
                'api_endpoint': 'https://api.otter.ai/v1/transcribe',
                'image_url': 'https://assets-global.website-files.com/618e9316785b3582a5178502/6193689b70db96f8d37a7e7f_Logo%402x.png',
                'is_featured': False
            },
            {
                'name': 'Notion AI',
                'provider': 'Notion Labs, Inc.',
                'endpoint': 'https://www.notion.so/product/ai',
                'category': 'Word Processor',
                'description': 'Notion AI is an AI writing assistant integrated into the Notion workspace. It can help draft, edit, summarize, improve, and generate content directly within Notion documents.',
                'popularity': 78,
                'api_type': 'custom',
                'api_model': 'notion-ai',
                'api_endpoint': 'https://api.notion.com/v1/ai/completions',
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png',
                'is_featured': False
            },
        ]

        # Function to download and save image
        def download_and_save_image(url, name):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # Process image with PIL to ensure it's valid
                    img = Image.open(BytesIO(response.content))
                    
                    # Convert to RGB if needed (for PNG with transparency)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        if 'A' in img.getbands():
                            background.paste(img, mask=img.getchannel('A'))
                        else:
                            background.paste(img)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                        
                    # Save to BytesIO
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=85)
                    output.seek(0)
                    # Create a unique filename
                    filename = f"{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.jpg"
                    return ContentFile(output.read(), name=filename)
                return None
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error downloading image for {name}: {e}"))
                return None

        # Add AI tools to the database
        for tool_data in ai_tools:
            try:
                # Check if tool already exists
                existing_tool = AITool.objects.filter(name=tool_data['name']).first()
                
                if existing_tool:
                    self.stdout.write(f"AI tool '{tool_data['name']}' already exists, updating...")
                    # Update existing tool
                    for key, value in tool_data.items():
                        if key != 'image_url' and hasattr(existing_tool, key):
                            setattr(existing_tool, key, value)
                    
                    # Handle image separately
                    if 'image_url' in tool_data and tool_data['image_url']:
                        image_content = download_and_save_image(tool_data['image_url'], tool_data['name'])
                        if image_content:
                            existing_tool.image = image_content
                    
                    existing_tool.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated AI tool: {tool_data['name']}"))
                else:
                    # Create new tool
                    new_tool = AITool(
                        name=tool_data['name'],
                        provider=tool_data['provider'],
                        endpoint=tool_data['endpoint'],
                        category=tool_data['category'],
                        description=tool_data['description'],
                        popularity=tool_data['popularity'],
                        api_type=tool_data['api_type'],
                        api_model=tool_data['api_model'],
                        api_endpoint=tool_data['api_endpoint'],
                        is_featured=tool_data['is_featured']
                    )
                    
                    # Handle image
                    if 'image_url' in tool_data and tool_data['image_url']:
                        image_content = download_and_save_image(tool_data['image_url'], tool_data['name'])
                        if image_content:
                            new_tool.image = image_content
                    
                    new_tool.save()
                    self.stdout.write(self.style.SUCCESS(f"Added new AI tool: {tool_data['name']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error adding AI tool {tool_data['name']}: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully populated AI tools')) 