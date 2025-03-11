import os
import time
import requests
import urllib.parse
from io import BytesIO
from PIL import Image
import uuid
import logging
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from catalog.models import AITool

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetches and updates high-quality logos for AI tools using various methods'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update of all images even if they already exist',
        )

    def handle(self, *args, **options):
        force_update = options['force']
        
        # Dictionary of AI tools and their logo sources
        # We're using multiple approaches to maximize chances of getting a good logo
        ai_tool_logos = {
            'ChatGPT': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/512px-ChatGPT_logo.svg.png',
                ],
                'search_term': 'ChatGPT logo transparent png',
                'brand_name': 'chatgpt',
                'company': 'openai'
            },
            'DALL-E': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/9/99/DALL-E_Logo.png',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/DALL-E_Logo.png/512px-DALL-E_Logo.png',
                ],
                'search_term': 'DALL-E OpenAI logo transparent png',
                'brand_name': 'dall-e',
                'company': 'openai'
            },
            'Midjourney': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.png',
                ],
                'search_term': 'Midjourney logo transparent png',
                'brand_name': 'midjourney',
                'company': 'midjourney'
            },
            'Stable Diffusion': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/a/a4/Stable_Diffusion_logo.png',
                ],
                'search_term': 'Stable Diffusion logo transparent png',
                'brand_name': 'stable-diffusion',
                'company': 'stability-ai'
            },
            'Claude': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/20/Anthropic_Logo.png',
                ],
                'search_term': 'Claude Anthropic logo transparent png',
                'brand_name': 'claude',
                'company': 'anthropic'
            },
            'Gemini': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_Gemini_icon.svg',
                ],
                'search_term': 'Google Gemini AI logo transparent png',
                'brand_name': 'gemini',
                'company': 'google'
            },
            'Whisper': {
                'direct_urls': [
                    'https://github.com/openai/whisper/blob/main/notebooks/assets/whisper.jpg?raw=true',
                ],
                'search_term': 'OpenAI Whisper logo transparent png',
                'brand_name': 'whisper',
                'company': 'openai'
            },
            'Copilot': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg',
                ],
                'search_term': 'GitHub Copilot logo transparent png',
                'brand_name': 'github-copilot',
                'company': 'github'
            },
            'Jasper': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/c/cf/Jasper_%28software%29_Logo.png',
                ],
                'search_term': 'Jasper AI logo transparent png',
                'brand_name': 'jasper-ai',
                'company': 'jasper'
            },
            'Grammarly': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/1/19/Grammarly_logo.svg',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Grammarly_logo.svg/512px-Grammarly_logo.svg.png',
                ],
                'search_term': 'Grammarly logo transparent png',
                'brand_name': 'grammarly',
                'company': 'grammarly'
            },
            'Hugging Face': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/8/83/Hugging-Face-Logo-Unofficial.svg',
                    'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Hugging-Face-Logo-Unofficial.svg/512px-Hugging-Face-Logo-Unofficial.svg.png',
                ],
                'search_term': 'Hugging Face logo transparent png',
                'brand_name': 'hugging-face',
                'company': 'huggingface'
            },
            'Runway': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/1/1f/RunwayML_Logo.svg',
                ],
                'search_term': 'Runway AI logo transparent png',
                'brand_name': 'runway',
                'company': 'runway-ml'
            },
            'Synthesia': {
                'direct_urls': [
                    'https://cdn1.synthesys.io/wp-content/uploads/2022/06/synthesia-logo-horizontal.png',
                ],
                'search_term': 'Synthesia AI logo transparent png',
                'brand_name': 'synthesia',
                'company': 'synthesia'
            },
            'Otter.ai': {
                'direct_urls': [
                    'https://play-lh.googleusercontent.com/Uwe_0p8-wQ-APDwmtkRbLTiP9jvFmh1_D4ogKMzx3VnAjRnR7Z-tpSVoNjl2ADDWvIVl',
                ],
                'search_term': 'Otter.ai logo transparent png',
                'brand_name': 'otter-ai',
                'company': 'otter'
            },
            'Notion AI': {
                'direct_urls': [
                    'https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png',
                ],
                'search_term': 'Notion AI logo transparent png',
                'brand_name': 'notion',
                'company': 'notion'
            },
        }

        # Try to fetch logos using different methods and update the database
        for ai_tool_name, logo_sources in ai_tool_logos.items():
            try:
                ai_tool = AITool.objects.filter(name=ai_tool_name).first()
                if not ai_tool:
                    self.stdout.write(self.style.WARNING(f"AI tool '{ai_tool_name}' not found in database, skipping..."))
                    continue

                # Skip if tool already has an image and force update is not enabled
                if ai_tool.image and not force_update:
                    self.stdout.write(f"AI tool '{ai_tool_name}' already has an image, skipping... (use --force to override)")
                    continue
                
                self.stdout.write(f"Updating logo for {ai_tool_name}...")
                
                # Try all methods to get a logo
                image_content = self.try_all_logo_methods(ai_tool_name, logo_sources)
                
                if image_content:
                    ai_tool.image = image_content
                    ai_tool.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully updated logo for {ai_tool_name}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to get a logo for {ai_tool_name} after trying all methods"))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing {ai_tool_name}: {str(e)}"))
                logger.error(f"Error processing {ai_tool_name}: {str(e)}", exc_info=True)
        
        self.stdout.write(self.style.SUCCESS("Finished updating AI tool logos"))

    def try_all_logo_methods(self, tool_name, logo_sources):
        """Try all available methods to get a logo"""
        self.stdout.write(f"Trying to get logo for {tool_name}...")
        
        # Method 1: Try direct URLs
        if 'direct_urls' in logo_sources and logo_sources['direct_urls']:
            for url in logo_sources['direct_urls']:
                self.stdout.write(f"  Trying direct URL: {url}")
                image_content = self.download_and_process_image(url, tool_name)
                if image_content:
                    return image_content
        
        # Method 2: Try Wikipedia API
        self.stdout.write(f"  Trying Wikipedia logo search...")
        image_content = self.get_logo_from_wikipedia(tool_name)
        if image_content:
            return image_content
        
        # Method 3: Try search term with DuckDuckGo
        if 'search_term' in logo_sources and logo_sources['search_term']:
            self.stdout.write(f"  Trying search term: {logo_sources['search_term']}")
            image_content = self.search_logo_image(logo_sources['search_term'])
            if image_content:
                return image_content
        
        return None

    def download_and_process_image(self, url, name, max_attempts=3):
        """Download and process an image from URL with retries"""
        for attempt in range(max_attempts):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    try:
                        img = Image.open(BytesIO(response.content))
                        
                        # Check if image has good dimensions for a logo
                        width, height = img.size
                        if width < 50 or height < 50:
                            self.stdout.write(f"    Image is too small ({width}x{height}), skipping...")
                            return None
                        
                        # Create standardized square logo with padding if needed
                        img = self.standardize_logo(img)
                        
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
                        self.stdout.write(f"    Error processing image: {e}")
                else:
                    self.stdout.write(f"    HTTP error {response.status_code} for URL: {url}")
            
            except Exception as e:
                self.stdout.write(f"    Error downloading image (attempt {attempt+1}/{max_attempts}): {e}")
                if attempt < max_attempts - 1:
                    time.sleep(1)  # Wait before retry
        
        return None

    def standardize_logo(self, img):
        """Standardize logo to make it look professional with proper padding"""
        # Get original size
        width, height = img.size
        
        # Determine if we need to add padding to make it square
        if abs(width - height) < min(width, height) * 0.1:  # Already roughly square
            max_dim = max(width, height)
            new_size = (max_dim, max_dim)
        else:  # Not square, but we'll keep aspect ratio
            return img  # Keep original aspect ratio
        
        # Create a new transparent image
        if img.mode == 'RGBA':
            new_img = Image.new('RGBA', new_size, (0, 0, 0, 0))
        else:
            new_img = Image.new('RGB', new_size, (255, 255, 255))
        
        # Calculate position to paste original image (centered)
        paste_x = (new_size[0] - width) // 2
        paste_y = (new_size[1] - height) // 2
        
        # Paste original image onto new canvas
        if img.mode == 'RGBA':
            new_img.paste(img, (paste_x, paste_y), img)
        else:
            new_img.paste(img, (paste_x, paste_y))
        
        return new_img

    def get_logo_from_wikipedia(self, company_name):
        """Try to get a logo from Wikipedia"""
        try:
            # First search for the company page
            search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(company_name)}&format=json"
            search_response = requests.get(search_url)
            search_data = search_response.json()
            
            if 'query' in search_data and 'search' in search_data['query'] and search_data['query']['search']:
                page_title = search_data['query']['search'][0]['title']
                
                # Now get the page images
                images_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(page_title)}&prop=images&format=json"
                images_response = requests.get(images_url)
                images_data = images_response.json()
                
                if 'query' in images_data and 'pages' in images_data['query']:
                    for page_id, page_data in images_data['query']['pages'].items():
                        if 'images' in page_data:
                            # Look for logo images
                            logo_images = [img for img in page_data['images'] if 'logo' in img['title'].lower() or 'icon' in img['title'].lower()]
                            if logo_images:
                                # Get the actual image URL
                                for logo in logo_images:
                                    file_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(logo['title'])}&prop=imageinfo&iiprop=url&format=json"
                                    file_response = requests.get(file_url)
                                    file_data = file_response.json()
                                    
                                    if 'query' in file_data and 'pages' in file_data['query']:
                                        for img_page_id, img_page_data in file_data['query']['pages'].items():
                                            if 'imageinfo' in img_page_data and img_page_data['imageinfo']:
                                                img_url = img_page_data['imageinfo'][0]['url']
                                                image_content = self.download_and_process_image(img_url, company_name)
                                                if image_content:
                                                    return image_content
        except Exception as e:
            self.stdout.write(f"    Error getting Wikipedia logo: {e}")
        
        return None

    def search_logo_image(self, search_term):
        """Search for logo images using DuckDuckGo"""
        try:
            # Use DuckDuckGo API (non-official)
            search_url = f"https://duckduckgo.com/?q={urllib.parse.quote(search_term)}&iax=images&ia=images&format=json"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # This is a fallback that won't work well in production due to DuckDuckGo's protections
            # For a production app, you should use a proper image search API
            self.stdout.write("    Note: Image search is limited in this demo. For production, use a paid API service.")
            
            # For demo purposes, let's just try a few predefined sources for common logos
            common_logo_sources = {
                'chatgpt logo': 'https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg',
                'dalle logo': 'https://upload.wikimedia.org/wikipedia/commons/9/99/DALL-E_Logo.png',
                'midjourney logo': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Midjourney_Emblem.png',
                'stable diffusion logo': 'https://upload.wikimedia.org/wikipedia/commons/a/a4/Stable_Diffusion_logo.png',
                'claude ai logo': 'https://upload.wikimedia.org/wikipedia/commons/2/20/Anthropic_Logo.png',
                'gemini ai logo': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_Gemini_icon.svg',
                'google logo': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg',
                'openai logo': 'https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg',
                'github logo': 'https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg',
                'jasper ai logo': 'https://upload.wikimedia.org/wikipedia/commons/c/cf/Jasper_%28software%29_Logo.png',
                'grammarly logo': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Grammarly_logo.svg',
                'hugging face logo': 'https://upload.wikimedia.org/wikipedia/commons/8/83/Hugging-Face-Logo-Unofficial.svg',
                'notion logo': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png',
            }
            
            # Try to find a matching logo
            for key, url in common_logo_sources.items():
                if any(term.lower() in key.lower() for term in search_term.lower().split()):
                    self.stdout.write(f"    Found potential match in common logos: {url}")
                    image_content = self.download_and_process_image(url, search_term)
                    if image_content:
                        return image_content
            
            return None
            
        except Exception as e:
            self.stdout.write(f"    Error searching for logo: {e}")
            return None