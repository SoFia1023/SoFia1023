# InspireIA Project Overview

## Introduction

InspireIA is a comprehensive platform designed to help users discover, compare, and interact with various AI tools. The platform provides a catalog of AI tools, allows users to chat with these tools, save favorite prompts, and share conversations with others.

## Project Structure

```
InspireIA/
├── api/                    # API app for RESTful endpoints
│   ├── serializers/        # Serializers for model data
│   ├── views/              # API views
│   └── urls.py             # API URL routing
├── catalog/                # Catalog app for AI tool listings
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── views/              # View functions and classes
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin panel configuration
├── docs/                   # Project documentation
├── inspireIA/              # Main project configuration
│   ├── settings/           # Environment-specific settings
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # Global templates
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── interaction/            # Interaction app for AI conversations
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── views/              # View functions and classes
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin panel configuration
├── media/                  # User-uploaded files
├── static/                 # Collected static files
├── users/                  # Users app for authentication
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── views/              # View functions and classes
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin panel configuration
├── .env                    # Environment variables (not in version control)
├── .gitignore              # Git ignore file
├── manage.py               # Django management script
├── README.md               # Project readme
└── requirements.txt        # Python dependencies
```

## Directory Structure Details

### API App

The API app provides RESTful endpoints for interacting with the application programmatically.

```
api/
├── serializers/
│   ├── catalog.py          # Serializers for catalog models
│   ├── interaction.py      # Serializers for interaction models
│   └── users.py            # Serializers for user models
├── views/
│   ├── catalog.py          # API views for catalog functionality
│   ├── interaction.py      # API views for interaction functionality
│   └── users.py            # API views for user functionality
├── urls.py                 # API URL routing
├── permissions.py          # Custom permissions for API access
└── tests/                  # API tests
```

### Catalog App

The Catalog app manages the AI tool catalog, including tool listings, search, filtering, and comparison functionality.

```
catalog/
├── migrations/             # Database migrations
├── templates/
│   ├── catalog/
│   │   ├── home.html       # Home page template
│   │   ├── tool_list.html  # Tool listing template
│   │   ├── tool_detail.html # Tool detail template
│   │   └── compare.html    # Tool comparison template
├── views/
│   ├── ai_tools.py         # Views for AI tools
│   ├── categories.py       # Views for categories
│   └── search.py           # Views for search functionality
├── models.py               # Database models
├── urls.py                 # URL routing
├── admin.py                # Admin panel configuration
├── mixins.py               # Reusable view mixins
├── context_processors.py   # Context processors
└── utils.py                # Utility functions
```

### Interaction App

The Interaction app manages user interactions with AI tools, including conversations, messages, favorite prompts, and sharing functionality.

```
interaction/
├── migrations/             # Database migrations
├── templates/
│   ├── interaction/
│   │   ├── chat.html       # Chat interface template
│   │   ├── favorites.html  # Favorite prompts template
│   │   └── shared.html     # Shared conversations template
├── views/
│   ├── chat.py             # Views for chat functionality
│   ├── favorites.py        # Views for favorite prompts
│   └── sharing.py          # Views for sharing functionality
├── models.py               # Database models
├── urls.py                 # URL routing
├── admin.py                # Admin panel configuration
├── utils.py                # Utility functions
└── templatetags/
    └── interaction_extras.py # Custom template tags
```

### Users App

The Users app manages user authentication, registration, profile management, and permissions.

```
users/
├── migrations/             # Database migrations
├── templates/
│   ├── users/
│   │   ├── login.html      # Login template
│   │   ├── register.html   # Registration template
│   │   └── dashboard.html  # Dashboard template
├── views/
│   ├── auth.py             # Authentication views
│   ├── dashboard.py        # Dashboard views
│   └── profile.py          # Profile views
├── models.py               # Database models
├── urls.py                 # URL routing
├── admin.py                # Admin panel configuration
├── forms.py                # User-related forms
└── management/
    └── commands/
        └── setup_groups.py # Command for setting up permission groups
```

### InspireIA (Main Project)

The main project configuration and settings.

```
inspireIA/
├── settings/
│   ├── base.py             # Base settings
│   ├── development.py      # Development settings
│   └── production.py       # Production settings
├── static/                 # Static files
│   ├── css/                # CSS files
│   ├── js/                 # JavaScript files
│   └── images/             # Image files
├── templates/
│   ├── base.html           # Base template
│   ├── navbar.html         # Navigation bar template
│   └── footer.html         # Footer template
├── urls.py                 # Main URL configuration
├── middleware.py           # Custom middleware
├── admin.py                # Custom admin site configuration
├── wsgi.py                 # WSGI configuration
└── asgi.py                 # ASGI configuration
```

## File Organization Principles

1. **Modular Structure**: The project follows a modular approach with separate apps for distinct functionality.
2. **Separation of Concerns**: Each app has a specific responsibility and focuses on a particular domain.
3. **DRY Principle**: Code reuse is encouraged through utility functions, mixins, and template inheritance.
4. **View Organization**: Views are organized in subdirectories based on functionality within each app.
5. **Template Structure**: Templates follow a hierarchical structure with inheritance from base templates.
6. **Static Files**: Static files are organized by type (CSS, JS, images) and app-specific needs.
7. **Configuration**: Settings are split into environment-specific files for better maintainability.

## Coding Standards

1. **PEP 8**: Python code follows PEP 8 style guide.
2. **Type Hints**: Type hints are used consistently throughout the codebase.
3. **Documentation**: Docstrings and comments are used to explain code functionality.
4. **Testing**: Unit tests are written for critical functionality.
5. **Code Formatting**: Black is used for code formatting.
6. **Import Sorting**: isort is used for import sorting.
7. **Linting**: flake8 is used for linting.
