# Database Models and E-R Diagram

## Introduction

This document provides a comprehensive overview of the database models used in the InspireIA project. The database schema is designed to support the core functionality of the platform, including user management, AI tool catalog, and interaction features.

The database design follows these key principles:

1. **Normalization**: Tables are normalized to reduce redundancy and improve data integrity
2. **Relationship Clarity**: Clear and explicit relationships between models
3. **Type Safety**: All fields have appropriate data types with constraints
4. **Performance**: Indexes on frequently queried fields for optimal performance
5. **Extensibility**: Design allows for future expansion without major schema changes

## Entity-Relationship Diagram

The following diagram illustrates the relationships between the main entities in the database:

```
+----------------+       +----------------+       +----------------+
|   CustomUser   |       |     AITool     |       |  Conversation  |
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK) UUID   |       | id (PK) UUID   |
| username       |       | name           |       | user (FK)      |
| email          |       | provider       |       | ai_tool (FK)   |
| password       |<----->| description    |<----->| created_at     |
| is_active      |  M:N  | category       |  1:N  | updated_at     |
| date_joined    |       | endpoint       |       | title          |
| favorites (M2M)|       | popularity     |       | is_archived    |
+----------------+       | image          |       +----------------+
        |                | api_type       |               |
        |                | api_model      |               |
        |                | api_endpoint   |               |
        |                | is_featured    |               |
        |                +----------------+               |
        |                        |                        |
        |                        |                        |
        v                        v                        v
+----------------+       +----------------+       +----------------+
| FavoritePrompt |       |    Category    |       |    Message     |
+----------------+       +----------------+       +----------------+
| id (PK) UUID   |       | id (PK)        |       | id (PK) UUID   |
| user (FK)      |       | name           |       | conversation(FK)|
| prompt_text    |<----->| description    |       | content        |
| ai_tools (M2M) |       | icon           |       | is_user        |
| title          |       | slug           |       | created_at     |
| description    |       | parent (FK)    |       | tokens         |
| created_at     |       | created_at     |       | model_used     |
| updated_at     |       | updated_at     |       +----------------+
+----------------+       +----------------+               |
        |                                                 |
        |                                                 |
        v                                                 v
+----------------+                                 +----------------+
|  PromptTag     |                                 |   SharedChat   |
+----------------+                                 +----------------+
| id (PK)        |                                 | id (PK) UUID   |
| name           |                                 | conversation(FK)|
| description    |                                 | access_token   |
| prompts (M2M)  |                                 | is_public      |
| created_at     |                                 | created_at     |
| updated_at     |                                 | expires_at     |
+----------------+                                 | view_count     |
                                                  +----------------+
```

## Model Descriptions

### Users App

#### CustomUser

```python
class CustomUser(AbstractUser):
    """Extended user model with additional functionality for the InspireIA platform."""
    email: models.EmailField = models.EmailField(
        unique=True, 
        help_text="User email address used for authentication and notifications"
    )
    favorites: models.ManyToManyField = models.ManyToManyField(
        'catalog.AITool', 
        related_name='favorited_by', 
        blank=True,
        help_text="AI tools marked as favorites by this user"
    )
    profile_image: models.ImageField = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        help_text="User profile picture"
    )
    bio: models.TextField = models.TextField(
        blank=True,
        help_text="Short user biography"
    )
    preferences: models.JSONField = models.JSONField(
        default=dict,
        blank=True,
        help_text="User preferences stored as JSON"
    )
    last_active: models.DateTimeField = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of user's last activity"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]
    
    def get_favorite_tools(self) -> QuerySet:
        """Returns a queryset of user's favorite AI tools"""
        return self.favorites.all()
    
    def get_recent_conversations(self, limit: int = 5) -> QuerySet:
        """Returns user's most recent conversations"""
        return self.conversations.order_by('-updated_at')[:limit]
```

**Description**: Extends Django's AbstractUser model to provide email-based authentication and enhanced user profile functionality. This model is the central user entity that connects to conversations, favorite prompts, and AI tools.

