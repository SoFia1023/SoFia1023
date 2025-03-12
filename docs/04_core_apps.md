# Core Apps

## 1. Catalog App

**Purpose**: Manages the AI tool catalog, including tool listings, search, filtering, and comparison functionality.

### Key Files

- `models.py`: Defines the AITool model with all necessary fields and relationships
- `views/ai_tools.py`: Contains views for catalog browsing, tool details, and comparison
- `views/categories.py`: Manages category-related views and filtering
- `views/search.py`: Implements search functionality across AI tools
- `urls.py`: URL routing for catalog functionality
- `admin.py`: Admin panel configuration for catalog models with customized interfaces
- `mixins.py`: Reusable view mixins (pagination, filtering, sorting)
- `context_processors.py`: Provides AI categories to all templates
- `utils.py`: Utility functions for AI tool operations, data processing, and API integrations

### Models

- `AITool`: Stores information about AI tools including name, provider, category, description, API integration details, and popularity metrics
- `Category`: Represents categories for organizing AI tools

### Key Views

- `HomeView`: Renders the home page with featured and popular AI tools
- `AIToolListView`: Class-based view for browsing the AI tool catalog with filtering and sorting
- `AIToolDetailView`: Displays detailed information about a specific AI tool
- `CompareToolsView`: Allows comparison between multiple AI tools
- `SearchView`: Provides search functionality across the AI tool catalog
- `CategoryListView`: Displays all available categories
- `CategoryDetailView`: Shows AI tools within a specific category

### Templates

- `home.html`: Home page with featured tools and categories
- `tool_list.html`: Paginated list of AI tools with filtering options
- `tool_detail.html`: Detailed view of a single AI tool
- `compare.html`: Side-by-side comparison of multiple AI tools
- `search_results.html`: Search results page
- `category_list.html`: List of all categories
- `category_detail.html`: AI tools within a specific category

### URL Patterns

```python
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tools/', views.AIToolListView.as_view(), name='tool_list'),
    path('tools/<uuid:tool_id>/', views.AIToolDetailView.as_view(), name='tool_detail'),
    path('compare/', views.CompareToolsView.as_view(), name='compare_tools'),
    path('search/', views.SearchView.as_view(), name='search_tools'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:category_slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
```

## 2. Interaction App

**Purpose**: Manages user interactions with AI tools, including conversations, messages, favorite prompts, and sharing functionality.

### Key Files

- `models.py`: Defines models for conversations, messages, favorite prompts, and shared chats
- `views/chat.py`: Contains views for chat interface and message handling
- `views/favorites.py`: Manages favorite prompts functionality
- `views/sharing.py`: Handles conversation sharing features
- `urls.py`: URL routing for interaction functionality
- `utils.py`: Utilities for processing messages, integrating with AI APIs, and formatting responses
- `admin.py`: Admin panel configuration for interaction models
- `templatetags/interaction_extras.py`: Custom template tags for interaction templates

### Models

- `Conversation`: Represents a conversation between a user and an AI tool
- `Message`: Represents a single message within a conversation (from user or AI)
- `FavoritePrompt`: Stores user's favorite prompts that can be used with multiple AI tools
- `SharedChat`: Manages sharing conversations with other users or publicly

### Key Views

- `ChatView`: Renders the chat interface for a specific AI tool
- `MessageView`: Handles sending and receiving messages in a conversation
- `FavoritePromptsView`: Lists and manages user's favorite prompts
- `SaveFavoritePromptView`: Creates new favorite prompts
- `SharedChatView`: Displays shared conversations
- `ShareConversationView`: Handles sharing conversations with others

### Templates

- `chat.html`: Chat interface for interacting with AI tools
- `conversation_list.html`: List of user's conversations
- `favorites.html`: User's favorite prompts
- `shared.html`: Shared conversation view

### URL Patterns

```python
urlpatterns = [
    path('chat/<uuid:ai_id>/', views.ChatView.as_view(), name='chat'),
    path('conversations/', views.ConversationListView.as_view(), name='conversation_list'),
    path('conversations/<uuid:conversation_id>/', views.ChatView.as_view(), name='conversation_detail'),
    path('messages/send/', views.MessageView.as_view(), name='send_message'),
    path('favorites/', views.FavoritePromptsView.as_view(), name='favorite_prompts'),
    path('favorites/save/', views.SaveFavoritePromptView.as_view(), name='save_favorite_prompt'),
    path('share/<uuid:conversation_id>/', views.ShareConversationView.as_view(), name='share_conversation'),
    path('shared/<uuid:access_token>/', views.SharedChatView.as_view(), name='shared_chat'),
]
```

## 3. Users App

**Purpose**: Manages user authentication, registration, profile management, and permissions.

### Key Files

- `models.py`: Defines the CustomUser model extending Django's AbstractUser
- `views/auth.py`: Contains views for user registration, login, and logout
- `views/dashboard.py`: Implements the user dashboard with tabs for overview, profile, and security
- `views/profile.py`: Manages user profile editing and settings
- `forms.py`: User-related forms for registration, login, profile editing
- `urls.py`: URL routing for user functionality
- `admin.py`: Admin panel configuration for user models
- `management/commands/setup_groups.py`: Command for setting up permission groups

### Models

- `CustomUser`: Extends Django's AbstractUser with additional fields and methods, including direct M2M relationship with AITool for favorites

### Key Views

