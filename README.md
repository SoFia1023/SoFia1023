# Inspire AI Platform

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

## 🚀 Features Highlight

### 🔍 AI Tool Discovery

- **Advanced Search**: Find AI tools using natural language queries, categories, or specific capabilities
- **Smart Recommendations**: Personalized AI tool suggestions based on user history and preferences
- **Interactive Filters**: Dynamic filtering system with real-time results update
- **Visual Categories**: Intuitive category organization with visual indicators
- **Comparison View**: Side-by-side comparison of multiple AI tools
- **Detailed Tool Pages**: Comprehensive information about each tool with usage examples
- **Related Tools**: Suggestions for similar or complementary tools

### 💬 Conversational AI Integration

- **Unified Chat Interface**: Consistent experience across different AI providers
- **Multi-Modal Support**: Text, image, and hybrid conversation capabilities
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
- **Intuitive Navigation**: Clear information architecture with breadcrumbs

### 🔄 Collaboration & Sharing

- **One-Click Sharing**: Generate shareable links for conversations or tool collections
- **Privacy Controls**: Granular control over what information is shared
- **Expiring Links**: Set time limits for shared conversation access
- **Read-Only Mode**: Share conversations without allowing modifications
- **Team Features**: Special features for educational institutions and research teams

## 🔄 Latest Updates (2025)

### Settings Module Refactoring

- Implemented a modular settings approach with environment-specific configuration files
- Added environment selection logic based on `DJANGO_ENV` variable
- Enhanced security with better environment variable validation

### Code Quality Improvements

- Enhanced code documentation with comprehensive docstrings
- Added detailed type hints to improve IDE support
- Standardized docstring format following PEP 257 conventions

### Direct Chat with Smart Routing

- Added a unified chat interface that automatically routes messages to appropriate AI tools
- Implemented pattern matching for different AI tool categories
- Enhanced user experience with context preservation

### Enhanced Conversation Sharing

- Improved conversation sharing with public and private options
- Added unique access tokens for secure sharing
- Implemented expiration for shared conversations

## 📂 Project Structure

The project follows a modular architecture with separate Django apps for distinct functionality:

```
ProyectoIntegrador1/
├── catalog/           # AI tool catalog core functionality
│   ├── models.py      # AITool model and related models
│   ├── views/         # Modular views for catalog functionality
│   └── templates/     # Catalog-specific templates
│
├── interaction/       # User-AI interaction functionality
│   ├── models.py      # Conversation and message models
│   ├── views/         # Chat, sharing, and conversation views
│   └── templates/     # Chat interface templates
│
├── users/             # User authentication and management
│   ├── models.py      # Custom user model
│   ├── views/         # Auth and profile views
│   └── templates/     # User authentication templates
│
├── core/              # Shared functionality across apps
│   ├── middleware/    # Request logging middleware
│   └── mixins/        # Reusable view mixins
│
├── api/               # REST API interfaces
│   └── serializers/   # JSON serialization for models
│
├── inspireIA/         # Project configuration
│   ├── settings/      # Environment-specific settings
│   └── urls.py        # Main URL routing
│
├── docs/              # Project documentation
├── static/            # Global static files
├── media/             # User-uploaded files
└── manage.py          # Django management script
```

## 💾 Key Data Models

### AITool (catalog app)

Central model for storing information about AI tools with categories, descriptions, API integration details, and popularity metrics.

### CustomUser (users app)

Extended user model with email authentication, favorite tools, conversation history, and profile information.

### Conversation & Message (interaction app)

Models for tracking user conversations with AI tools, storing message history, and metadata.

### FavoritePrompt & SharedChat (interaction app)

Models for saving favorite prompts and sharing conversations with expiration controls and access tokens.

## 🛠️ Technologies

- **Backend**: Django 5.1+ (Python 3.9+)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3
- **Database**: SQLite (development), PostgreSQL (production)
- **AI Integrations**: OpenAI API, Hugging Face API, Custom API integrations
- **Authentication**: Django authentication system with custom user model
- **Logging**: Custom request logging middleware for tracking user interactions
- **Monitoring**: Sentry for error tracking and performance monitoring
- **Testing**: pytest for automated testing
- **Code Quality**: Black, isort, flake8 for code formatting and linting

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
DJANGO_ENV=development
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
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

9. Access the application at <http://127.0.0.1:8000/>

## 🧭 URL Patterns

### Main URLs

- `/` - Home page with featured AI tools
- `/catalog/` - Browse all AI tools with filtering
- `/catalog/presentation/<uuid>/` - Detailed AI tool information
- `/catalog/compare/` - Compare AI tools side by side

### Interaction URLs

- `/interaction/direct-chat/` - Smart chat interface with automatic tool routing
- `/interaction/chat/<uuid>/` - Chat with a specific AI tool
- `/interaction/conversations/` - View conversation history
- `/interaction/prompts/` - Manage favorite prompts
- `/interaction/share/<uuid>/` - Share conversations

### User URLs

- `/users/login/` - User login
- `/users/register/` - User registration
- `/users/profile/` - User profile management

## ⚙️ Management Commands

### Content Management

- `populate_ai_tools` - Add sample AI tools to database
- `export_ai_tools` - Export AI tools to JSON
- `import_ai_tools` - Import AI tools from JSON
- `fetch_ai_tool_logos` - Download logos for AI tools

### User Management

- `create_admin` - Create admin user
- `create_test_users` - Add test users to the system
- `setup_groups` - Configure permission groups

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Project Overview](docs/01_project_overview.md)
- [Database Models](docs/02_database_models.md)
- [API Documentation](docs/03_api_documentation.md)
- [Core Apps](docs/04_core_apps.md)
- [Features and Technologies](docs/05_features_and_technologies.md)
- [Project Configuration](docs/06_project_configuration.md)
- [Logging Guide](docs/logging_guide.md)
- [Security](docs/security.md)
- [URL Patterns](docs/url_patterns.md)

## 🔮 Future Roadmap

- AI tool recommendation engine based on user behavior
- Integration with more AI providers and model types
- Advanced analytics dashboard for educational insights
- Mobile app versions for iOS and Android
- Collaborative workspaces for team-based exploration
- Integration with learning management systems
- Expanded multilingual support

## 🤝 Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get involved.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- Mateo Lopera Ortiz
- Maria Mercedes Olaya Lopez
- Sofia Acosta Pareja

## 🙏 Acknowledgements

- EAFIT University for project guidance and support

---

<p align="center">
  Made with ❤️ at EAFIT University | Proyecto Integrador 1 | 2025
</p>