**Key Fields**:
- **email**: Unique email address used for authentication and notifications
- **favorites**: Collection of AI tools marked as favorites by the user
- **profile_image**: Optional user profile picture
- **bio**: Optional short user biography
- **preferences**: JSON field storing user preferences (theme, notification settings, etc.)
- **last_active**: Timestamp tracking user's last activity

**Key Relationships**:
- **favorites**: Many-to-Many relationship with AITool model
- **conversations**: One-to-Many relationship with Conversation model (reverse relation)
- **favorite_prompts**: One-to-Many relationship with FavoritePrompt model (reverse relation)

**Indexes**:
- Email and username fields are indexed for faster lookup

**Methods**:
- **get_favorite_tools()**: Returns all AI tools favorited by the user
- **get_recent_conversations()**: Returns user's most recent conversations

### Catalog App

#### AITool

```python
class AITool(models.Model):
    """Model representing an AI tool in the catalog."""
    id: models.UUIDField = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for the AI tool"
    )
    name: models.CharField = models.CharField(
        max_length=100,
        help_text="Name of the AI tool"
    )
    provider: models.CharField = models.CharField(
        max_length=100,
        help_text="Company or organization that provides the AI tool"
    )
    description: models.TextField = models.TextField(
        help_text="Detailed description of the AI tool"
    )
    short_description: models.CharField = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Brief summary of the AI tool for display in listings"
    )
    category: models.ForeignKey = models.ForeignKey(
        'Category', 
        on_delete=models.CASCADE, 
        related_name='tools',
        help_text="Category the AI tool belongs to"
    )
    endpoint: models.URLField = models.URLField(
        help_text="URL for accessing the AI tool's website"
    )
    api_endpoint: models.URLField = models.URLField(
        blank=True, 
        null=True,
        help_text="URL for the AI tool's API endpoint"
    )
    api_type: models.CharField = models.CharField(
        max_length=50, 
        choices=[
            ('REST', 'REST API'),
            ('GRAPHQL', 'GraphQL API'),
            ('WEBSOCKET', 'WebSocket API'),
            ('CUSTOM', 'Custom Integration')
        ],
        default='REST',
        help_text="Type of API used by the AI tool"
    )
    api_model: models.CharField = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Specific model identifier used when calling the API"
    )
    api_key_required: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether an API key is required to use this tool"
    )
    image: models.ImageField = models.ImageField(
        upload_to='ai_tool_images/',
        null=True,
        blank=True,
        help_text="Image representing the AI tool"
    )
    popularity: models.IntegerField = models.IntegerField(
        default=0,
        help_text="Popularity score based on usage and favorites"
    )
    is_featured: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether this tool should be featured on the homepage"
    )
    is_free: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether this tool is free to use"
    )
    pricing_model: models.CharField = models.CharField(
        max_length=50,
        choices=[
            ('FREE', 'Free'),
            ('FREEMIUM', 'Freemium'),
            ('SUBSCRIPTION', 'Subscription'),
            ('PAY_PER_USE', 'Pay Per Use'),
            ('ENTERPRISE', 'Enterprise')
        ],
        default='FREEMIUM',
        help_text="Pricing model of the AI tool"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "AI Tool"
        verbose_name_plural = "AI Tools"
        ordering = ['-popularity', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['provider']),
            models.Index(fields=['category']),
            models.Index(fields=['popularity']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} by {self.provider}"
    
    def increment_popularity(self) -> None:
        """Increment the popularity score of this AI tool"""
        self.popularity += 1
        self.save(update_fields=['popularity'])
    
    def get_absolute_url(self) -> str:
        """Returns the URL to access the detail view of this AI tool"""
        return reverse('catalog:ai_tool_detail', kwargs={'id': self.id})
```

**Description**: Represents an AI tool in the catalog. Contains comprehensive information about the tool, its provider, category, API integration details, and usage statistics.

