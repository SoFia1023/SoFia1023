# Inspire AI Project

![Inspire AI Logo](https://img.shields.io/badge/Inspire%20AI-Empowering%20Education-blue?style=for-the-badge)

> *Empowering students and educators through intelligent technology discovery*

[![Django](https://img.shields.io/badge/Django-5.1+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/Mateoloperaortiz/ProyectoIntegrador1)

---

## ✨ Overview

Inspire AI is a comprehensive web application designed to help students and teachers discover, access, search, and interact with Artificial Intelligence tools. The project is part of "Proyecto Integrador 1" at EAFIT University. It provides a centralized platform for AI tool discovery, comparison, and interaction through chat interfaces, with a focus on education and research applications.

![Project Banner](https://img.shields.io/badge/EAFIT-Proyecto%20Integrador%201-orange?style=for-the-badge)

## 🎯 Main Objectives

- Provide a centralized catalog of AI tools with comprehensive information
- Facilitate searching and filtering tools by category, pricing, and functionality
- Offer detailed information about each tool with comparison capabilities
- Allow interaction with AI tools through integrated chat interfaces
- Enable users to save favorite tools and prompts for quick access
- Provide conversation history, sharing, and export functionality
- Create a responsive, accessible interface that works across all devices
- Implement a secure authentication system with role-based permissions
- Offer analytics and insights on tool usage and popularity

## 📂 Modular Code Structure

The project follows a modular code organization pattern to improve maintainability and scalability:

### View Organization

- **Modular Views**: Views are organized into separate modules based on functionality (e.g., `catalog/views/catalog.py`, `catalog/views/ai_tools.py`)
- **Clear Imports**: Each app's `__init__.py` file exports all necessary views for URL routing
- **Centralized Constants**: Common constants like `CATEGORIES` are defined in dedicated files
- **Class-Based Views**: Extensive use of Django's class-based views with mixins for code reuse
- **Function-Based Alternatives**: Simpler function-based views provided as alternatives where appropriate

### Model Organization

- **Clear Relationships**: Models have well-defined relationships with appropriate foreign keys
- **Type Hints**: All models use Python type hints for better code completion and error detection
- **Comprehensive Docstrings**: Detailed documentation for each model and its fields
- **Custom Managers**: Where needed, models have custom managers for common query operations

### Benefits of Modular Structure

- **Improved Readability**: Smaller, focused files are easier to understand
- **Better Maintainability**: Changes to one feature don't affect others
- **Easier Collaboration**: Team members can work on different modules simultaneously
- **Simplified Testing**: Isolated modules are easier to test
- **Clearer Dependencies**: Import structure clearly shows dependencies between components
- **Scalability**: New features can be added without disrupting existing functionality
- **Reusability**: Common patterns can be extracted into mixins and utility functions

## 🚀 Features Highlight

Inspire AI offers a comprehensive set of features designed to enhance the discovery and use of AI tools:

## 🧭 URL Patterns and Routing

The Inspire AI project follows Django's URL routing system with a clear hierarchical structure. Below is a comprehensive documentation of all URL patterns organized by app.

### 🌐 Main Project URLs (`inspireIA/urls.py`)

| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `admin/` | `admin.site.urls` | N/A | Django's default admin interface |
| `inspire-admin/` | `admin_site.urls` | `inspire_admin` | Custom admin interface with enhanced features |
| `''` (root) | `catalog_views.home` | `home` | Project homepage |
| `catalog/` | include `catalog.urls` | N/A | All catalog-related URLs |
| `interaction/` | include `interaction.urls` | N/A | All interaction-related URLs |
| `users/` | include `users.urls` | N/A | All user management URLs |

### 📚 Catalog App URLs (`catalog/urls.py`)

| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `''` | `CatalogView.as_view()` | `catalog` | Main catalog page with AI tools listing |
| `presentation/<uuid:id>/` | `AIToolDetailView.as_view()` | `presentationAI` | Detailed view of a specific AI tool |
| `compare/` | `compare_tools` | `compare` | Compare multiple AI tools |
| `register/` | `register_view` | `register` | User registration page |
| `login/` | `login_view` | `login` | User login page |
| `logout/` | `logout_view` | `logout` | User logout functionality |
| `profile/` | `profile_view` | `profile` | User profile page |
| `ai/<uuid:ai_id>/favorite/` | `toggle_favorite` | `toggle_favorite` | Toggle favorite status for an AI tool |

### 💬 Interaction App URLs (`interaction/urls.py`)

| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `direct-chat/` | `direct_chat` | `direct_chat` | Smart chat interface with automatic tool routing |
| `direct-chat/message/` | `direct_chat_message` | `direct_chat_message` | API endpoint for direct chat messages |
| `chat/` | `chat_selection` | `chat_selection` | Select AI tool for chatting |
| `chat/conversation/<uuid:conversation_id>/` | `chat_view` | `continue_conversation` | Continue an existing conversation |
| `chat/conversation/<uuid:conversation_id>/send/` | `send_message` | `send_message` | Send message in an existing conversation |
| `chat/<uuid:ai_id>/` | `chat_view` | `chat` | Start a new chat with specific AI tool |
| `conversations/` | `conversation_history` | `conversation_history` | View conversation history |
| `conversations/<uuid:conversation_id>/delete/` | `delete_conversation` | `delete_conversation` | Delete a conversation |
| `conversations/<uuid:conversation_id>/download/<str:format>/` | `download_conversation` | `download_conversation` | Download conversation in specified format |
| `prompts/` | `favorite_prompts` | `favorite_prompts` | View all favorite prompts |
| `prompts/ai/<uuid:ai_id>/` | `favorite_prompts` | `ai_favorite_prompts` | View favorite prompts for specific AI tool |
| `prompts/save/` | `save_favorite_prompt` | `save_favorite_prompt` | Save a new favorite prompt |
| `prompts/<uuid:prompt_id>/delete/` | `delete_favorite_prompt` | `delete_favorite_prompt` | Delete a favorite prompt |
| `share/<uuid:conversation_id>/` | `share_conversation` | `share_conversation` | Share a conversation |
| `shared/<str:access_token>/` | `view_shared_chat` | `view_shared_chat` | View a shared conversation |

### 👤 Users App URLs (`users/urls.py`)

| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `login/` | `user_login` | `login` | User login page |
| `logout/` | `user_logout` | `logout` | User logout functionality |
| `register/` | `register` | `register` | User registration page |
| `profile/` | `profile` | `profile` | User profile page |
| `admin/check-permissions/<int:user_id>/` | `check_user_permissions` | `check_user_permissions` | Admin tool to check user permissions |

### 🔄 URL Naming Conventions

The project follows these URL naming conventions:

- **Namespaced URLs**: App-specific URLs are namespaced (e.g., `catalog:home`, `interaction:chat`) for avoiding name conflicts
- **RESTful patterns**: Resource-oriented URLs with appropriate HTTP methods
- **Consistent naming**: Related functionality uses consistent naming patterns
- **Semantic URLs**: URLs are designed to be descriptive and semantic

### 🔗 URL Routing Logic

1. **Main request flow**: `inspireIA/urls.py` → App-specific urls.py → View function/class
2. **URL resolution**: Django matches URLs from top to bottom within each file
3. **Parameter capturing**: URL parameters are captured using `<type:name>` syntax
4. **Reverse URL resolution**: URLs can be reversed in templates and code using `{% url %}` and `reverse()`

### 🔍 Intelligent Search & Discovery

- **Advanced Search**: Find AI tools using natural language queries, categories, or specific capabilities
- **Smart Recommendations**: Personalized AI tool suggestions based on user history and preferences
- **Interactive Filters**: Dynamic filtering system with real-time results update
- **Visual Categories**: Intuitive category organization with visual indicators
- **Sorting Options**: Sort tools by popularity, name, or newest additions
- **Pricing Filters**: Filter tools by pricing model (free or paid)
- **Comparison View**: Side-by-side comparison of multiple AI tools
- **Detailed Tool Pages**: Comprehensive information about each tool with usage examples
- **Related Tools**: Suggestions for similar or complementary tools

### 💬 Conversational AI Integration

- **Unified Chat Interface**: Consistent experience across different AI providers
- **Multi-Modal Support**: Text, image, and hybrid conversation capabilities
- **Context Awareness**: Maintains conversation context across sessions
- **Model Selection**: Switch between different AI models within the same tool
- **Smart Routing**: Automatically routes messages to the most appropriate AI tool based on content analysis
- **Conversation History**: Browse, search, and continue previous conversations
- **Favorite Prompts**: Save and reuse effective prompts for different AI tools
- **Export Options**: Download conversations in multiple formats (JSON, TXT, CSV)
- **Sharing Capabilities**: Generate shareable links for conversations with privacy controls
- **API Integration**: Support for OpenAI, Hugging Face, and custom API integrations

### 👤 User Experience

- **Personalized Dashboard**: Customizable dashboard showing favorite tools and recent conversations
- **Dark/Light Theme**: UI theme preference with automatic system detection
- **Responsive Design**: Optimized experience on desktop, tablet, and mobile devices
- **Accessibility Focus**: WCAG compliant interface with keyboard navigation support
- **Progressive Web App**: Installable on mobile devices with offline capabilities
- **Performance Optimization**: Fast loading times with optimized assets
- **Intuitive Navigation**: Clear information architecture with breadcrumbs
- **Feedback System**: In-app notifications and status messages
- **User Onboarding**: Guided introduction for new users
- **Cross-Browser Support**: Works consistently across all modern browsers

### 🔄 Collaboration & Sharing

- **One-Click Sharing**: Generate shareable links for conversations or tool collections
- **Collaboration Spaces**: Create shared workspaces for team-based tool exploration
- **Export Options**: Download conversations in multiple formats (JSON, TXT, CSV)
- **Embedding Support**: Embed chat widgets or tool recommendations in external sites
- **Privacy Controls**: Granular control over what information is shared
- **Expiring Links**: Set time limits for shared conversation access
- **Read-Only Mode**: Share conversations without allowing modifications
- **Team Features**: Special features for educational institutions and research teams
- **Integration Options**: Connect with learning management systems
- **Citation Generation**: Create academic citations for AI-generated content

## 🛠️ Technologies

- **Backend**: Django 5.1+ (Python 3.9+)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3
- **Database**: SQLite (development), PostgreSQL (production)
- **AI Integrations**: OpenAI API, Hugging Face API, Custom API integrations
- **Authentication**: Django authentication system with custom user model
- **Logging**: Custom request logging middleware for tracking user interactions
- **Monitoring**: Sentry for error tracking and performance monitoring
- **Caching**: Redis for performance optimization
- **Task Queue**: Celery for background processing
- **Testing**: pytest for automated testing
- **CI/CD**: GitHub Actions for continuous integration and deployment
- **Containerization**: Docker and Docker Compose
- **Version Control**: Git with GitHub
- **Code Quality**: Black, isort, flake8 for code formatting and linting
- **Documentation**: Markdown with comprehensive project documentation

## 📂 Project Structure

The project consists of multiple Django apps, each with specific responsibilities:

```text
ProyectoIntegrador1/
├── catalog/                  # AI tool catalog core functionality
│   ├── migrations/           # Database migrations
│   ├── static/               # CSS, JS, images
│   │   └── catalog/
│   │       ├── css/          # Catalog-specific stylesheets
│   │       └── js/           # Catalog-specific JavaScript
│   ├── templates/            # HTML templates
│   │   └── catalog/          # Catalog-specific templates
│   │       ├── catalog.html  # Main catalog listing page
│   │       ├── PresentationAI.html # AI tool detail page
│   │       ├── compare.html  # Tool comparison page
│   │       └── compare_select.html # Tool selection for comparison
│   ├── management/
│   │   └── commands/         # Custom management commands
│   │       └── populate_ai_tools.py # Command to populate AI tools
│   ├── views/                # View modules
│   │   ├── __init__.py       # View imports
│   │   ├── ai_tools.py       # AI tool detail views
│   │   ├── auth.py           # Authentication views
│   │   ├── catalog.py        # Catalog listing views
│   │   ├── home.py           # Homepage views
│   │   └── profile.py        # User profile views
│   ├── models.py             # Database models
│   ├── urls.py               # URL patterns
│   ├── admin.py              # Admin site configuration
│   ├── apps.py               # App configuration
│   └── templatetags/         # Custom template tags
│       └── catalog_extras.py # Catalog-specific template tags
│   │   └── commands/         # Command implementations
│   ├── views/                # Modular views
│   │   ├── __init__.py      # View exports
│   │   ├── catalog.py       # Catalog listing views
│   │   └── home.py          # Homepage views
│   ├── admin.py              # Admin panel configuration
│   ├── apps.py               # App configuration
│   ├── constants.py          # Centralized constants (CATEGORIES, etc.)
│   ├── context_processors.py # Template context processors
│   ├── mixins.py             # Reusable view mixins (pagination, filtering)
│   ├── models.py             # AI tool data models
│   ├── tests.py              # Unit tests
│   ├── urls.py               # URL routing
│   ├── utils.py              # Utility functions
│   └── views.py              # View controllers
│
├── interaction/              # User-AI interaction functionality
│   ├── migrations/           # Database migrations
│   ├── static/               # Static assets
│   ├── views/                # Modular views
│   │   ├── __init__.py      # View exports
│   │   ├── chat.py          # Chat-related views
│   │   ├── conversations.py # Conversation management views
│   │   ├── favorites.py     # Favorite prompts views
│   │   └── sharing.py       # Conversation sharing views
│   │   └── interaction/
│   │       └── css/          # Interaction-specific stylesheets
│   ├── templates/            # HTML templates
│   │   └── interaction/      # Interaction-specific templates
│   │       ├── chat.html     # Main chat interface
│   │       ├── direct_chat.html # Smart routing chat interface
│   │       └── ...           # Other interaction templates
│   ├── admin.py              # Admin panel configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Conversation and message models
│   ├── tests.py              # Unit tests
│   ├── urls.py               # URL routing
│   ├── utils.py              # Utility functions for routing and formatting
│   └── views.py              # View controllers for chat functionality
│
├── users/                    # User authentication and management
│   ├── migrations/           # Database migrations
│   ├── static/               # User-specific assets
│   │   └── users/
│   │       ├── css/          # User-specific stylesheets
│   │       └── js/           # User-specific JavaScript
│   ├── templates/            # User templates
│   │   └── users/            # User-specific templates
│   ├── management/           # User management commands
│   ├── admin.py              # Admin panel configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # User forms
│   ├── models.py             # Custom user model
│   ├── tests.py              # Unit tests
│   ├── urls.py               # URL routing
│   └── views.py              # User view controllers
│
├── inspireIA/                # Project configuration
│   ├── settings/             # Environment-specific settings
│   │   ├── base.py           # Base settings for all environments
│   │   ├── development.py    # Development-specific settings
│   │   └── production.py     # Production-specific settings
│   ├── middleware.py         # Custom middleware for request logging
│   ├── storage_backends.py   # Storage configuration
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration for deployment
│   └── asgi.py               # ASGI configuration for async support
│
├── static/                   # Global static files
├── media/                    # User-uploaded files
├── logs/                     # Application logs
├── manage.py                 # Django management script
└── README.md                 # Project documentation
```

## 💾 Data Models

### AITool (catalog app)

The core model for storing information about AI tools:

```python
├── core/                    # Core functionality shared across apps
│   ├── mixins/              # Reusable view mixins
│   │   ├── __init__.py      # Mixin imports
│   │   ├── pagination.py    # Pagination mixins
│   │   └── filtering.py     # Filtering mixins
│   ├── middleware/          # Custom middleware
│   │   └── logging.py       # Request logging middleware
│   ├── templatetags/        # Global template tags
│   └── utils/               # Utility functions
│       ├── formatting.py    # Text formatting utilities
│       └── validation.py    # Data validation utilities
│
├── interaction/             # AI tool interaction functionality
│   ├── migrations/          # Database migrations
│   ├── static/              # Interaction-specific static files
│   ├── templates/           # Interaction templates
│   │   └── interaction/     # Chat and interaction templates
│   ├── views/               # View modules
│   │   ├── chat.py          # Chat interface views
│   │   └── sharing.py       # Conversation sharing views
│   ├── models.py            # Conversation and message models
│   ├── urls.py              # URL patterns
│   └── admin.py             # Admin site configuration
│
├── users/                   # User management functionality
│   ├── migrations/          # Database migrations
│   ├── templates/           # User-related templates
│   │   └── users/           # Authentication templates
│   ├── forms.py             # User forms
│   ├── models.py            # Custom user model
│   ├── urls.py              # URL patterns
│   └── admin.py             # Admin site configuration
│
├── static/                  # Global static files
│   ├── css/                 # Global CSS
│   │   ├── base.css         # Base styles
│   │   └── variables.css    # CSS variables
│   ├── js/                  # Global JavaScript
│   │   ├── main.js          # Main JavaScript file
│   │   └── utils.js         # Utility functions
│   └── images/              # Global images
│
├── templates/               # Global templates
│   ├── base.html            # Base template
│   ├── navbar.html          # Navigation bar
│   └── footer.html          # Footer template
│
├── docs/                    # Project documentation
│   ├── 01_project_overview.md # Project overview
│   ├── 02_database_models.md # Database models documentation
│   ├── 03_core_apps.md      # Core apps documentation
│   └── 04_project_configuration.md # Configuration docs
│
├── inspireIA/              # Project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
│
├── media/                  # User-uploaded files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # Project readme
```
    category = models.CharField(max_length=100)
    description = models.TextField()
    popularity = models.IntegerField()
    image = models.ImageField(upload_to='ai_images/', null=True, blank=True)
    api_type = models.CharField(
        max_length=50, 
        choices=[
            ('openai', 'OpenAI API'),
            ('huggingface', 'Hugging Face API'),
            ('custom', 'Custom Integration'),
            ('none', 'No Integration')
        ],
        default='none'
    )
    api_model = models.CharField(max_length=100, blank=True, null=True)
    api_endpoint = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
```

### CustomUser (users app)

Extended user model for authentication and user preferences:

```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, help_text="User email")
    first_name = models.CharField(max_length=255, help_text="User first name")  
    favorites = models.ManyToManyField(
        'catalog.AITool',  
        related_name='favorited_by',
        blank=True,
        help_text="User's favorite AI tools"
    )
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'first_name']
```

### Conversation & Message (interaction app)

Models for tracking user conversations with AI tools:

```python
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            null=True, blank=True, related_name='interaction_conversations')
    ai_tool = models.ForeignKey(AITool, on_delete=models.CASCADE, 
                               related_name='interaction_conversations')
    title = models.CharField(max_length=255, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Methods for message retrieval and JSON conversion
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    is_user = models.BooleanField(default=True)  # True if from user, False if from AI
    timestamp = models.DateTimeField(default=timezone.now)
```

### FavoritePrompt & SharedChat (interaction app)

Models for saving favorite prompts and sharing conversations:

```python
class FavoritePrompt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ai_tool = models.ForeignKey(AITool, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
class SharedChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                 related_name='shared_chats')
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                   null=True, blank=True, related_name='received_chats')
    is_public = models.BooleanField(default=False)
    access_token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## 🔄 Key Features Implementation

### Smart Message Routing

The application includes a smart routing system that analyzes message content and directs it to the most appropriate AI tool:

```python
def route_message_to_ai_tool(message_content):
    """
    Analyze message content and route to the most appropriate AI tool.
    """
    # Convert to lowercase for case-insensitive matching
    content_lower = message_content.lower()
    
    # Define patterns for different AI tool categories
    patterns = {
        'Image Generator': [
            r'(create|generate|make|draw|design|produce) (a|an|some)? ?(image|picture|photo|illustration|artwork|drawing)',
            # Additional patterns...
        ],
        'Video Generator': [
            r'(create|generate|make|produce) (a|an|some)? ?(video|animation|clip|movie)',
            # Additional patterns...
        ],
        # Other categories...
    }
    
    # Match patterns and select the best category
    # Return the most popular AI tool in that category
```

### Conversation Export

Users can export their conversations in multiple formats:

```python
## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository

```bash
git clone https://github.com/Mateoloperaortiz/ProyectoIntegrador1.git
cd ProyectoIntegrador1
```

2. Create a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a `.env` file in the root directory with the following variables:

```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///db.sqlite3
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

5. Run migrations

```bash
python manage.py migrate
```

6. Create a superuser

```bash
python manage.py createsuperuser
```

7. Populate the database with sample AI tools

```bash
python manage.py populate_ai_tools
```

8. Run the development server

```bash
python manage.py runserver
```

9. Access the application at http://127.0.0.1:8000/
    """
    # Format conversation based on the requested format type
    # Return formatted content, content type, and file extension
```

### Direct Chat Interface

A unified chat interface that automatically routes messages to appropriate AI tools:

```python
@login_required
def direct_chat(request):
    """View for the smart chat interface that routes messages to appropriate AI tools."""
    # Load existing conversation or start a new one
    # Render the direct chat template with conversation context
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Django 4.2+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mateoloperaortiz/ProyectoIntegrador1.git
   cd ProyectoIntegrador1
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment configuration:
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## 🔒 Environment Configuration

### Settings Structure

The project uses a modular settings approach with environment-specific configuration files:

```
inspireIA/
└── settings/
    ├── __init__.py       # Environment selection logic
    ├── base.py           # Common settings shared across all environments
    ├── development.py    # Development-specific settings
    ├── testing.py        # Testing-specific settings
    ├── production.py     # Production-specific settings
    ├── local.py          # Local overrides (gitignored)
    └── local.py.example  # Template for local.py
```

### Environment Variables

The project uses python-dotenv to load environment variables from a `.env` file. Key variables include:

- `DJANGO_ENV`: Environment to use (development, testing, production)
- `DJANGO_SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode toggle
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection URL

See [Settings Documentation](docs/settings.md) for complete details on configuration options.

### Environment Selection

The environment is selected based on the `DJANGO_ENV` environment variable in your `.env` file:

```bash
# In .env file
DJANGO_ENV=development  # Options: development, testing, production
```

No need to set `DJANGO_SETTINGS_MODULE` manually as the project handles this automatically.

## 📊 Implemented Features

### Recent Updates (March 2025)

#### Settings Module Refactoring (March 2025)
- Implemented a modular settings approach with environment-specific configuration files
- Added environment selection logic in `__init__.py` based on `DJANGO_ENV` variable
- Integrated `python-dotenv` for consistent environment variable management
- Created a testing settings file for improved test performance
- Added comprehensive settings documentation
- Enhanced security with better environment variable validation

#### Code Quality Improvements (March 2025)
- Enhanced code documentation with comprehensive docstrings across the entire codebase
- Added detailed type hints to improve IDE support and catch potential bugs early
- Improved module-level documentation with usage examples
- Standardized docstring format following PEP 257 conventions
- Added detailed parameter and return value documentation for all functions and methods

#### Direct Chat with Smart Routing
- Added a new direct chat interface that automatically routes messages to the most appropriate AI tool
- Implemented pattern matching for different AI tool categories
- Enhanced user experience with a unified chat interface
- Added support for conversation history and context preservation

#### Enhanced Conversation Sharing
- Improved the conversation sharing functionality with public and private options
- Added unique access tokens for secure sharing
- Implemented a dedicated view for shared conversations
- Added support for downloading conversations in multiple formats (JSON, TXT, CSV)

### User Management

- Custom user registration and authentication
- User profiles with favorites and history
- Email-based authentication
- Password reset and account recovery
- User activity logging and analytics

### AI Tool Catalog

- Comprehensive AI tool listings with detailed information
## 🧪 Testing

### Running Tests

```bash
python -m pytest
```

### Test Coverage

```bash
python -m pytest --cov=.
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Project Overview](docs/01_project_overview.md)
- [Database Models](docs/02_database_models.md)
- [Core Apps](docs/03_core_apps.md)
- [Project Configuration](docs/04_project_configuration.md)
- [Features and Technologies](docs/05_features_and_technologies.md)
- [Logging Guide](docs/logging_guide.md)
- [Pagination](docs/pagination.md)
- [Security](docs/security.md)
- [Settings](docs/settings.md)
- [URL Patterns](docs/url_patterns.md)
- Usage statistics and visualizations

### AI Interaction

- Real-time chat interfaces with AI tools
- Smart message routing to appropriate AI tools
- Conversation history management
- Favorite prompts saving and reuse
- Conversation sharing (public or private)
- Conversation export (JSON, TXT, CSV formats)
- Context preservation across sessions
- Prompt templates for educational scenarios
- Conversation tagging and categorization
- Custom management commands for data import/export
- Usage analytics dashboard
- Content moderation tools
- Automated status checking for integrated APIs
- Customizable notification system
- Detailed audit logs for all system activities

## 💻 Code Quality & Documentation

The project follows strict code quality standards to ensure maintainability and ease of onboarding for new developers:

### Documentation Standards
- **Comprehensive Docstrings**: All classes, methods, and functions include detailed docstrings
- **Type Hints**: Extensive use of Python type hints for better IDE support and early error detection
- **Module Documentation**: Each module includes a descriptive header explaining its purpose and usage
- **Inline Comments**: Complex algorithms and business logic include explanatory comments
- **Example Usage**: Key utilities include example usage in their documentation

### Code Style
- **PEP 8 Compliance**: All Python code follows PEP 8 style guidelines
- **Black Formatting**: Automatic code formatting with Black
- **isort**: Consistent import sorting
- **flake8**: Linting to catch potential issues

### Testing
- **pytest**: Comprehensive test suite with pytest
- **Coverage Tracking**: Monitoring of test coverage
- **CI/CD Integration**: Automated testing in the development pipeline

## 🖥️ User Interface

### Home Dashboard

The application features a modern, intuitive dashboard with:

- Personalized AI tool recommendations
- Recent conversations and saved prompts
- Quick search functionality
- Featured and trending tools
- Category exploration sections
- Latest platform announcements and updates

### Tool Discovery

- Visual card layout with tool thumbnails and key information
- Interactive filtering sidebar
- Comparison view for side-by-side evaluation
- Detailed tool presentation pages with demos
- Related tools suggestions
- User reviews and ratings section

### Chat Interface

- Clean, distraction-free conversation design
- Real-time message delivery with typing indicators
- Code block formatting with syntax highlighting
- Support for markdown rendering
- Image upload and display capabilities
- Message editing and deletion
- Conversation forking and branching
## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- Mateo Lopera Ortiz - Project Lead
- EAFIT University - Proyecto Integrador 1

## 📞 Contact

For questions or feedback, please contact:
- GitHub: [@Mateoloperaortiz](https://github.com/Mateoloperaortiz)
- Email: [your-email@example.com]
- Favorite tools and prompts management
- Shared conversations management
- Notification preferences
- Account settings and security options
- Integration with learning management systems

## 🔌 Key Endpoints

### Public Endpoints

- `/` - Home page with featured AI tools
- `/catalog/` - Browse all AI tools with filtering
- `/catalog/presentation/<uuid>/` - Detailed AI tool information
- `/catalog/compare/` - Compare AI tools side by side
- `/catalog/category/<slug>/` - Browse tools by category
- `/catalog/trending/` - Currently popular AI tools
- `/register/`, `/login/`, `/logout/` - User authentication

### Authenticated Endpoints

- `/interaction/chat/<uuid>/` - Chat with an AI tool
- `/interaction/conversations/` - View conversation history
- `/interaction/prompts/` - Manage favorite prompts
- `/interaction/share/<uuid>/` - Share conversations
- `/profile/` - User profile management
- `/profile/favorites/` - Manage favorite tools
- `/profile/settings/` - Account settings and preferences
- `/profile/notifications/` - Notification management

### API Endpoints

- `/api/v1/tools/` - List available AI tools
- `/api/v1/categories/` - List tool categories
- `/api/v1/conversations/` - Manage conversations
- `/api/v1/prompts/` - Handle favorite prompts
- `/api/v1/chat/` - Chat with AI tools programmatically

## ⚙️ Management Commands

## 🛠️ Development

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Run linting with flake8
flake8
```

### Custom Management Commands

The project includes several custom Django management commands:

- `python manage.py populate_ai_tools` - Populate database with predefined AI tools
- `python manage.py cleanup_conversations` - Remove old conversations
- `python manage.py create_test_data` - Create test data for development

## 🤝 Contributing

Contributions are welcome! Please check out our [contributing guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- Mateo Lopera Ortiz - Project Lead
- EAFIT University - Proyecto Integrador 1

## 🙏 Acknowledgements

- Django Team for the amazing web framework
- Bootstrap Team for the frontend framework
- OpenAI for API integration examples
- Hugging Face for model hosting and APIs
- EAFIT University for project guidance and support
- `python manage.py export_ai_tools` - Export AI tools to JSON
- `python manage.py import_ai_tools <file>` - Import AI tools from JSON
- `python manage.py check_api_status` - Verify status of integrated AI services
- `python manage.py update_tool_metrics` - Update usage statistics for tools

### User Management

- `python manage.py create_admin` - Create admin superuser
- `python manage.py create_test_users` - Create test user accounts
- `python manage.py setup_groups` - Configure permission groups
- `python manage.py export_user_data` - Export user data (GDPR compliant)
- `python manage.py cleanup_inactive` - Archive inactive accounts

### System Management

- `python manage.py backup_database` - Create database backup
- `python manage.py cleanup_conversations` - Archive old conversations
- `python manage.py generate_sitemap` - Create XML sitemap for SEO
- `python manage.py performance_report` - Generate system performance metrics

## 🚀 Getting Started

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/inspireai.git
   cd inspireai
   ```

2. Create a virtual environment

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment
   - Windows:

     ```bash
     venv\Scripts\activate
     ```

   - Unix/MacOS:

     ```bash
     source venv/bin/activate
     ```

4. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables

   ```bash
   cp .env.example .env
   # Edit .env with your configuration settings
   ```

6. Run migrations

   ```bash
   python manage.py migrate
   ```

7. Create a superuser

   ```bash
   python manage.py createsuperuser
   ```

8. (Optional) Populate with sample data

   ```bash
   python manage.py populate_ai_tools
   ```

9. Start the server

   ```bash
   python manage.py runserver
   ```

### Configuration

- Environment-specific configurations in `inspireIA/settings/`
- For AI API integration, configure API keys in environment variables
- Development settings in `development.py`, production in `production.py`
- Customize appearance and behavior through settings.INSPIRE_CONFIG

### Testing

- Run tests:

  ```bash
  python manage.py test
  ```

- Test specific app:

  ```bash
  python manage.py test [app_name]
  ```

- Test specific class:

  ```bash
  python manage.py test [app_name.tests.TestClassName]
  ```

- Coverage report:

  ```bash
  coverage run --source='.' manage.py test && coverage report
  ```

## 📱 Mobile Compatibility

Inspire AI is fully responsive and provides an optimized experience on mobile devices:

- Adaptive layouts for different screen sizes
- Touch-friendly interface elements
- Offline capability for viewing saved content
- Progressive Web App (PWA) features
- Native-like experience with smooth transitions

## 🔮 Future Roadmap

### Planned Enhancements

- AI tool recommendation engine based on user behavior
- Integration with more AI providers and model types
- Advanced analytics dashboard for educational insights
- Mobile app versions for iOS and Android
- Collaborative workspaces for team-based exploration
- Integration with learning management systems (LMS)
- Expanded multilingual support
- Accessibility improvements

### Community Features

- User-submitted tool reviews and ratings
- Community prompt sharing marketplace
- Educational templates and workflows
- Integration with academic citation systems
- Collaborative research tools

## 🤝 Contributing

We welcome contributions from the community! Please check out our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get involved.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- We follow PEP 8 for Python code
- ESLint configuration for JavaScript
- Black for automatic code formatting
- isort for import sorting
- Type hints throughout the codebase
- Comprehensive docstrings following PEP 257
- Pre-commit hooks for quality assurance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- EAFIT University for supporting this project
- All team members
- Open source libraries and frameworks that made this possible
- The AI research community for their groundbreaking work

## 📞 Contact

For more information about the project, contact the development team.

---

<p align="center">
  Made with ❤️ at EAFIT University | Proyecto Integrador 1 | 2025
</p>
