# Security Best Practices

## API Key Management

### Overview

This document outlines the security enhancements implemented for API key management in the InspireIA application. These enhancements ensure that sensitive data like API keys are properly secured and not stored in the codebase or database.

### Key Security Enhancements

1. **Environment Variable Storage**
   - All API keys are now stored exclusively in environment variables
   - No API keys are stored in the database or settings files
   - The application uses a secure retrieval mechanism via the `get_api_key` function

2. **Encryption for Sensitive Data**
   - Added encryption capabilities for sensitive data using Fernet symmetric encryption
   - Encryption key is derived from a salt and the Django SECRET_KEY using PBKDF2
   - Encrypted data is stored as base64-encoded strings

### How to Configure API Keys

#### Local Development

1. Create a `.env` file in the project root (if not already present)
2. Add your API keys to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   ENCRYPTION_KEY_SALT=your_random_salt_string
   ```
3. Make sure the `.env` file is added to `.gitignore` to prevent it from being committed to version control

#### Production Environment

1. Set environment variables on your production server:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export HUGGINGFACE_API_KEY=your_huggingface_api_key
   export ENCRYPTION_KEY_SALT=your_random_salt_string
   ```
2. For containerized deployments (Docker), add these as environment variables in your Docker Compose file or Kubernetes secrets

### Using the Security Module

The application now includes a `core.security` module with the following key functions:

1. **`get_api_key(key_name)`**
   - Securely retrieves an API key from environment variables
   - Example: `api_key = get_api_key('OPENAI_API_KEY')`

2. **`encrypt_value(value)`**
   - Encrypts a sensitive value using Fernet symmetric encryption
   - Example: `encrypted = encrypt_value('sensitive_data')`

3. **`decrypt_value(encrypted_value)`**
   - Decrypts a previously encrypted value
   - Example: `decrypted = decrypt_value(encrypted_value)`

### Security Best Practices

1. **Never hardcode API keys** in your code or commit them to version control
2. **Rotate API keys periodically** according to your security policy
3. **Use different API keys** for development and production environments
4. **Limit API key permissions** to only what's necessary for your application
5. **Monitor API key usage** for unusual patterns that might indicate compromise
6. **Implement rate limiting** to prevent abuse of your API keys

### Troubleshooting

If you encounter issues with API keys:

1. Verify that the environment variables are properly set
2. Check that the `ENCRYPTION_KEY_SALT` is set and consistent
3. Ensure that the application has permission to read environment variables
4. Look for error logs that might indicate encryption/decryption issues

For any security concerns or vulnerabilities, please contact the security team immediately.