**Key Fields**:
- **id**: UUID primary key for unique identification
- **name**: Name of the AI tool
- **provider**: Company or organization that provides the tool
- **description**: Detailed description of the tool's capabilities
- **short_description**: Brief summary for display in listings
- **endpoint**: URL to the tool's website
- **api_endpoint**: URL for API access (if applicable)
- **api_type**: Type of API (REST, GraphQL, etc.)
- **api_model**: Specific model identifier for API calls
- **image**: Visual representation of the tool
- **popularity**: Usage-based score for ranking
- **is_featured**: Flag for featuring on homepage
- **is_free**: Whether the tool is free to use
- **pricing_model**: Pricing structure (Free, Freemium, etc.)

**Key Relationships**:
- **category**: Foreign Key to Category model
- **favorited_by**: Reverse relation from CustomUser.favorites (Many-to-Many)
- **conversations**: One-to-Many relationship with Conversation model (reverse relation)
- **favorite_prompts**: Many-to-Many relationship with FavoritePrompt model (reverse relation)

**Indexes**:
- Indexed fields include name, provider, category, and popularity for efficient filtering and sorting

**Methods**:
- **increment_popularity()**: Increases the popularity score
- **get_absolute_url()**: Returns the URL for the detail view

#### Category

```python
class Category(models.Model):
    """Model representing a category for AI tools."""
    name: models.CharField = models.CharField(
        max_length=50,
        help_text="Name of the category"
    )
    description: models.TextField = models.TextField(
        help_text="Detailed description of the category"
    )
    icon: models.CharField = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Font Awesome icon class for the category"
    )
    slug: models.SlugField = models.SlugField(
        unique=True,
        help_text="URL-friendly version of the category name"
    )
    parent: models.ForeignKey = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        help_text="Parent category if this is a subcategory"
    )
    order: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text="Order in which to display this category"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self) -> str:
        """Returns the URL to access the category view"""
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})
    
    def get_all_tools(self) -> QuerySet:
        """Returns all tools in this category and its subcategories"""
        tools = self.tools.all()
        for subcategory in self.subcategories.all():
            tools = tools | subcategory.get_all_tools()
        return tools
```

**Description**: Represents a category for AI tools. Used for organizing and filtering tools in the catalog. Supports hierarchical categorization through parent-child relationships.

**Key Fields**:
- **name**: Name of the category
- **description**: Detailed description of what the category encompasses
- **icon**: Font Awesome icon class for visual representation
- **slug**: URL-friendly version of the name for clean URLs
- **parent**: Optional reference to a parent category
- **order**: Position for display ordering

**Key Relationships**:
- **tools**: One-to-Many relationship with AITool model (reverse relation)
- **parent**: Self-referential Foreign Key for hierarchical categories
- **subcategories**: Reverse relation for child categories

**Indexes**:
- Indexed fields include slug and parent for efficient lookups

**Methods**:
- **get_absolute_url()**: Returns the URL for the category view
- **get_all_tools()**: Recursively collects all tools from this category and its subcategories

### Interaction App

#### Conversation

```python
class Conversation(models.Model):
    """Model representing a conversation between a user and an AI tool."""
    id: models.UUIDField = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for the conversation"
    )
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='conversations',
        help_text="User who initiated the conversation"
    )
    ai_tool: models.ForeignKey = models.ForeignKey(
        'catalog.AITool', 
        on_delete=models.CASCADE, 
        related_name='conversations',
        help_text="AI tool used in the conversation"
    )
    title: models.CharField = models.CharField(
        max_length=255, 
        blank=True,
        help_text="Title of the conversation, auto-generated if not provided"
    )
    is_archived: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether the conversation has been archived by the user"
    )
    token_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text="Total token count used in this conversation"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['ai_tool']),
            models.Index(fields=['updated_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.title or 'Untitled'} - {self.user.username} with {self.ai_tool.name}"
    
    def get_absolute_url(self) -> str:
        """Returns the URL to access the conversation detail view"""
        return reverse('interaction:conversation_detail', kwargs={'id': self.id})
    
    def get_message_count(self) -> int:
        """Returns the number of messages in this conversation"""
        return self.messages.count()
    
    def get_last_message(self) -> Optional['Message']:
        """Returns the most recent message in the conversation"""
        return self.messages.order_by('-created_at').first()
    
    def update_token_count(self) -> None:
        """Updates the total token count based on all messages"""
        self.token_count = self.messages.aggregate(Sum('tokens'))['tokens__sum'] or 0
        self.save(update_fields=['token_count'])
    
    def generate_title(self) -> None:
        """Generates a title for the conversation based on its content"""
        if not self.title and self.messages.exists():
            first_message = self.messages.filter(is_user=True).first()
            if first_message:
                # Truncate to first 50 chars or first sentence
                content = first_message.content
                title = content[:50] + ('...' if len(content) > 50 else '')
                self.title = title
                self.save(update_fields=['title'])
```

