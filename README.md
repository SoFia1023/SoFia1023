# Inspire AI Project

## Overview
Inspire AI is a web application designed to help students and teachers discover, access, search, and interact with Artificial Intelligence tools. The project is part of "Proyecto Integrador 1" at EAFIT University. It provides a centralized platform for AI tool discovery, comparison, and interaction through chat interfaces.

## Main Objectives
- Provide a centralized catalog of AI tools
- Facilitate searching and filtering tools by category and functionality
- Offer detailed information about each tool
- Allow interaction with AI tools through integrated chat interfaces
- Enable users to save favorite tools and prompts
- Provide conversation history, sharing, and export functionality

## Technologies
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5.3
- **Database**: SQLite (development), PostgreSQL (production)
- **AI Integrations**: OpenAI API, Hugging Face API, Custom API integrations

## Project Structure
The project consists of multiple Django apps, each with specific responsibilities:

```
ProyectoIntegrador1/
├── catalog/            # AI tool catalog core functionality
│   ├── migrations/     # Database migrations
│   ├── static/         # CSS, JS, images
│   ├── templates/      # HTML templates
│   ├── management/     # Custom management commands
│   ├── admin.py        # Admin panel configuration
│   ├── models.py       # AI tool data models
│   ├── urls.py         # URL routing
│   └── views.py        # View controllers
├── interaction/        # User-AI interaction functionality
│   ├── migrations/     # Database migrations
│   ├── templates/      # HTML templates
│   ├── models.py       # Conversation and message models
│   ├── urls.py         # URL routing
│   └── views.py        # View controllers
├── users/              # User authentication and management
│   ├── migrations/     # Database migrations
│   ├── static/         # User-specific assets
│   ├── templates/      # User templates
│   ├── management/     # User management commands
│   ├── forms.py        # User forms
│   ├── models.py       # Custom user model
│   ├── urls.py         # URL routing
│   └── views.py        # User view controllers
└── inspireIA/          # Project configuration
    ├── settings/       # Environment-specific settings
    ├── urls.py         # Main URL configuration
    └── wsgi.py         # WSGI configuration for deployment
```

## Core Models

### AITool (catalog app)
- Stores information about AI tools including name, provider, category, description
- Supports API integration configurations (OpenAI, Hugging Face, custom)
- Tracks popularity and featured status

### CustomUser (users app)
- Extends Django's AbstractUser
- Email-based authentication
- Stores user preferences and favorites

### Conversation & Message (interaction app)
- Tracks user conversations with AI tools
- Stores message history with timestamps
- Supports conversation export and sharing

### FavoritePrompt & SharedChat (interaction app)
- Allows users to save and reuse favorite prompts
- Enables sharing conversations publicly or with specific users

## Implemented Features

### User Management
- Custom user registration and authentication
- User profiles with favorites and history
- Permission-based access control with user groups

### AI Tool Catalog
- Comprehensive AI tool listings with detailed information
- Search and filtering by category, popularity, and features
- Tool comparison functionality
- Favorite tools management

### AI Interaction
- Real-time chat interfaces with AI tools
- Conversation history management
- Favorite prompts saving and reuse
- Conversation sharing (public or private)
- Conversation export (JSON, text formats)

### Administration
- Enhanced admin interface for content management
- Bulk operations for AI tools and user data
- Permission management and monitoring
- Custom management commands for data import/export

## Key Endpoints

- `/` - Home page with featured AI tools
- `/catalog/` - Browse all AI tools with filtering
- `/catalog/presentation/<uuid>/` - Detailed AI tool information
- `/catalog/compare/` - Compare AI tools side by side
- `/interaction/chat/<uuid>/` - Chat with an AI tool
- `/interaction/conversations/` - View conversation history
- `/interaction/prompts/` - Manage favorite prompts
- `/interaction/share/<uuid>/` - Share conversations
- `/register/`, `/login/`, `/logout/` - User authentication
- `/profile/` - User profile management

## Management Commands

The project includes several custom Django management commands:

### AI Tool Management
- `python manage.py populate_ai_tools` - Populate database with predefined AI tools
- `python manage.py export_ai_tools` - Export AI tools to JSON
- `python manage.py import_ai_tools <file>` - Import AI tools from JSON

### User Management
- `python manage.py create_admin` - Create admin superuser
- `python manage.py create_test_users` - Create test user accounts
- `python manage.py setup_groups` - Configure permission groups

## Getting Started

### Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. (Optional) Populate with sample data: `python manage.py populate_ai_tools`
8. Start the server: `python manage.py runserver`

### Configuration
- Environment-specific configurations in `inspireIA/settings/`
- For AI API integration, configure API keys in environment variables
- Development settings in `development.py`, production in `production.py`

### Testing
- Run tests: `python manage.py test`
- Test specific app: `python manage.py test [app_name]`
- Test specific class: `python manage.py test [app_name.tests.TestClassName]`

## Contact
For more information about the project, contact the development team.