- `RegisterView`: Handles user registration
- `LoginView`: Handles user login
- `LogoutView`: Handles user logout
- `DashboardView`: Consolidated view with tabs for overview, profile, and security settings
- `PasswordChangeView`: Handles password changes
- `EmailChangeView`: Handles email changes

### Templates

- `register.html`: User registration form
- `login.html`: User login form
- `dashboard.html`: User dashboard with tabs
- `profile.html`: User profile editing form
- `password_change.html`: Password change form
- `email_change.html`: Email change form

### URL Patterns

```python
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('email/change/', views.EmailChangeView.as_view(), name='email_change'),
]
```

## 4. API App

**Purpose**: Provides a RESTful API for interacting with the application programmatically.

### Key Files

- `views/catalog.py`: API views for catalog functionality
- `views/interaction.py`: API views for interaction functionality
- `views/users.py`: API views for user functionality
- `serializers/catalog.py`: Serializers for catalog models
- `serializers/interaction.py`: Serializers for interaction models
- `serializers/users.py`: Serializers for user models
- `urls.py`: URL routing for API endpoints
- `permissions.py`: Custom permissions for API access control

### Key Endpoints

- `/api/catalog/tools/`: List and detail endpoints for AI tools
- `/api/catalog/categories/`: Endpoints for tool categories
- `/api/interaction/conversations/`: Endpoints for managing conversations
- `/api/interaction/messages/`: Endpoints for sending and receiving messages
- `/api/interaction/favorites/`: Endpoints for managing favorite prompts
- `/api/interaction/shared/`: Endpoints for shared conversations
- `/api/users/profile/`: Endpoints for user profile management
- `/api/users/favorites/`: Endpoints for user favorites

### Serializers

- `AIToolSerializer`: Serializes AITool model data
- `CategorySerializer`: Serializes Category model data
- `ConversationSerializer`: Serializes Conversation model data
- `MessageSerializer`: Serializes Message model data
- `FavoritePromptSerializer`: Serializes FavoritePrompt model data, including the list of associated AI tools
- `SharedChatSerializer`: Serializes SharedChat model data
- `UserSerializer`: Serializes CustomUser model data

### URL Patterns

```python
urlpatterns = [
    path('catalog/', include([
        path('tools/', views.AIToolListAPIView.as_view(), name='api_tool_list'),
        path('tools/<uuid:tool_id>/', views.AIToolDetailAPIView.as_view(), name='api_tool_detail'),
        path('categories/', views.CategoryListAPIView.as_view(), name='api_category_list'),
        path('categories/<slug:category_slug>/', views.CategoryDetailAPIView.as_view(), name='api_category_detail'),
    ])),
    path('interaction/', include([
        path('conversations/', views.ConversationListAPIView.as_view(), name='api_conversation_list'),
        path('conversations/<uuid:conversation_id>/', views.ConversationDetailAPIView.as_view(), name='api_conversation_detail'),
        path('messages/', views.MessageListAPIView.as_view(), name='api_message_list'),
        path('messages/<uuid:message_id>/', views.MessageDetailAPIView.as_view(), name='api_message_detail'),
        path('favorites/', views.FavoritePromptListAPIView.as_view(), name='api_favorite_prompt_list'),
        path('favorites/<uuid:prompt_id>/', views.FavoritePromptDetailAPIView.as_view(), name='api_favorite_prompt_detail'),
        path('shared/', views.SharedChatListAPIView.as_view(), name='api_shared_chat_list'),
        path('shared/<uuid:access_token>/', views.SharedChatDetailAPIView.as_view(), name='api_shared_chat_detail'),
    ])),
    path('users/', include([
        path('profile/', views.UserProfileAPIView.as_view(), name='api_user_profile'),
        path('favorites/', views.UserFavoritesAPIView.as_view(), name='api_user_favorites'),
    ])),
]
```

## Recent Changes and Updates

### FavoritePrompt Model Update

The `FavoritePrompt` model has been updated to allow prompts to work with multiple AI tools by changing the relationship from a ForeignKey to a ManyToManyField:

**Before**:
```python
class FavoritePrompt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    ai_tool = models.ForeignKey('catalog.AITool', on_delete=models.CASCADE, related_name='favorite_prompts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**After**:
```python
class FavoritePrompt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    ai_tools = models.ManyToManyField('catalog.AITool', related_name='favorite_prompts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

This change required updates to:
- `FavoritePromptSerializer` to handle the new ManyToManyField relationship
- API views to filter prompts based on the new relationship
- Admin interface to display the list of associated AI tools

### User Favorites Consolidation

The redundant `UserFavorite` model has been removed, consolidating user favorites into the `CustomUser` model:

**Before**:
```python
class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_favorites')
    ai_tool = models.ForeignKey('catalog.AITool', on_delete=models.CASCADE, related_name='user_favorites')
    created_at = models.DateTimeField(auto_now_add=True)
```

**After**:
```python
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, help_text="User email")
    favorites = models.ManyToManyField('catalog.AITool', related_name='favorited_by', blank=True)
```

This change simplifies the data model and improves query performance by eliminating an unnecessary join table.

### Dashboard Consolidation

The user profile and dashboard functionality has been consolidated into a single dashboard view with tabs for different sections (overview, profile, security). This approach:

- Reduces redundancy
- Improves user experience
- Follows the DRY (Don't Repeat Yourself) principle

The implementation uses query parameters to control which tab is active and redirects old profile URLs to the appropriate dashboard tabs.