**Description**: Represents a conversation between a user and an AI tool. Contains metadata about the conversation, links to the messages exchanged, and utility methods for conversation management.

**Key Fields**:
- **id**: UUID primary key for unique identification
- **user**: Reference to the user who initiated the conversation
- **ai_tool**: Reference to the AI tool used in the conversation
- **title**: Optional title for the conversation (auto-generated if not provided)
- **is_archived**: Flag indicating whether the user has archived the conversation
- **token_count**: Running total of tokens used in the conversation
- **created_at/updated_at**: Timestamps for creation and last update

**Key Relationships**:
- **user**: Foreign Key to CustomUser model
- **ai_tool**: Foreign Key to AITool model
- **messages**: One-to-Many relationship with Message model (reverse relation)
- **shared**: One-to-One relationship with SharedChat model (reverse relation, optional)

**Indexes**:
- Indexed fields include user, ai_tool, and updated_at for efficient filtering and sorting

**Methods**:
- **get_absolute_url()**: Returns the URL for the conversation detail view
- **get_message_count()**: Returns the number of messages in the conversation
- **get_last_message()**: Returns the most recent message
- **update_token_count()**: Recalculates the total token usage
- **generate_title()**: Automatically generates a title based on conversation content

#### Message

```python
class Message(models.Model):
    """Model representing a single message within a conversation."""
    id: models.UUIDField = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for the message"
    )
    conversation: models.ForeignKey = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages',
        help_text="Conversation this message belongs to"
    )
    content: models.TextField = models.TextField(
        help_text="Content of the message"
    )
    is_user: models.BooleanField = models.BooleanField(
        default=True,
        help_text="Whether this message was sent by the user (True) or the AI (False)"
    )
    tokens: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text="Number of tokens used in this message"
    )
    model_used: models.CharField = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Specific model used to generate this message (for AI responses)"
    )
    metadata: models.JSONField = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional metadata about the message (e.g., API response details)"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_user']),
        ]
    
    def __str__(self) -> str:
        sender = "User" if self.is_user else "AI"
        return f"{sender} message in {self.conversation.title or 'Untitled'}"
    
    def save(self, *args, **kwargs) -> None:
        """Override save to update conversation token count and updated_at"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Update conversation's updated_at and token count
            self.conversation.updated_at = timezone.now()
            self.conversation.token_count += self.tokens
            self.conversation.save(update_fields=['updated_at', 'token_count'])
            
            # Generate title for new conversations
            if self.is_user and self.conversation.messages.count() <= 2:
                self.conversation.generate_title()
    
    def get_formatted_content(self) -> str:
        """Returns content formatted for display (e.g., with markdown rendering)"""
        # This is a placeholder for more complex formatting logic
        return self.content
```

**Description**: Represents a single message within a conversation. Can be from the user or the AI tool. Includes token tracking and metadata storage.

**Key Fields**:
- **id**: UUID primary key for unique identification
- **conversation**: Reference to the conversation this message belongs to
- **content**: The actual text content of the message
- **is_user**: Boolean flag indicating whether the message is from the user (True) or AI (False)
- **tokens**: Number of tokens used in this message (for usage tracking and billing)
- **model_used**: Specific AI model used to generate this response (for AI messages)
- **metadata**: JSON field for storing additional information about the message
- **created_at**: Timestamp when the message was created

