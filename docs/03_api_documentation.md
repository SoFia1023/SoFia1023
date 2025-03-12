# API Documentation

## Introduction

This document provides comprehensive documentation for the InspireIA API. The API allows developers to interact programmatically with the InspireIA platform, enabling integration with external applications and services.

## API Overview

The InspireIA API follows RESTful principles and uses standard HTTP methods:

- **GET**: Retrieve resources
- **POST**: Create new resources
- **PUT/PATCH**: Update existing resources
- **DELETE**: Remove resources

All API endpoints return responses in JSON format and use standard HTTP status codes to indicate success or failure.

## Authentication

### Token Authentication

The API uses token-based authentication. To authenticate, include the token in the Authorization header:

```
Authorization: Token your_api_token_here
```

### Obtaining a Token

To obtain an API token, make a POST request to the token endpoint:

```
POST /api/token/
```

Request body:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "token": "your_api_token_here"
}
```

## Rate Limiting

API requests are subject to rate limiting to ensure fair usage and system stability:

- **Authenticated requests**: 100 requests per minute
- **Unauthenticated requests**: 20 requests per minute

Rate limit headers are included in all API responses:

- `X-RateLimit-Limit`: Maximum number of requests allowed in the current period
- `X-RateLimit-Remaining`: Number of requests remaining in the current period
- `X-RateLimit-Reset`: Time when the rate limit will reset (Unix timestamp)

## API Endpoints

### AI Tools

#### List AI Tools

```
GET /api/tools/
```

Query parameters:
- `category`: Filter by category ID
- `provider`: Filter by provider name
- `search`: Search term for name and description
- `is_free`: Filter by free tools (true/false)
- `page`: Page number for pagination
- `page_size`: Number of items per page

Response:
```json
{
    "count": 100,
    "next": "http://example.com/api/tools/?page=2",
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "GPT-4",
            "provider": "OpenAI",
            "description": "Advanced language model for text generation and analysis",
            "short_description": "State-of-the-art language model",
            "category": {
                "id": 1,
                "name": "Language Models",
                "slug": "language-models"
            },
            "endpoint": "https://openai.com/gpt-4",
            "api_endpoint": "https://api.openai.com/v1/chat/completions",
            "api_type": "REST",
            "api_key_required": true,
            "popularity": 1250,
            "is_free": false,
            "pricing_model": "PAY_PER_USE",
            "created_at": "2023-01-15T12:00:00Z",
            "updated_at": "2023-06-20T15:30:00Z"
        },
        // More tools...
    ]
}
```

#### Get AI Tool Details

```
GET /api/tools/{tool_id}/
```

Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "GPT-4",
    "provider": "OpenAI",
    "description": "Advanced language model for text generation and analysis...",
    "short_description": "State-of-the-art language model",
    "category": {
        "id": 1,
        "name": "Language Models",
        "slug": "language-models"
    },
    "endpoint": "https://openai.com/gpt-4",
    "api_endpoint": "https://api.openai.com/v1/chat/completions",
    "api_type": "REST",
    "api_model": "gpt-4",
    "api_key_required": true,
    "popularity": 1250,
    "is_free": false,
    "pricing_model": "PAY_PER_USE",
    "created_at": "2023-01-15T12:00:00Z",
    "updated_at": "2023-06-20T15:30:00Z"
}
```

#### Compare AI Tools

```
GET /api/tools/compare/?ids=id1,id2,id3
```

Response:
```json
{
    "tools": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "GPT-4",
            "provider": "OpenAI",
            "category": "Language Models",
            "is_free": false,
            "pricing_model": "PAY_PER_USE",
            "api_key_required": true
        },
        {
            "id": "660e8400-e29b-41d4-a716-446655440001",
            "name": "Claude 2",
            "provider": "Anthropic",
            "category": "Language Models",
            "is_free": false,
            "pricing_model": "SUBSCRIPTION",
            "api_key_required": true
        }
    ],
    "comparison": {
        "features": [
            {
                "name": "pricing_model",
                "values": {
                    "550e8400-e29b-41d4-a716-446655440000": "PAY_PER_USE",
                    "660e8400-e29b-41d4-a716-446655440001": "SUBSCRIPTION"
                }
            },
            // More feature comparisons...
        ]
    }
}
```

### Categories

#### List Categories

```
GET /api/categories/
```

Query parameters:
- `parent`: Filter by parent category ID
- `page`: Page number for pagination
- `page_size`: Number of items per page

