# URL Patterns and Routing Documentation

This document provides a comprehensive overview of the URL routing system in the Inspire AI project.

## Table of Contents

1. [Overview](#overview)
2. [URL Structure](#url-structure)
3. [Main Project URLs](#main-project-urls)
4. [Catalog App URLs](#catalog-app-urls)
5. [Interaction App URLs](#interaction-app-urls)
6. [Users App URLs](#users-app-urls)
7. [URL Naming Conventions](#url-naming-conventions)
8. [URL Routing Logic](#url-routing-logic)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)

## Overview

The Inspire AI project follows Django's URL routing system with a clear hierarchical structure. URL patterns are defined in `urls.py` files within each app and are included in the main project's URL configuration.

## URL Structure

The URL structure follows a hierarchical pattern:

```
/                           # Root URL (Home)
├── admin/                  # Django admin interface
├── inspire-admin/          # Custom admin interface
├── catalog/                # Catalog app
│   ├── presentation/<id>/  # AI tool details
│   ├── compare/            # Compare tools
│   └── ...
├── interaction/            # Interaction app
│   ├── direct-chat/        # Smart chat interface
│   ├── chat/               # Regular chat interface
│   ├── conversations/      # Conversation history
│   ├── prompts/            # Favorite prompts
│   └── ...
└── users/                  # Users app
    ├── login/              # User login
    ├── register/           # User registration
    └── ...
```

## Main Project URLs

The main URL configuration is defined in `inspireIA/urls.py`:

| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `admin/` | `admin.site.urls` | N/A | Django's default admin interface |
| `inspire-admin/` | `admin_site.urls` | `inspire_admin` | Custom admin interface with enhanced features |
| `''` (root) | `catalog_views.home` | `home` | Project homepage |
| `catalog/` | include `catalog.urls` | N/A | All catalog-related URLs |
| `interaction/` | include `interaction.urls` | N/A | All interaction-related URLs |
| `users/` | include `users.urls` | N/A | All user management URLs |

## Catalog App URLs

The catalog app URLs are defined in `catalog/urls.py`:

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

### View Details

- `CatalogView`: Class-based view that displays the catalog of AI tools
- `AIToolDetailView`: Class-based view for detailed information about a specific AI tool
- `compare_tools`: Function-based view for comparing multiple AI tools
- Authentication views (`register_view`, `login_view`, `logout_view`, `profile_view`): Handle user authentication

## Interaction App URLs

The interaction app URLs are defined in `interaction/urls.py`:

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

### View Details

- `direct_chat`: Smart chat interface that automatically routes messages to appropriate AI tools
- `direct_chat_message`: API endpoint for handling messages in the smart chat interface
- `chat_view`: Handles both new and existing conversations with specific AI tools
- `conversation_history`: Displays the user's conversation history
- `favorite_prompts`: Manages favorite prompts for quick access
- `share_conversation`: Enables sharing conversations with other users

## Users App URLs

The users app URLs are defined in `users/urls.py`:

| URL Pattern | View | Name | Description |
|------------|------|------|-------------|
| `login/` | `user_login` | `login` | User login page |
| `logout/` | `user_logout` | `logout` | User logout functionality |
| `register/` | `register` | `register` | User registration page |
| `profile/` | `profile` | `profile` | User profile page |
| `admin/check-permissions/<int:user_id>/` | `check_user_permissions` | `check_user_permissions` | Admin tool to check user permissions |

### View Details

- `user_login`: Handles user authentication
- `user_logout`: Handles user logout
- `register`: Handles user registration
- `profile`: Displays and manages user profile information
- `check_user_permissions`: Admin tool for checking user permissions

## URL Naming Conventions

The project follows these URL naming conventions:

- **Namespaced URLs**: App-specific URLs are namespaced (e.g., `catalog:home`, `interaction:chat`) for avoiding name conflicts
- **RESTful patterns**: Resource-oriented URLs with appropriate HTTP methods
- **Consistent naming**: Related functionality uses consistent naming patterns
- **Semantic URLs**: URLs are designed to be descriptive and semantic

### Examples

- Resource listing: `conversations/`
- Resource detail: `conversations/<uuid:conversation_id>/`
- Resource action: `conversations/<uuid:conversation_id>/delete/`
- API endpoints: `direct-chat/message/`

## URL Routing Logic

1. **Main request flow**: `inspireIA/urls.py` → App-specific urls.py → View function/class
2. **URL resolution**: Django matches URLs from top to bottom within each file
3. **Parameter capturing**: URL parameters are captured using `<type:name>` syntax
   - Common types: `str`, `int`, `uuid`, `slug`, `path`
4. **Reverse URL resolution**: URLs can be reversed in templates and code using `{% url %}` and `reverse()`

### Example URL Resolution Flow

For a request to `/interaction/chat/conversation/123e4567-e89b-12d3-a456-426614174000/`:

1. Main `urls.py` matches `interaction/` and includes `interaction.urls`
2. `interaction/urls.py` matches `chat/conversation/<uuid:conversation_id>/` and routes to `chat_view`
3. `chat_view` receives `conversation_id` as a parameter with value `123e4567-e89b-12d3-a456-426614174000`

## Best Practices

1. **Use namespaces**: Always use app namespaces to avoid URL name conflicts
2. **Consistent patterns**: Follow consistent URL patterns across the project
3. **Semantic URLs**: Use descriptive, semantic URLs that reflect the resource hierarchy
4. **Type checking**: Use appropriate parameter types (`int`, `uuid`, etc.) for URL parameters
5. **Order matters**: Place more specific URL patterns before more general ones
6. **Reverse resolution**: Always use reverse URL resolution (`reverse()` or `{% url %}`) instead of hardcoding URLs

## Common Patterns

### Resource URLs

- List: `/resources/`
- Detail: `/resources/<id>/`
- Create: `/resources/create/` or `/resources/new/`
- Edit: `/resources/<id>/edit/`
- Delete: `/resources/<id>/delete/`

### API Endpoints

- List/Create: `/api/resources/`
- Retrieve/Update/Delete: `/api/resources/<id>/`
- Custom actions: `/api/resources/<id>/<action>/`

### Authentication URLs

- Login: `/users/login/` or `/login/`
- Logout: `/users/logout/` or `/logout/`
- Register: `/users/register/` or `/register/`
- Profile: `/users/profile/` or `/profile/`