**Key Relationships**:
- **conversation**: Foreign Key to Conversation model

**Indexes**:
- Indexed fields include conversation, created_at, and is_user for efficient filtering and sorting

**Methods**:
- **save()**: Overridden to update the parent conversation's token count and timestamps
- **get_formatted_content()**: Returns the message content with appropriate formatting applied

#### FavoritePrompt

```python
class FavoritePrompt(models.Model):
    """Model for storing user's favorite prompts that can be reused with AI tools."""
    id: models.UUIDField = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for the favorite prompt"
    )
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='favorite_prompts',
        help_text="User who saved this prompt"
    )
    title: models.CharField = models.CharField(
        max_length=100,
        help_text="Short title for the prompt"
    )
    prompt_text: models.TextField = models.TextField(
        help_text="The actual prompt text to be sent to AI tools"
    )
    description: models.TextField = models.TextField(
        blank=True,
        help_text="Optional description explaining the purpose of this prompt"
    )
    ai_tools: models.ManyToManyField = models.ManyToManyField(
        'catalog.AITool', 
        related_name='favorite_prompts', 
        blank=True,
        help_text="AI tools this prompt works well with"
    )
    usage_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this prompt has been used"
    )
    is_public: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether this prompt is shared publicly with other users"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Favorite Prompt"
        verbose_name_plural = "Favorite Prompts"
        ordering = ['-usage_count', '-updated_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_public']),
            models.Index(fields=['usage_count']),
        ]
    
    def __str__(self) -> str:
        return f"{self.title} ({self.user.username})"
    
    def get_absolute_url(self) -> str:
        """Returns the URL to access the favorite prompt detail view"""
        return reverse('interaction:favorite_prompt_detail', kwargs={'id': self.id})
    
    def increment_usage(self) -> None:
        """Increments the usage count for this prompt"""
        self.usage_count += 1
        self.save(update_fields=['usage_count'])
    
    def get_truncated_text(self, length: int = 50) -> str:
        """Returns a truncated version of the prompt text for display"""
        if len(self.prompt_text) <= length:
            return self.prompt_text
        return self.prompt_text[:length] + '...'
```

**Description**: Stores user's favorite prompts that can be reused with multiple AI tools. This model allows users to save, organize, and quickly access frequently used prompts.

**Key Fields**:
- **id**: UUID primary key for unique identification
- **user**: Reference to the user who saved this prompt
- **title**: Short descriptive title for the prompt
- **prompt_text**: The actual prompt text to be sent to AI tools
- **description**: Optional explanation of the prompt's purpose or use case
- **ai_tools**: Collection of AI tools this prompt works well with
- **usage_count**: Counter tracking how many times this prompt has been used
- **is_public**: Flag indicating whether this prompt is shared with other users
- **created_at/updated_at**: Timestamps for creation and last update

**Key Relationships**:
- **user**: Foreign Key to CustomUser model
- **ai_tools**: Many-to-Many relationship with AITool model
- **tags**: Many-to-Many relationship with PromptTag model (through reverse relation)

**Indexes**:
- Indexed fields include user, is_public, and usage_count for efficient filtering and sorting

**Methods**:
- **get_absolute_url()**: Returns the URL for the prompt detail view
- **increment_usage()**: Increases the usage count when the prompt is used
- **get_truncated_text()**: Returns a shortened version of the prompt for display

#### SharedChat