Response:
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Language Models",
            "description": "AI tools focused on natural language processing and generation",
            "slug": "language-models",
            "icon": "fa-comments",
            "parent": null,
            "subcategories": [
                {
                    "id": 2,
                    "name": "Text Generation",
                    "slug": "text-generation"
                },
                {
                    "id": 3,
                    "name": "Translation",
                    "slug": "translation"
                }
            ],
            "tool_count": 25
        },
        // More categories...
    ]
}
```

#### Get Category Details

```
GET /api/categories/{category_id}/
```

Response:
```json
{
    "id": 1,
    "name": "Language Models",
    "description": "AI tools focused on natural language processing and generation",
    "slug": "language-models",
    "icon": "fa-comments",
    "parent": null,
    "subcategories": [
        {
            "id": 2,
            "name": "Text Generation",
            "slug": "text-generation"
        },
        {
            "id": 3,
            "name": "Translation",
            "slug": "translation"
        }
    ],
    "tools": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "GPT-4",
            "provider": "OpenAI",
            "short_description": "State-of-the-art language model"
        },
        // More tools...
    ]
}
```

### User Management

#### User Profile

```
GET /api/users/profile/
```

Response:
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "date_joined": "2023-01-01T10:00:00Z",
    "bio": "AI enthusiast and developer",
    "favorite_tools_count": 5,
    "conversations_count": 20
}
```

#### Update User Profile

```
PATCH /api/users/profile/
```

Request body:
```json
{
    "bio": "AI researcher and Python developer",
    "preferences": {
        "theme": "dark",
        "notifications_enabled": true
    }
}
```

Response:
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "date_joined": "2023-01-01T10:00:00Z",
    "bio": "AI researcher and Python developer",
    "preferences": {
        "theme": "dark",
        "notifications_enabled": true
    },
    "favorite_tools_count": 5,
    "conversations_count": 20
}
```

### Conversations

#### List User Conversations

```
GET /api/conversations/
```

Query parameters:
- `ai_tool`: Filter by AI tool ID
- `is_archived`: Filter archived conversations (true/false)
- `page`: Page number for pagination
- `page_size`: Number of items per page

Response:
```json
{
    "count": 20,
    "next": "http://example.com/api/conversations/?page=2",
    "previous": null,
    "results": [
        {
            "id": "770e8400-e29b-41d4-a716-446655440000",
            "title": "Project planning with AI",
            "ai_tool": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "GPT-4",
                "provider": "OpenAI"
            },
            "message_count": 12,
            "token_count": 2500,
            "is_archived": false,
            "created_at": "2023-06-15T14:30:00Z",
            "updated_at": "2023-06-15T15:00:00Z"
        },
        // More conversations...
    ]
}
```

#### Get Conversation Details

```
GET /api/conversations/{conversation_id}/
```

Response:
```json
{
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "title": "Project planning with AI",
    "ai_tool": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "GPT-4",
        "provider": "OpenAI"
    },
    "messages": [
        {
            "id": "880e8400-e29b-41d4-a716-446655440000",
            "content": "Can you help me plan a software project?",
            "is_user": true,
            "tokens": 10,
            "created_at": "2023-06-15T14:30:00Z"
        },
        {
            "id": "990e8400-e29b-41d4-a716-446655440000",
            "content": "I'd be happy to help you plan a software project! Let's break this down into steps...",
            "is_user": false,
            "tokens": 150,
            "model_used": "gpt-4",
            "created_at": "2023-06-15T14:30:15Z"
        },
        // More messages...
    ],
    "token_count": 2500,
    "is_archived": false,
    "created_at": "2023-06-15T14:30:00Z",
    "updated_at": "2023-06-15T15:00:00Z"
}
```

#### Create New Conversation

```
POST /api/conversations/
```

Request body:
```json
{
    "ai_tool_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Research on renewable energy",
    "initial_message": "I need information about recent advances in solar energy technology."
}
```

Response:
```json
{
    "id": "aa0e8400-e29b-41d4-a716-446655440000",
    "title": "Research on renewable energy",
    "ai_tool": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "GPT-4",
        "provider": "OpenAI"
    },
    "messages": [
        {
            "id": "bb0e8400-e29b-41d4-a716-446655440000",
            "content": "I need information about recent advances in solar energy technology.",
            "is_user": true,
            "tokens": 12,
            "created_at": "2023-06-20T09:00:00Z"
        },
        {
            "id": "cc0e8400-e29b-41d4-a716-446655440000",
            "content": "There have been several significant advances in solar energy technology recently...",
            "is_user": false,
            "tokens": 200,
            "model_used": "gpt-4",
            "created_at": "2023-06-20T09:00:15Z"
        }
    ],
    "token_count": 212,
    "is_archived": false,
    "created_at": "2023-06-20T09:00:00Z",
    "updated_at": "2023-06-20T09:00:15Z"
}
```

#### Add Message to Conversation

```
POST /api/conversations/{conversation_id}/messages/
```

Request body:
```json
{
    "content": "What about advancements in energy storage for solar systems?"
}
```

Response:
```json
{
    "id": "dd0e8400-e29b-41d4-a716-446655440000",
    "content": "What about advancements in energy storage for solar systems?",
    "is_user": true,
    "tokens": 10,
    "created_at": "2023-06-20T09:15:00Z"
}
```

#### Archive Conversation

```
PATCH /api/conversations/{conversation_id}/
```

Request body:
```json
{
    "is_archived": true
}
```

Response:
```json
{
    "id": "770e8400-e29b-41d4-a716-446655440000",
    "title": "Project planning with AI",
    "is_archived": true,
    "updated_at": "2023-06-20T10:00:00Z"
}
```

### Favorite Prompts

#### List Favorite Prompts

```
GET /api/favorite-prompts/
```

Query parameters:
- `ai_tool`: Filter by AI tool ID
- `is_public`: Filter public prompts (true/false)
- `page`: Page number for pagination
- `page_size`: Number of items per page

Response:
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "ee0e8400-e29b-41d4-a716-446655440000",
            "title": "Project Requirements Gathering",
            "prompt_text": "I need to gather requirements for a software project that will...",
            "description": "Prompt for gathering comprehensive project requirements",
            "ai_tools": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "GPT-4"
                },
                {
                    "id": "660e8400-e29b-41d4-a716-446655440001",
                    "name": "Claude 2"
                }
            ],
            "tags": [
                "project-management",
                "requirements"
            ],
            "usage_count": 8,
            "is_public": false,
            "created_at": "2023-05-10T11:00:00Z",
            "updated_at": "2023-06-15T14:00:00Z"
        },
        // More prompts...
    ]
}
```

