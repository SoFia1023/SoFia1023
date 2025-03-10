# AI Tools Management Commands

This directory contains Django management commands for managing AI tools in your database.

## Available Commands

### 1. Populate AI Tools

This command populates your database with a predefined list of AI tools.

**Usage:**

```bash
python manage.py populate_ai_tools
```

**Options:**

- `--clear`: Clear existing AI tools before adding new ones

```bash
python manage.py populate_ai_tools --clear
```

### 2. Export AI Tools

This command exports all AI tools from your database to a JSON file.

**Usage:**

```bash
python manage.py export_ai_tools
```

**Options:**

- `--output`: Specify the output file path (default: ai_tools_export.json)

```bash
python manage.py export_ai_tools --output=my_ai_tools.json
```

### 3. Import AI Tools

This command imports AI tools from a JSON file into your database.

**Usage:**

```bash
python manage.py import_ai_tools <input_file>
```

**Options:**

- `--clear`: Clear existing AI tools before importing
- `--download-images`: Download images from URLs in the JSON file

```bash
python manage.py import_ai_tools ai_tools_export.json --clear --download-images
```

## Customization

You can customize the list of AI tools by editing the `ai_tools` list in the `populate_ai_tools.py` file. Each tool is represented as a dictionary with the following fields:

- `name`: The name of the AI tool
- `provider`: The company or organization that provides the tool
- `endpoint`: The URL where the tool can be accessed
- `category`: The category of the tool (e.g., Text Generator, Image Generator)
- `description`: A detailed description of the tool
- `popularity`: A numerical value representing the popularity of the tool (0-100)
- `api_type`: The type of API integration (openai, huggingface, custom, none)
- `api_model`: The specific model used by the tool
- `api_endpoint`: The API endpoint for the tool
- `image_url`: The URL of an image representing the tool
- `is_featured`: Whether the tool should be featured on the site

## Requirements

These commands require the following packages:
- Django
- Pillow
- requests

Make sure these are installed in your environment before running the commands. 