```python
class SharedChat(models.Model):
    """Model for managing shared conversations with access control."""
    id: models.UUIDField = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for the shared chat"
    )
    conversation: models.OneToOneField = models.OneToOneField(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='shared',
        help_text="Conversation being shared"
    )
    access_token: models.UUIDField = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        help_text="Unique token for accessing this shared conversation"
    )
    is_public: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether this conversation is publicly accessible without authentication"
    )
    allow_comments: models.BooleanField = models.BooleanField(
        default=False,
        help_text="Whether viewers can add comments to this shared conversation"
    )
    view_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this shared conversation has been viewed"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    expires_at: models.DateTimeField = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Optional expiration date after which the share becomes invalid"
    )
    
    class Meta:
        verbose_name = "Shared Chat"
        verbose_name_plural = "Shared Chats"
        indexes = [
            models.Index(fields=['access_token']),
            models.Index(fields=['is_public']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self) -> str:
        status = "Public" if self.is_public else "Private"
        return f"{status} share of {self.conversation.title or 'Untitled'}"
    
    def get_absolute_url(self) -> str:
        """Returns the URL to access this shared conversation"""
        return reverse('interaction:shared_chat', kwargs={'token': self.access_token})
    
    def is_expired(self) -> bool:
        """Checks if this share has expired"""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at
    
    def increment_view_count(self) -> None:
        """Increments the view count for this shared conversation"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def generate_new_token(self) -> None:
        """Generates a new access token, invalidating the old one"""
        self.access_token = uuid.uuid4()
        self.save(update_fields=['access_token'])
```

**Description**: Manages sharing conversations with other users or publicly. Contains access control information, expiration settings, and usage tracking.

**Key Fields**:
- **id**: UUID primary key for unique identification
- **conversation**: Reference to the conversation being shared
- **access_token**: Unique token used in the share URL for access control
- **is_public**: Flag indicating whether the conversation is publicly accessible
- **allow_comments**: Flag indicating whether viewers can add comments
- **view_count**: Counter tracking how many times the shared conversation has been viewed
- **created_at**: Timestamp when the share was created
- **expires_at**: Optional timestamp after which the share becomes invalid

**Key Relationships**:
- **conversation**: One-to-One relationship with Conversation model

**Indexes**:
- Indexed fields include access_token, is_public, and expires_at for efficient lookups

**Methods**:
- **get_absolute_url()**: Returns the URL for accessing the shared conversation
- **is_expired()**: Checks if the share has expired based on the expires_at field
- **increment_view_count()**: Increases the view count when the share is accessed
- **generate_new_token()**: Creates a new access token, invalidating the previous share link

#### PromptTag

```python
class PromptTag(models.Model):
    """Model for categorizing and organizing favorite prompts."""
    name: models.CharField = models.CharField(
        max_length=50,
        unique=True,
        help_text="Name of the tag"
    )
    description: models.TextField = models.TextField(
        blank=True,
        help_text="Optional description of what this tag represents"
    )
    prompts: models.ManyToManyField = models.ManyToManyField(
        'FavoritePrompt',
        related_name='tags',
        blank=True,
        help_text="Prompts associated with this tag"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Prompt Tag"
        verbose_name_plural = "Prompt Tags"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self) -> str:
        return self.name
    
    def get_prompt_count(self) -> int:
        """Returns the number of prompts with this tag"""
        return self.prompts.count()
```

**Description**: Provides a tagging system for categorizing and organizing favorite prompts. Allows users to group related prompts together for easier discovery and management.

**Key Fields**:
- **name**: Unique name of the tag
- **description**: Optional explanation of what the tag represents
- **prompts**: Collection of prompts associated with this tag
- **created_at/updated_at**: Timestamps for creation and last update

**Key Relationships**:
- **prompts**: Many-to-Many relationship with FavoritePrompt model

**Indexes**:
- Name field is indexed for efficient lookups

**Methods**:
- **get_prompt_count()**: Returns the number of prompts associated with this tag

## Database Schema Evolution

### Recent Changes

1. **FavoritePrompt Model Update**:
   - Changed `ai_tool` from a ForeignKey to `ai_tools` as a ManyToManyField
   - This allows prompts to be associated with multiple AI tools instead of just one
   - Added `title` and `description` fields for better organization
   - Added `usage_count` field to track popularity
   - Added `is_public` flag for sharing prompts with other users
   - Updated related serializers and views to handle the new relationship

2. **User Favorites Consolidation**:
   - Removed the redundant `UserFavorite` model
   - Consolidated user favorites into the `CustomUser` model with a direct ManyToManyField
   - This simplifies the data model and improves query performance
   - Added related methods to CustomUser for easier access to favorites

