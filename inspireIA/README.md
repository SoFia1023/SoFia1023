# InspireIA Admin Customizations

This document outlines the customizations made to the Django admin interface for the InspireIA platform.

## Custom Admin Site

We've created a custom admin site with the following features:

- **Improved Organization**: Models are grouped into logical categories
- **Enhanced UI**: Dashboard-style interface with statistics
- **Custom Actions**: Bulk actions for common tasks
- **Optimized Queries**: Improved performance with prefetch_related and select_related

## Admin URL

The custom admin site is available at:
- `/inspire-admin/` - Custom admin interface
- `/admin/` - Standard Django admin (for backward compatibility)

## Model Organization

Models are organized into the following groups:

1. **Authentication and Authorization**
   - Users
   - Groups
   - Permissions

2. **Catalog**
   - AI Tools
   - User Favorites

3. **User Interactions**
   - Conversations
   - Messages
   - Favorite Prompts
   - Shared Chats

## Search Fields

Each model has customized search fields to make finding content easier:

- **AI Tools**: Search by name, provider, description, or category
- **Users**: Search by username, email, or first name
- **Conversations**: Search by title, username, or AI tool name
- **Messages**: Search by content, conversation title, or username

## Filters

Common filters have been added to each model:

- **AI Tools**: Filter by category, API type, featured status, or provider
- **Users**: Filter by staff status, superuser status, groups, or active status
- **Conversations**: Filter by AI tool, creation date, or update date
- **Messages**: Filter by user/AI, timestamp, or conversation AI tool

## Admin Actions

Custom admin actions have been added for common tasks:

### AI Tools
- ✨ Feature selected AI tools
- ⬇️ Unfeature selected AI tools
- 📈 Increase popularity by 10
- 🔄 Reset popularity to 0
- 🔄 Duplicate selected AI tools

### Users
- ✅ Activate selected users
- ❌ Deactivate selected users
- 👤 Add to Regular Users group
- 📊 Add to Content Managers group
- 🔑 Add to Administrators group
- 🗑️ Remove from all groups
- 📄 Export users to CSV
- 👔 Grant staff status
- 👕 Revoke staff status

### Groups
- 📄 Export permissions to CSV
- 📋 Copy permissions to selected groups

### Conversations
- 📤 Export to JSON
- 📄 Export to CSV
- ⭐ Mark as important
- 📦 Archive conversations

## Dashboard

The custom admin dashboard includes:

- **Statistics**: User count, AI tool count, conversation count, message count
- **Grouped Models**: Models organized into logical groups
- **Recent Actions**: List of recent admin actions

## Performance Optimizations

The admin views have been optimized for performance:

- **Prefetch Related**: Reduces database queries for related objects
- **Select Related**: Joins related tables in a single query
- **Optimized Queries**: Custom querysets for better performance

## Usage

To use the custom admin site:

1. Log in with an admin account at `/inspire-admin/`
2. Navigate through the organized model groups
3. Use the search fields, filters, and actions to manage content
4. View statistics on the dashboard

## Common Admin Tasks

### Managing AI Tools
- **Feature/Unfeature AI Tools**: Select AI tools and use the "Feature selected AI tools" or "Unfeature selected AI tools" actions
- **Adjust Popularity**: Use "Increase popularity by 10" or "Reset popularity to 0" actions
- **Create Copies**: Use "Duplicate selected AI tools" to create copies of existing tools

### Managing User Permissions
- **Assign Users to Groups**: Select users and use the "Add to X group" actions
- **Manage Staff Status**: Use "Grant staff status" or "Revoke staff status" actions
- **Activate/Deactivate Users**: Use "Activate selected users" or "Deactivate selected users" actions
- **Export User Data**: Use "Export users to CSV" to download user information

### Managing Conversations
- **Export Conversation Data**: Select conversations and use "Export to JSON" or "Export to CSV" actions
- **Organize Conversations**: Use "Mark as important" or "Archive conversations" actions

### Managing Groups and Permissions
- **Export Group Permissions**: Select groups and use "Export permissions to CSV" action
- **Copy Permissions Between Groups**: Select source and target groups, then use "Copy permissions to selected groups" action 