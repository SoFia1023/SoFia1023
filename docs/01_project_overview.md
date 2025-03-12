# InspireIA Project Overview

## Introduction

InspireIA is a comprehensive platform designed to help users discover, compare, and interact with various AI tools. The platform provides a catalog of AI tools, allows users to chat with these tools, save favorite prompts, and share conversations with others. The project is part of "Proyecto Integrador 1" at EAFIT University, focusing on creating a centralized hub for AI tool discovery and interaction specifically tailored for educational and research purposes.

## Project Vision and Goals

### Vision Statement

To become the leading platform for AI tool discovery and interaction in educational environments, empowering students and educators to leverage AI technologies effectively in their learning and teaching processes.

### Core Goals

1. **Accessibility**: Make AI tools accessible to users with varying levels of technical expertise
2. **Education**: Provide educational resources about AI tools and their applications
3. **Curation**: Offer a curated selection of high-quality AI tools relevant to education
4. **Integration**: Enable seamless interaction with various AI tools through a unified interface
5. **Community**: Foster a community of AI tool users and developers in educational settings
6. **Innovation**: Encourage innovative applications of AI in education through example use cases

## Project Architecture

InspireIA follows a modular, component-based architecture based on Django's MVT (Model-View-Template) pattern:

### Architecture Layers

1. **Presentation Layer**: Templates, CSS, JavaScript for user interface
2. **Application Layer**: Views, URL patterns, forms for business logic
3. **Data Layer**: Models, managers, migrations for data persistence
4. **Integration Layer**: API clients, webhooks for external service integration
5. **Infrastructure Layer**: Settings, middleware, WSGI/ASGI configuration

### Key Architectural Decisions

1. **Modular App Structure**: Separate Django apps for distinct functionality domains
2. **View Organization**: Views organized in subdirectories by feature area
3. **Type Hints**: Consistent use of Python type hints throughout the codebase
4. **Mixins Over Inheritance**: Preference for composition over inheritance using mixins
5. **Separation of Concerns**: Clear separation between data access, business logic, and presentation

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

### Python Code Standards

1. **PEP 8**: Python code follows PEP 8 style guide for consistent formatting
2. **Type Hints**: Type hints are used consistently throughout the codebase
3. **Documentation**: Docstrings follow the Google style guide format
4. **Imports**: Imports are organized using isort with the following sections:
   - Standard library imports
   - Third-party library imports
   - Django imports
   - Local application imports
5. **Naming Conventions**:
   - Classes: CamelCase (e.g., `AITool`, `UserProfile`)
   - Functions/Methods: snake_case (e.g., `get_tools`, `format_response`)
   - Variables: snake_case (e.g., `user_id`, `tool_list`)
   - Constants: UPPER_CASE (e.g., `DEFAULT_TIMEOUT`, `API_VERSION`)

### JavaScript Code Standards

1. **ES6+ Features**: Modern JavaScript features are used throughout
2. **Function Declarations**: Arrow functions for callbacks, named functions for methods
3. **Variable Declarations**: `const` by default, `let` when reassignment is needed
4. **DOM Manipulation**: Vanilla JavaScript with helper functions
5. **Event Handling**: Event delegation pattern for dynamic elements

### HTML/CSS Standards

1. **Semantic HTML**: Proper use of semantic HTML5 elements
2. **Accessibility**: WCAG 2.1 AA compliance with proper ARIA attributes
3. **CSS Organization**: Component-based CSS with BEM naming convention
4. **Responsive Design**: Mobile-first approach with responsive breakpoints
5. **CSS Variables**: Use of CSS custom properties for theming

### Testing Standards

1. **Test Coverage**: Minimum 70% test coverage for critical functionality
2. **Test Organization**: Tests organized by app and feature area
3. **Fixtures**: Reusable test fixtures for common test scenarios
4. **Mocking**: External services are mocked in tests
5. **CI Integration**: Tests run automatically on pull requests

### Documentation Standards

1. **Code Documentation**: Comprehensive docstrings for all functions, classes, and methods
2. **Project Documentation**: Markdown files in the `docs/` directory
3. **API Documentation**: OpenAPI/Swagger documentation for API endpoints
4. **User Documentation**: User guides and tutorials in the project wiki
5. **Change Documentation**: Detailed commit messages and pull request descriptions

### Version Control Standards

1. **Branching Strategy**: Feature branches with pull requests to main
2. **Commit Messages**: Conventional Commits format (type: description)
3. **Code Reviews**: Required for all pull requests
4. **CI/CD**: Automated testing and deployment pipelines
5. **Release Management**: Semantic versioning for releases
