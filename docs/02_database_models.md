# Database Models and E-R Diagram

## Entity-Relationship Diagram

```
+----------------+       +----------------+       +----------------+
|   CustomUser   |       |     AITool     |       |  Conversation  |
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| username       |       | name           |       | user (FK)      |
| email          |       | provider       |       | ai_tool (FK)   |
| password       |<----->| description    |<----->| created_at     |
| is_active      |  M:N  | category       |  1:N  | updated_at     |
| date_joined    |       | api_endpoint   |       | title          |
+----------------+       | popularity     |       +----------------+
        |                | created_at     |               |
        |                | updated_at     |               |
        |                +----------------+               |
        |                        |                        |
        |                        |                        |
        v                        v                        v
+----------------+       +----------------+       +----------------+
| FavoritePrompt |       |    Category    |       |    Message     |
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| user (FK)      |       | name           |       | conversation(FK)|
| prompt_text    |<----->| description    |       | content        |
| ai_tools (M2M) |       | icon           |       | is_user        |
| created_at     |       | created_at     |       | created_at     |
| updated_at     |       | updated_at     |       | tokens         |
+----------------+       +----------------+       +----------------+
                                                         |
                                                         |
                                                         v
                                                  +----------------+
                                                  |   SharedChat   |
                                                  +----------------+
                                                  | id (PK)        |
                                                  | conversation(FK)|
                                                  | access_token   |
                                                  | is_public      |
                                                  | created_at     |
                                                  | expires_at     |
                                                  +----------------+
```

## Model Descriptions

### Users App

#### CustomUser

```python
class CustomUser(AbstractUser):
    email: models.EmailField = models.EmailField(unique=True, help_text="User email")
    favorites: models.ManyToManyField = models.ManyToManyField('catalog.AITool', related_name='favorited_by', blank=True)
    
    # Additional fields and methods
```

**Description**: Extends Django's AbstractUser model to provide email-based authentication and direct relationship with favorite AI tools. This model is the central user entity that connects to conversations, favorite prompts, and AI tools.

**Key Relationships**:
- **favorites**: Many-to-Many relationship with AITool model, allowing users to save their favorite AI tools directly.

### Catalog App

#### AITool

```python
class AITool(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    provider: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()
    category: models.ForeignKey = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='tools')
    api_endpoint: models.URLField = models.URLField(blank=True, null=True)
    api_key_required: models.BooleanField = models.BooleanField(default=False)
    popularity: models.IntegerField = models.IntegerField(default=0)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    # Additional fields and methods
```

**Description**: Represents an AI tool in the catalog. Contains information about the tool, its provider, category, and API integration details.

**Key Relationships**:
- **category**: Foreign Key to Category model
- **favorited_by**: Reverse relation from CustomUser.favorites (Many-to-Many)
- **conversations**: One-to-Many relationship with Conversation model
- **favorite_prompts**: Many-to-Many relationship with FavoritePrompt model

#### Category

```python
class Category(models.Model):
    name: models.CharField = models.CharField(max_length=50)
    description: models.TextField = models.TextField()
    icon: models.CharField = models.CharField(max_length=50, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    # Additional fields and methods
```

**Description**: Represents a category for AI tools. Used for organizing and filtering tools in the catalog.

**Key Relationships**:
- **tools**: One-to-Many relationship with AITool model

### Interaction App

#### Conversation

```python
class Conversation(models.Model):
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    ai_tool: models.ForeignKey = models.ForeignKey('catalog.AITool', on_delete=models.CASCADE, related_name='conversations')
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    title: models.CharField = models.CharField(max_length=100, blank=True)
    
    # Additional fields and methods
```

**Description**: Represents a conversation between a user and an AI tool. Contains metadata about the conversation and links to the messages exchanged.

**Key Relationships**:
- **user**: Foreign Key to CustomUser model
- **ai_tool**: Foreign Key to AITool model
- **messages**: One-to-Many relationship with Message model
- **shared_chat**: One-to-One relationship with SharedChat model (optional)

#### Message

```python
class Message(models.Model):
    conversation: models.ForeignKey = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content: models.TextField = models.TextField()
    is_user: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    tokens: models.IntegerField = models.IntegerField(default=0)
    
    # Additional fields and methods
```

**Description**: Represents a single message within a conversation. Can be from the user or the AI tool.

**Key Relationships**:
- **conversation**: Foreign Key to Conversation model

#### FavoritePrompt

```python
class FavoritePrompt(models.Model):
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt_text: models.TextField = models.TextField()
    ai_tools: models.ManyToManyField = models.ManyToManyField('catalog.AITool', related_name='favorite_prompts', blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    # Additional fields and methods
```

**Description**: Stores user's favorite prompts that can be used with multiple AI tools. This model has been updated to use a ManyToManyField for AI tools instead of a ForeignKey, allowing prompts to be associated with multiple AI tools.

**Key Relationships**:
- **user**: Foreign Key to CustomUser model
- **ai_tools**: Many-to-Many relationship with AITool model, allowing a prompt to be associated with multiple AI tools

#### SharedChat

```python
class SharedChat(models.Model):
    conversation: models.OneToOneField = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name='shared')
    access_token: models.UUIDField = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_public: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    expires_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    
    # Additional fields and methods
```

**Description**: Manages sharing conversations with other users or publicly. Contains access control information and expiration settings.

**Key Relationships**:
- **conversation**: One-to-One relationship with Conversation model

## Database Schema Evolution

### Recent Changes

1. **FavoritePrompt Model Update**:
   - Changed `ai_tool` from a ForeignKey to `ai_tools` as a ManyToManyField
   - This allows prompts to be associated with multiple AI tools instead of just one
   - Updated related serializers and views to handle the new relationship

2. **User Favorites Consolidation**:
   - Removed the redundant `UserFavorite` model
   - Consolidated user favorites into the `CustomUser` model with a direct ManyToManyField
   - This simplifies the data model and improves query performance

### Migration Path

The database schema evolution is managed through Django's migration system. Key migrations include:

1. Initial model creation with basic relationships
2. Addition of sharing functionality with SharedChat model
3. Enhancement of user profiles with additional fields
4. Update of FavoritePrompt model to support multiple AI tools
5. Consolidation of user favorites into the CustomUser model

## Database Optimization

1. **Indexes**:
   - Primary keys are automatically indexed
   - Foreign keys are indexed for faster joins
   - Additional indexes on frequently queried fields

2. **Query Optimization**:
   - Use of `select_related` and `prefetch_related` to reduce database queries
   - Optimized admin queries with custom `get_queryset` methods
   - Pagination for large result sets

3. **Data Integrity**:
   - Appropriate `on_delete` behaviors for foreign keys
   - Validation at the model level
   - Constraints enforced at the database level

## Future Schema Considerations

1. **User Permissions Enhancement**:
   - More granular permission system for different user roles
   - Integration with Django's permission system

2. **AI Tool Versioning**:
   - Track changes to AI tools over time
   - Allow conversations with specific versions of tools

3. **Advanced Analytics**:
   - Additional models for tracking user behavior and preferences
   - Enhanced metrics for AI tool performance and popularity
