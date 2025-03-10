import json
import os
import uuid
from django.core.management.base import BaseCommand
from catalog.models import AITool
from django.core.files.base import ContentFile
import requests
from io import BytesIO
from PIL import Image
from django.conf import settings
import urllib.parse

class Command(BaseCommand):
    help = 'Imports AI tools from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'input_file',
            help='Input JSON file path',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing AI tools before importing',
        )
        parser.add_argument(
            '--download-images',
            action='store_true',
            help='Download images from URLs in the JSON file',
        )

    def handle(self, *args, **options):
        input_file = options['input_file']
        
        if not os.path.exists(input_file):
            self.stdout.write(self.style.ERROR(f'Input file {input_file} does not exist'))
            return
        
        if options['clear']:
            self.stdout.write('Clearing existing AI tools...')
            AITool.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared existing AI tools'))
        
        # Read JSON file
        with open(input_file, 'r') as f:
            tools_data = json.load(f)
        
        # Function to download and save image
        def download_and_save_image(url, name):
            try:
                # Check if URL is relative (from our media)
                if url.startswith('/media/'):
                    media_path = os.path.join(settings.MEDIA_ROOT, url.replace('/media/', ''))
                    if os.path.exists(media_path):
                        with open(media_path, 'rb') as f:
                            return ContentFile(f.read(), name=os.path.basename(media_path))
                
                # Otherwise download from external URL
                response = requests.get(url)
                if response.status_code == 200:
                    # Process image with PIL to ensure it's valid
                    img = Image.open(BytesIO(response.content))
                    
                    # Convert to RGB if needed
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
        
        # Import AI tools
        imported_count = 0
        for tool_data in tools_data:
            try:
                # Check if tool already exists by ID or name
                existing_tool = None
                if 'id' in tool_data:
                    try:
                        existing_tool = AITool.objects.filter(id=tool_data['id']).first()
                    except (ValueError, TypeError):
                        pass
                
                if not existing_tool and 'name' in tool_data:
                    existing_tool = AITool.objects.filter(name=tool_data['name']).first()
                
                if existing_tool:
                    self.stdout.write(f"AI tool '{tool_data['name']}' already exists, updating...")
                    # Update existing tool
                    for key, value in tool_data.items():
                        if key not in ['id', 'image_url'] and hasattr(existing_tool, key):
                            setattr(existing_tool, key, value)
                    
                    # Handle image separately if needed
                    if options['download_images'] and 'image_url' in tool_data and tool_data['image_url']:
                        image_content = download_and_save_image(tool_data['image_url'], tool_data['name'])
                        if image_content:
                            existing_tool.image = image_content
                    
                    existing_tool.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated AI tool: {tool_data['name']}"))
                else:
                    # Create new tool
                    new_tool_data = {k: v for k, v in tool_data.items() if k not in ['id', 'image_url']}
                    
                    # Handle ID if provided
                    if 'id' in tool_data:
                        try:
                            new_tool_data['id'] = uuid.UUID(tool_data['id'])
                        except (ValueError, TypeError):
                            pass
                    
                    new_tool = AITool(**new_tool_data)
                    
                    # Handle image
                    if options['download_images'] and 'image_url' in tool_data and tool_data['image_url']:
                        image_content = download_and_save_image(tool_data['image_url'], tool_data['name'])
                        if image_content:
                            new_tool.image = image_content
                    
                    new_tool.save()
                    self.stdout.write(self.style.SUCCESS(f"Added new AI tool: {tool_data['name']}"))
                
                imported_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing AI tool {tool_data.get('name', 'unknown')}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {imported_count} AI tools from {input_file}')) 