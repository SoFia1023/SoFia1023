# User Groups and Permissions

This document outlines the user groups and their permissions in the InspireIA platform.

## User Groups

### 1. Administrators

Administrators have full access to all features and functionalities of the platform.

**Permissions:**
- Full access to all models (create, read, update, delete)
- User management
- AI tool management
- Content management
- System configuration

### 2. Content Managers

Content Managers are responsible for managing the AI tools catalog but have limited access to user data.

**Permissions:**
- **AI Tools**: Full access (create, read, update, delete)
- **User Favorites**: View only
- **Conversations**: View only
- **Messages**: View only
- **Favorite Prompts**: View only
- **Shared Chats**: View only
- **Users**: View only

### 3. Regular Users

Regular users can interact with the platform but cannot manage AI tools or other users' data.

**Permissions:**
- **AI Tools**: View only
- **User Favorites**: Full access to their own data
- **Conversations**: Full access to their own data
- **Messages**: Full access to their own data
- **Favorite Prompts**: Full access to their own data
- **Shared Chats**: Full access to their own data

## Managing User Groups

### Adding Users to Groups

1. Go to the Django Admin panel
2. Navigate to "Users" under the "USERS" section
3. Select a user to edit
4. In the "Permissions" section, select the appropriate group(s) from the "Groups" field
5. Click "Save"

### Creating New Groups

To create new user groups with custom permissions, you can:

1. Use the Django Admin panel to create and configure groups manually
2. Run the management command: `python manage.py setup_groups` to reset groups to the default configuration

## Implementation Details

The user groups and permissions are implemented using Django's built-in authentication system. The setup is defined in the `setup_groups` management command located in `users/management/commands/setup_groups.py`. 