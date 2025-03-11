# Project Configuration and Component Interactions

## InspireIA App (Project Configuration)

**Purpose**: Contains project-wide settings, URL configuration, and middleware.

### Key Files

- `settings/base.py`: Base settings for all environments
- `settings/development.py`: Development-specific settings
- `settings/production.py`: Production-specific settings
- `urls.py`: Main URL configuration
- `middleware.py`: Custom middleware for request processing
- `admin.py`: Custom admin site configuration with dashboard
- `wsgi.py`: WSGI configuration for deployment
- `asgi.py`: ASGI configuration for async capabilities

### Settings Structure

The project uses a split settings approach to manage different environments:

1. **Base Settings** (`base.py`):
   - Common settings shared across all environments
   - Installed apps, middleware, templates, authentication
   - Database configuration (abstract)
   - Static and media files configuration
   - Internationalization settings

2. **Development Settings** (`development.py`):
   - Debug mode enabled
   - Local database configuration (SQLite)
   - Django Debug Toolbar configuration
   - Simplified email backend
   - No HTTPS enforcement

3. **Production Settings** (`production.py`):
   - Debug mode disabled
   - PostgreSQL database configuration
   - HTTPS enforcement
   - Production-ready email backend
   - Caching configuration
   - Logging configuration

### URL Configuration