3. **Conversation and Message Enhancements**:
   - Added UUID primary keys for all conversation-related models
   - Added `token_count` tracking for usage analytics and potential billing
   - Added `is_archived` flag to Conversation model for better organization
   - Added `model_used` field to Message model to track which AI model generated responses
   - Added `metadata` JSON field to Message model for storing additional response data
   - Implemented automatic title generation for conversations

4. **SharedChat Improvements**:
   - Added `view_count` field to track popularity of shared conversations
   - Added `allow_comments` flag to enable interactive shared conversations
   - Added methods for token regeneration and expiration checking

5. **New PromptTag Model**:
   - Added a tagging system for organizing favorite prompts
   - Implemented a Many-to-Many relationship with FavoritePrompt
   - Added methods for counting and retrieving tagged prompts

6. **Category Hierarchy**:
   - Added self-referential relationship to Category model for parent-child relationships
   - Added `slug` field for SEO-friendly URLs
   - Added `order` field for custom sorting
   - Implemented recursive methods for retrieving all tools in a category and its subcategories

7. **AITool Model Expansion**:
   - Added detailed API integration fields (`api_type`, `api_model`)
   - Added pricing information fields (`is_free`, `pricing_model`)
   - Added `is_featured` flag for homepage promotion
   - Added `short_description` field for listings
   - Implemented popularity tracking and increment methods

### Migration Path

The database schema evolution is managed through Django's migration system. Key migrations include:

1. Initial model creation with basic relationships
2. Addition of sharing functionality with SharedChat model
3. Enhancement of user profiles with additional fields
4. Update of FavoritePrompt model to support multiple AI tools
5. Consolidation of user favorites into the CustomUser model

## Database Optimization

### Indexing Strategy

The database schema includes strategic indexes to optimize query performance for common operations:

1. **Primary Lookup Fields**:
   - All models have indexes on fields commonly used in WHERE clauses
   - Examples: `user`, `ai_tool`, `conversation` foreign keys

2. **Sorting Fields**:
   - Fields used for ordering results are indexed
   - Examples: `updated_at`, `created_at`, `popularity`, `name`

3. **Filtering Fields**:
   - Fields used for filtering in list views are indexed
   - Examples: `is_public`, `is_featured`, `is_archived`

4. **Unique Constraints**:
   - Unique fields have indexes automatically
   - Examples: `email`, `slug`, `access_token`

5. **Composite Indexes**:
   - For queries that filter on multiple columns simultaneously
   - Examples: `(user, is_public)`, `(category, is_featured)`

### Query Optimization

The application implements several query optimization techniques:

1. **Select Related**:
   - Uses Django's `select_related()` for foreign key relationships
   - Example: `Conversation.objects.select_related('user', 'ai_tool')`

2. **Prefetch Related**:
   - Uses Django's `prefetch_related()` for many-to-many relationships
   - Example: `AITool.objects.prefetch_related('favorited_by')`

3. **Deferred Loading**:
   - Uses `defer()` to exclude large fields when not needed
   - Example: `Message.objects.defer('metadata')`

4. **Bulk Operations**:
   - Uses `bulk_create()` and `bulk_update()` for batch operations
   - Example: `Message.objects.bulk_create(messages)`

5. **Annotated Queries**:
   - Uses annotations to perform calculations in the database
   - Example: `AITool.objects.annotate(favorite_count=Count('favorited_by'))`

### Database Migrations

The project follows these best practices for database migrations:

1. **Incremental Changes**:
   - Small, focused migrations instead of large schema changes
   - Each migration addresses a specific model change

2. **Data Migrations**:
   - Separate schema changes from data transformations
   - Use Django's `RunPython` for complex data migrations

3. **Zero Downtime Migrations**:
   - Avoid locking tables during migrations
   - Add columns as nullable first, then fill data, then add constraints

4. **Testing Migrations**:
   - All migrations are tested in staging before production
   - Includes performance testing for potentially slow migrations

5. **Rollback Plans**:
   - Each migration has a documented rollback procedure
   - Critical migrations include pre-written reverse migrations

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
