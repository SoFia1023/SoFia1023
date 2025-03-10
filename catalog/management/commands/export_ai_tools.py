import json
import os
from django.core.management.base import BaseCommand
from catalog.models import AITool
from django.core.serializers.json import DjangoJSONEncoder
import uuid

class UUIDEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

class Command(BaseCommand):
    help = 'Exports AI tools to a JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default='ai_tools_export.json',
            help='Output file path',
        )

    def handle(self, *args, **options):
        output_file = options['output']
        
        # Get all AI tools
        ai_tools = AITool.objects.all()
        
        # Convert to list of dictionaries
        tools_data = []
        for tool in ai_tools:
            tool_dict = {
                'id': tool.id,
                'name': tool.name,
                'provider': tool.provider,
                'endpoint': tool.endpoint,
                'category': tool.category,
                'description': tool.description,
                'popularity': tool.popularity,
                'api_type': tool.api_type,
                'api_model': tool.api_model,
                'api_endpoint': tool.api_endpoint,
                'is_featured': tool.is_featured,
                'image_url': tool.image.url if tool.image else None
            }
            tools_data.append(tool_dict)
        
        # Write to JSON file
        with open(output_file, 'w') as f:
            json.dump(tools_data, f, cls=UUIDEncoder, indent=4)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully exported {len(tools_data)} AI tools to {output_file}')) 