The main `urls.py` file includes URL patterns from all apps and sets up admin, static, and media URLs:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('users/', include('users.urls')),
    path('interaction/', include('interaction.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Custom Admin Dashboard

The project includes a custom admin dashboard in `admin.py` that provides:

- Overview of system statistics
- Recent activity tracking
- Quick access to common admin tasks
- Custom admin views for data visualization

## Component Diagram

```text
+----------------+     +----------------+     +----------------+
|    Users       |     |    Catalog     |     |  Interaction   |
+----------------+     +----------------+     +----------------+
| - Authentication|<--->| - Tool Listing |<--->| - Chat Interface|
| - Registration  |     | - Search       |     | - Messages     |
| - Profile       |     | - Filtering    |     | - Favorites    |
| - Dashboard     |     | - Comparison   |     | - Sharing      |
+-------^----------     +-------^----------     +-------^----------
        |                      |                      |
        |                      |                      |
        v                      v                      v
+----------------+     +----------------+     +----------------+
|      API       |<--->|    Database    |<--->|  External APIs |
+----------------+     +----------------+     +----------------+
| - REST Endpoints|     | - Django ORM   |     | - OpenAI      |
| - Serializers   |     | - Models       |     | - Hugging Face|
| - Authentication|     | - Migrations   |     | - Custom APIs |
+----------------+     +----------------+     +----------------+
```

## Component Interactions

### 1. Users ↔ Catalog

- User authentication for personalized catalog views
- Direct M2M relationship for favoriting AI tools
- User-specific tool recommendations
- Tool filtering based on user preferences

**Code Example**:
```python
# In users/models.py
class CustomUser(AbstractUser):
    favorites = models.ManyToManyField('catalog.AITool', related_name='favorited_by', blank=True)

# In catalog/views/ai_tools.py
class AIToolListView(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Mark favorites for the current user
            for tool in queryset:
                tool.is_favorite = tool in self.request.user.favorites.all()
        return queryset
```

### 2. Users ↔ Interaction

- User authentication for conversations
- Creating and managing favorite prompts that work across multiple AI tools
- Sharing conversations with other users
- Dashboard with conversation history and analytics

**Code Example**:
```python
# In interaction/views/favorites.py
class FavoritePromptsView(LoginRequiredMixin, ListView):
    model = FavoritePrompt
    template_name = 'interaction/favorites.html'
    context_object_name = 'favorite_prompts'
    
    def get_queryset(self):
        return FavoritePrompt.objects.filter(user=self.request.user)
```

### 3. Catalog ↔ Interaction

- Selecting AI tools for conversations
- Tool-specific prompt suggestions
- Tool metadata for chat interface
- Favorite prompts can be associated with multiple AI tools

**Code Example**:
```python
# In interaction/views/chat.py
class ChatView(LoginRequiredMixin, DetailView):
    model = AITool
    template_name = 'interaction/chat.html'
    pk_url_kwarg = 'ai_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ai_tool = self.get_object()
        # Get favorite prompts for this tool
        context['favorite_prompts'] = FavoritePrompt.objects.filter(
            user=self.request.user,
            ai_tools=ai_tool
        )
        return context
```

### 4. API ↔ All Components

- RESTful access to all functionality
- Authentication and permissions
- Data serialization and validation
- Consistent response formats and error handling

**Code Example**:
```python
# In api/views/interaction.py
class FavoritePromptListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        prompts = FavoritePrompt.objects.filter(user=request.user)
        serializer = FavoritePromptSerializer(prompts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FavoritePromptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### 5. External APIs ↔ Interaction

- Sending prompts to AI services
- Receiving and processing responses
- API key management and rate limiting
- Handling different API formats and requirements

**Code Example**:
```python
# In interaction/utils.py
def send_to_ai_service(message, ai_tool):
    """Send a message to the appropriate AI service based on the AI tool."""
    if ai_tool.provider.lower() == 'openai':
        return send_to_openai(message, ai_tool)
    elif ai_tool.provider.lower() == 'huggingface':
        return send_to_huggingface(message, ai_tool)
    else:
        return send_to_custom_api(message, ai_tool)
```

### 6. Users App ↔ Other Apps

- Authentication and authorization through Django's auth system
- User preferences and favorites stored directly in CustomUser model
- Consolidated dashboard with tabs for different functionality
- Profile data for personalization across the application

**Code Example**:
```python
# In users/views/dashboard.py
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get active tab from query parameter, default to 'overview'
        active_tab = self.request.GET.get('tab', 'overview')
        context['active_tab'] = active_tab
        
        # Common data for all tabs
        context['user'] = user
        
        # Tab-specific data
        if active_tab == 'overview':
            context['recent_conversations'] = user.conversations.order_by('-updated_at')[:5]
            context['favorite_tools'] = user.favorites.all()
            context['favorite_prompts'] = FavoritePrompt.objects.filter(user=user)[:5]
        elif active_tab == 'profile':
            context['profile_form'] = UserProfileForm(instance=user)
        elif active_tab == 'security':
            context['password_form'] = PasswordChangeForm(user=user)
            context['email_form'] = EmailChangeForm(instance=user)
            
        return context
```

## Data Flow

### User Registration and Authentication

1. User submits registration form
2. System validates input and creates CustomUser instance
3. User receives confirmation email
4. User logs in with email and password
5. System authenticates and creates session
6. User is redirected to dashboard with overview tab

### AI Tool Discovery

1. User browses catalog or searches for tools
2. System queries database based on filters/search
3. Results are paginated and displayed
4. User can sort, filter, or compare tools
5. User can favorite tools directly through M2M relationship
6. Favorited tools appear in user's dashboard

### Conversation with AI Tool

1. User selects an AI tool to chat with
2. System creates a new Conversation instance linked to user and tool
3. User sends a message (stored as Message)
4. System processes message and sends to appropriate AI API
5. AI response is received and stored as Message
6. Conversation is updated and response displayed
7. User can continue conversation or save prompts as favorites
8. Favorite prompts can be associated with multiple AI tools

### Sharing Conversations

1. User selects a conversation to share
2. User chooses sharing options (public or specific users)
3. System creates SharedChat instance with access token
4. System generates sharing link with secure token
5. Recipients can access conversation via link
6. Public shares are accessible to anyone with the link
7. Private shares require authentication

## Security Considerations

1. **Authentication**
   - Email-based authentication with Django's password hashing
   - Session management with secure cookies
   - Password reset functionality with time-limited secure tokens
   - CSRF protection on all forms

2. **Authorization**
   - Permission-based access control using Django's auth system
   - Object-level permissions for shared resources
   - Role-based access for admin functionality
   - Custom permission groups for different user types

3. **API Security**
   - Token-based authentication for API access
   - Rate limiting to prevent abuse
   - Input validation and sanitization
   - Proper error handling with appropriate status codes

4. **Data Protection**
   - Sensitive data encryption
   - API keys stored securely in environment variables
   - HTTPS for all communications
   - Database connection security

5. **External API Integration**
   - Secure handling of API keys
   - Validation of responses
   - Error handling for API failures
   - Timeouts and retry mechanisms