#### Create Favorite Prompt

```
POST /api/favorite-prompts/
```

Request body:
```json
{
    "title": "Code Review Assistant",
    "prompt_text": "Please review the following code and suggest improvements...",
    "description": "Prompt for getting AI assistance with code reviews",
    "ai_tool_ids": [
        "550e8400-e29b-41d4-a716-446655440000"
    ],
    "tags": [
        "coding",
        "review"
    ],
    "is_public": false
}
```

Response:
```json
{
    "id": "ff0e8400-e29b-41d4-a716-446655440000",
    "title": "Code Review Assistant",
    "prompt_text": "Please review the following code and suggest improvements...",
    "description": "Prompt for getting AI assistance with code reviews",
    "ai_tools": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "GPT-4"
        }
    ],
    "tags": [
        "coding",
        "review"
    ],
    "usage_count": 0,
    "is_public": false,
    "created_at": "2023-06-20T11:00:00Z",
    "updated_at": "2023-06-20T11:00:00Z"
}
```

## Error Handling

All API errors follow a consistent format:

```json
{
    "error": {
        "code": "error_code",
        "message": "Human-readable error message",
        "details": {
            // Additional error details if available
        }
    }
}
```

Common error codes:

- `authentication_failed`: Invalid or missing authentication
- `permission_denied`: Authenticated user lacks required permissions
- `not_found`: Requested resource does not exist
- `validation_error`: Invalid request data
- `rate_limit_exceeded`: Too many requests in a given time period

## Versioning

The API uses versioning to ensure backward compatibility. The current version is v1, which is included in the URL path:

```
/api/v1/tools/
```

## Webhooks

InspireIA supports webhooks for real-time notifications about events. To register a webhook:

```
POST /api/webhooks/
```

Request body:
```json
{
    "url": "https://your-app.com/webhook-endpoint",
    "events": ["conversation.created", "message.created"],
    "secret": "your_webhook_secret"
}
```

Response:
```json
{
    "id": "gg0e8400-e29b-41d4-a716-446655440000",
    "url": "https://your-app.com/webhook-endpoint",
    "events": ["conversation.created", "message.created"],
    "created_at": "2023-06-20T12:00:00Z"
}
```

## SDK and Client Libraries

Official client libraries are available for:

- Python: [inspireai-python](https://github.com/inspireai/inspireai-python)
- JavaScript: [inspireai-js](https://github.com/inspireai/inspireai-js)

## API Changelog

### v1.2.0 (2023-06-15)

- Added support for conversation archiving
- Added token count tracking for conversations and messages
- Improved filtering options for AI tools

### v1.1.0 (2023-04-10)

- Added webhooks for real-time notifications
- Added support for favorite prompts tags
- Enhanced user profile endpoints

### v1.0.0 (2023-01-15)

- Initial API release
