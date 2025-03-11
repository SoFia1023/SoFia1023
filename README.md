# Inspire AI Project

![Inspire AI Logo](https://img.shields.io/badge/Inspire%20AI-Empowering%20Education-blue?style=for-the-badge)

> *Empowering students and educators through intelligent technology discovery*

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/Mateoloperaortiz/ProyectoIntegrador1)

---

## ✨ Overview

Inspire AI is a web application designed to help students and teachers discover, access, search, and interact with Artificial Intelligence tools. The project is part of "Proyecto Integrador 1" at EAFIT University. It provides a centralized platform for AI tool discovery, comparison, and interaction through chat interfaces.

![Project Banner](https://img.shields.io/badge/EAFIT-Proyecto%20Integrador%201-orange?style=for-the-badge)

## 🎯 Main Objectives

- Provide a centralized catalog of AI tools
- Facilitate searching and filtering tools by category and functionality
- Offer detailed information about each tool
- Allow interaction with AI tools through integrated chat interfaces
- Enable users to save favorite tools and prompts
- Provide conversation history, sharing, and export functionality

## 🚀 Features Highlight

### 🔍 Intelligent Search & Discovery

- **Advanced Search**: Find AI tools using natural language queries, categories, or specific capabilities
- **Smart Recommendations**: Personalized AI tool suggestions based on user history and preferences
- **Interactive Filters**: Dynamic filtering system with real-time results update
- **Visual Categories**: Intuitive category organization with visual indicators

### 💬 Conversational AI Integration

- **Unified Chat Interface**: Consistent experience across different AI providers
- **Multi-Modal Support**: Text, image, and hybrid conversation capabilities
- **Context Awareness**: Maintains conversation context across sessions
- **Model Selection**: Switch between different AI models within the same tool
- **Smart Routing**: Automatically routes messages to the most appropriate AI tool based on content analysis

### 👤 User Experience

- **Personalized Dashboard**: Customizable dashboard showing favorite tools and recent conversations
- **Dark/Light Theme**: UI theme preference with automatic system detection
- **Responsive Design**: Optimized experience on desktop, tablet, and mobile devices
- **Accessibility Focus**: WCAG compliant interface with keyboard navigation support

### 🔄 Collaboration & Sharing

- **One-Click Sharing**: Generate shareable links for conversations or tool collections
- **Collaboration Spaces**: Create shared workspaces for team-based tool exploration
- **Export Options**: Download conversations in multiple formats (JSON, TXT, CSV)
- **Embedding Support**: Embed chat widgets or tool recommendations in external sites

## 🛠️ Technologies

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5.3
- **Database**: SQLite (development), PostgreSQL (production)
- **AI Integrations**: OpenAI API, Hugging Face API, Custom API integrations
- **Authentication**: Django authentication system with custom user model
- **Logging**: Custom request logging middleware for tracking user interactions
- **Monitoring**: Sentry for error tracking and performance monitoring

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
│   │   ├── base.html         # Base template for the entire application
│   │   └── catalog/          # Catalog-specific templates
│   ├── management/           # Custom management commands
│   │   └── commands/         # Command implementations
│   ├── admin.py              # Admin panel configuration
│   ├── apps.py               # App configuration
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
class AITool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    endpoint = models.URLField()
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
def format_conversation_for_download(conversation, format_type='json'):
    """
    Format a conversation for download in the specified format.
    
    Supports JSON, TXT, and CSV formats.
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

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## 🔒 Environment Configuration

The project uses environment-specific settings files:

- `base.py`: Common settings for all environments
- `development.py`: Development-specific settings
- `production.py`: Production-specific settings

To switch between environments, set the `DJANGO_SETTINGS_MODULE` environment variable:

```bash
# Development (default)
export DJANGO_SETTINGS_MODULE=inspireIA.settings.development

# Production
export DJANGO_SETTINGS_MODULE=inspireIA.settings.production
```

## 📊 Implemented Features

### Recent Updates (March 2025)

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
- Search and filtering by category, popularity, and features
- Tool comparison functionality
- Favorite tools management
- Trending and recommended tools sections
- Rating and review system
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

The project includes several custom Django management commands:

### AI Tool Management

- `python manage.py populate_ai_tools` - Populate database with predefined AI tools
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
