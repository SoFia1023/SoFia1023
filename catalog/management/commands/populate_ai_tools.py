import json
import os
import random
import time
from django.core.management.base import BaseCommand
from catalog.models import AITool
from django.conf import settings
from django.core.files.base import ContentFile
import requests
from io import BytesIO
from PIL import Image
import uuid
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database with AI tools and fetches high-quality logos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing AI tools before adding new ones',
        )
        parser.add_argument(
            '--update-images',
            action='store_true',
            help='Update images for existing AI tools',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing AI tools...')
            AITool.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared existing AI tools'))

        # List of AI tools with their details and improved logo URLs
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/chatgpt-1.svg',
                'backup_urls': [
                    'https://1000logos.net/wp-content/uploads/2023/02/ChatGPT-Logo.png',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/1200px-ChatGPT_logo.svg.png'
                ],
                'logo_search_term': 'ChatGPT logo transparent',
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
                'image_url': 'https://seeklogo.com/images/D/dall-e-logo-1DD3C0AF39-seeklogo.com.png',
                'backup_urls': [
                    'https://cdn.worldvectorlogo.com/logos/dall-e-2.svg',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/DALL-E_Logo.png/640px-DALL-E_Logo.png'
                ],
                'logo_search_term': 'DALL-E logo official transparent',
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
                'image_url': 'https://seeklogo.com/images/M/midjourney-logo-A21208B8EB-seeklogo.com.png',
                'backup_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.png',
                    'https://cdn.worldvectorlogo.com/logos/midjourney.svg'
                ],
                'logo_search_term': 'Midjourney logo official transparent',
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
                'image_url': 'https://seeklogo.com/images/S/stable-diffusion-logo-8EEF76E240-seeklogo.com.png',
                'backup_urls': [
                    'https://storage.googleapis.com/stable-diffusion-art/sd-space-images/stable-diffusion-image.png',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Stable_Diffusion_logo.png/640px-Stable_Diffusion_logo.png'
                ],
                'logo_search_term': 'Stable Diffusion logo transparent official',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/anthropic-2.svg',
                'backup_urls': [
                    'https://d1muf25xaso8hp.cloudfront.net/https%3A%2F%2Fs3.amazonaws.com%2Fappforest_uf%2Ff1697649857507x778114736463423000%2FAnthropicLogo.png?w=192&h=64&auto=compress&dpr=1&fit=max',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Anthropic_Logo.png/640px-Anthropic_Logo.png'
                ],
                'logo_search_term': 'Claude AI Anthropic logo transparent',
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
                'image_url': 'https://seeklogo.com/images/G/google-gemini-logo-6D598BF8B1-seeklogo.com.png',
                'backup_urls': [
                    'https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-logo.max-300x300.jpg',
                    'https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini_1.width-1300.format-webp.webp'
                ],
                'logo_search_term': 'Google Gemini AI logo transparent',
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
                'image_url': 'https://avatars.githubusercontent.com/u/14957082?s=280&v=4',
                'backup_urls': [
                    'https://miro.medium.com/v2/resize:fit:2000/1*JluYG5ZmxQvXL-TdJOu8Vw.png',
                    'https://cdn.openai.com/whisper/draft-20220919a/asr-summary-of-model-architecture-light.svg'
                ],
                'logo_search_term': 'OpenAI Whisper logo transparent',
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
                'image_url': 'https://i.pcmag.com/imagery/reviews/05XBKmNFYUrwKCVLqeYVNnE-7.fit_scale.size_1028x578.v1694533352.png',
                'backup_urls': [
                    'https://cdn.worldvectorlogo.com/logos/github-copilot.svg',
                    'https://github.blog/wp-content/uploads/2022/06/GitHub-Copilot-GA_banner.png'
                ],
                'logo_search_term': 'GitHub Copilot logo transparent',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/jasper-ai.svg',
                'backup_urls': [
                    'https://www.jasper.ai/images/logos/jasper.svg',
                    'https://assets-global.website-files.com/60e5f2de011b86acebc30db7/64b7a3e6e6c1a2e7f9c6c447_Jasper-Wordmark-Black.svg'
                ],
                'logo_search_term': 'Jasper AI logo transparent',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/grammarly-1.svg',
                'backup_urls': [
                    'https://static.grammarly.com/assets/files/cbd7bbeb88f576866883f2aca5320b16/grammarly_logo.svg',
                    'https://static.grammarly.com/assets/files/cb6ce17d281d15f2c819035bcd430b0e/grammarly_logo.svg'
                ],
                'logo_search_term': 'Grammarly logo transparent',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/huggingface-1.svg',
                'backup_urls': [
                    'https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.svg',
                    'https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png'
                ],
                'logo_search_term': 'Hugging Face logo transparent',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/runway-ml.svg',
                'backup_urls': [
                    'https://uploads-ssl.webflow.com/5ec38213cb7a7c4c3fcd8cbf/5f7b5b40e3bbc3f08b8c9a20_runway-logo-white.svg',
                    'https://cdn.sanity.io/images/7p2w2wp6/production/5f3d4c8a4c6c9c9c9c9c9c9c9c9c9c9c9c9c9c9c.svg'
                ],
                'logo_search_term': 'Runway AI logo transparent',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/synthesia.svg',
                'backup_urls': [
                    'https://lever-client-logos.s3.us-west-2.amazonaws.com/6fecf749-b084-4f32-8789-264a2b2d07a5-1666168185180.png',
                    'https://assets-global.website-files.com/61dc0796f359b6145bc06581/6241ba3d7d3f8d3671a23d1e_OG%20image%20(1).png'
                ],
                'logo_search_term': 'Synthesia AI logo transparent',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/otter-1.svg',
                'backup_urls': [
                    'https://brandfetch.com/_next/image?url=https%3A%2F%2Fasset.brandfetch.io%2FidGRv2N2u7%2Fid4w536b8B.png&w=1080&q=75',
                    'https://assets-global.website-files.com/618e9316785b3582a5178502/6193689b70db96f8d37a7e7f_Logo%402x.png'
                ],
                'logo_search_term': 'Otter.ai logo transparent',
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
                'image_url': 'https://cdn.worldvectorlogo.com/logos/notion-logo-1.svg',
                'backup_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png',
                    'https://logos-world.net/wp-content/uploads/2023/02/Notion-Logo.png'
                ],
                'logo_search_term': 'Notion AI logo transparent',
                'is_featured': False
            },
        ]

        # Function to download and save image with retries and improved error handling
        def download_and_save_image(url, name, attempts=0, max_attempts=3):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    # Process image with PIL to ensure it's valid
                    try:
                        img = Image.open(BytesIO(response.content))
                        
                        # Check if image has good dimensions for a logo
                        width, height = img.size
                        if width < 50 or height < 50:
                            self.stdout.write(self.style.WARNING(f"Image for {name} is too small ({width}x{height}), trying next source..."))
                            return None
                        
                        # Keep transparency for PNG images
                        if img.mode in ('RGBA', 'LA'):
                            # For transparent PNGs, maintain transparency
                            output = BytesIO()
                            img.save(output, format='PNG')
                            output.seek(0)
                            # Create a unique filename
                            filename = f"{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.png"
                            return ContentFile(output.read(), name=filename)
                        # Convert other formats to RGB and save as JPEG
                        else:
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            
                            # Save to BytesIO
                            output = BytesIO()
                            img.save(output, format='JPEG', quality=95)  # Higher quality
                            output.seek(0)
                            # Create a unique filename
                            filename = f"{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.jpg"
                            return ContentFile(output.read(), name=filename)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Error processing image for {name}: {e}"))
                        return None
                else:
                    self.stdout.write(self.style.WARNING(f"Failed to download image from {url}: HTTP {response.status_code}"))
                    return None
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error downloading image for {name}: {e}"))
                if attempts < max_attempts:
                    self.stdout.write(f"Retrying download for {name} (attempt {attempts+1} of {max_attempts})...")
                    time.sleep(1)  # Wait before retry
                    return download_and_save_image(url, name, attempts + 1, max_attempts)
                return None

        # Function to try multiple image sources
        def get_image_content(tool_data):
            # Try primary image URL
            if 'image_url' in tool_data and tool_data['image_url']:
                self.stdout.write(f"Trying primary image URL for {tool_data['name']}...")
                image_content = download_and_save_image(tool_data['image_url'], tool_data['name'])
                if image_content:
                    return image_content
            
            # Try backup URLs if available
            if 'backup_urls' in tool_data and tool_data['backup_urls']:
                for i, url in enumerate(tool_data['backup_urls']):
                    self.stdout.write(f"Trying backup URL {i+1} for {tool_data['name']}...")
                    image_content = download_and_save_image(url, tool_data['name'])
                    if image_content:
                        return image_content
            
            # If all attempts fail, return None
            self.stdout.write(self.style.WARNING(f"All image sources failed for {tool_data['name']}"))
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
                        if key not in ['image_url', 'backup_urls', 'logo_search_term'] and hasattr(existing_tool, key):
                            setattr(existing_tool, key, value)
                    
                    # Handle image separately if it's missing or update is requested
                    if options['update_images'] or not existing_tool.image:
                        self.stdout.write(f"Updating image for {tool_data['name']}...")
                        image_content = get_image_content(tool_data)
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
                    image_content = get_image_content(tool_data)
                    if image_content:
                        new_tool.image = image_content
                    
                    new_tool.save()
                    self.stdout.write(self.style.SUCCESS(f"Added new AI tool: {tool_data['name']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error adding AI tool {tool_data['name']}: {e}"))
                logger.error(f"Error adding AI tool {tool_data['name']}: {e}", exc_info=True)

        self.stdout.write(self.style.SUCCESS('Successfully populated AI tools')) 