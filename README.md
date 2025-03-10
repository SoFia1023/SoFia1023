# Inspire AI Project

![Inspire AI Logo](https://img.shields.io/badge/Inspire%20AI-Empowering%20Education-blue?style=for-the-badge)

> *Empowering students and educators through intelligent technology discovery*

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/yourusername/inspireai)

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

### 👤 User Experience

- **Personalized Dashboard**: Customizable dashboard showing favorite tools and recent conversations
- **Dark/Light Theme**: UI theme preference with automatic system detection
- **Responsive Design**: Optimized experience on desktop, tablet, and mobile devices
- **Accessibility Focus**: WCAG compliant interface with keyboard navigation support

### 🔄 Collaboration & Sharing

- **One-Click Sharing**: Generate shareable links for conversations or tool collections
- **Collaboration Spaces**: Create shared workspaces for team-based tool exploration
- **Export Options**: Download conversations in multiple formats (PDF, JSON, Markdown)
- **Embedding Support**: Embed chat widgets or tool recommendations in external sites

## 🛠️ Technologies

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5.3
- **Database**: SQLite (development), PostgreSQL (production)
- **AI Integrations**: OpenAI API, Hugging Face API, Custom API integrations
- **Authentication**: Django Allauth with social authentication support
- **Real-time**: Django Channels with WebSockets for chat functionality
- **Caching**: Redis for performance optimization
- **Search**: Elasticsearch for advanced search capabilities
- **Monitoring**: Sentry for error tracking and performance monitoring

## 📂 Project Structure

The project consists of multiple Django apps, each with specific responsibilities:

```text
ProyectoIntegrador1/
├── catalog/            # AI tool catalog core functionality
│   ├── migrations/     # Database migrations
│   ├── static/         # CSS, JS, images
│   ├── templates/      # HTML templates
│   ├── management/     # Custom management commands
│   ├── admin.py        # Admin panel configuration
│   ├── mixins.py       # Reusable view mixins (pagination, filtering)
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
    ├── middleware.py   # Custom middleware for request logging and tracking
    ├── urls.py         # Main URL configuration
    └── wsgi.py         # WSGI configuration for deployment
```

## 📊 Core Models

### AITool (catalog app)

- Stores information about AI tools including name, provider, category, description
- Supports API integration configurations (OpenAI, Hugging Face, custom)
- Tracks popularity and featured status
- Customizable metadata for specialized tool capabilities
- Versioning support for tracking tool updates over time

### CustomUser (users app)

- Extends Django's AbstractUser
- Email-based authentication
- Stores user preferences and favorites
- Usage analytics tracking with privacy controls
- Role-based access with customizable permissions

### Conversation & Message (interaction app)

- Tracks user conversations with AI tools
- Stores message history with timestamps
- Supports conversation export and sharing
- Message tagging for better organization
- Custom conversation metadata for educational use cases

### FavoritePrompt & SharedChat (interaction app)

- Allows users to save and reuse favorite prompts
- Enables sharing conversations publicly or with specific users
- Prompt categories and tags for better organization
- Collaborative prompt editing with version history

## 🌟 Implemented Features

### Recent Updates (July 2023)

#### User Interaction Tracking
- Added middleware for tracking user interactions with the platform
- Implemented request logging with timing information
- Tracks authenticated user activity for analytics
- Logs request paths, methods, status codes, and processing times
- Helps identify performance bottlenecks and popular features

#### Enhanced Pagination
- Added PaginationMixin for consistent pagination across the application
- Improved navigation with smart page range display
- Better handling of edge cases (invalid page numbers, empty pages)
- Visual indicators for current page and total pages
- Consistent pagination UI across all listing pages

### User Management

- Custom user registration and authentication
- User profiles with favorites and history
- Permission-based access control with user groups
- Social authentication (Google, Microsoft)
- Two-factor authentication for enhanced security
- Password reset and account recovery
- Email verification and notifications
- User activity logging and analytics

### AI Tool Catalog

- Comprehensive AI tool listings with detailed information
- Search and filtering by category, popularity, and features
- Tool comparison functionality
- Favorite tools management
- Trending and recommended tools sections
- New tools notification system
- Rating and review system
- Usage statistics and visualizations

### AI Interaction

- Real-time chat interfaces with AI tools
- Conversation history management
- Favorite prompts saving and reuse
- Conversation sharing (public or private)
- Conversation export (JSON, text formats)
- Multi-modal support (text, images)
- Context preservation across sessions
- Prompt templates for educational scenarios
- Conversation tagging and categorization
- Advanced system prompts management
- Message reactions and annotations

### Administration

- Enhanced admin interface for content management
- Bulk operations for AI tools and user data
- Permission management and monitoring
- Custom management commands for data import/export
- Usage analytics dashboard
- Content moderation tools
- Automated status checking for integrated APIs
- Customizable notification system
- Detailed audit logs for all system activities

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
- Context and system prompt management panel

### User Profile

- Activity timeline with usage statistics
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
- Pre-commit hooks for quality assurance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- EAFIT University for supporting this project
- All team members
- Open source libraries and frameworks that made this possible
- The AI research community for their groundbreaking work

## 📞 Contact

For more information about the project, contact the development.

---

<p align="center">
  Made with ❤️ at EAFIT University | Proyecto Integrador 1 | 2025
</p>
