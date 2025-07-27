# Postman Collections for Messaging API

## Setup Instructions

1. **Import the Collection**:
   - Open Postman
   - Click "Import" button
   - Select the `Messaging_API.postman_collection.json` file

2. **Configure Environment Variables**:
   - Create a new environment in Postman
   - Set the following variables:
     - `base_url`: `http://localhost:8000` (or your deployed URL)
     - `access_token`: Your JWT access token
     - `refresh_token`: Your JWT refresh token

3. **Testing Flow**:

### Step 1: Authentication
1. First, create users via Django admin or API
2. Use "Get JWT Token" to obtain access token
3. Set the `access_token` variable in your environment

### Step 2: Create Conversation
1. Use "Create Conversation" with participant UUIDs
2. Save the returned conversation ID

### Step 3: Send Messages
1. Use "Send Message" with the conversation ID
2. Send multiple messages to test pagination

### Step 4: Fetch Conversations and Messages
1. Use "List Conversations" to see all user conversations
2. Use "List Messages" to see paginated messages
3. Test filtering with query parameters

### Step 5: Test Unauthorized Access
1. Try accessing endpoints without tokens
2. Try accessing private conversations with wrong user tokens

## Available Endpoints

### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

### Conversations
- `POST /api/conversations/` - Create conversation
- `GET /api/conversations/` - List conversations
- `GET /api/conversations/{id}/` - Get conversation detail
- `PUT /api/conversations/{id}/` - Update conversation
- `DELETE /api/conversations/{id}/` - Delete conversation
- `GET /api/conversations/{id}/messages/` - Get conversation messages

### Messages
- `POST /api/messages/` - Send message
- `GET /api/messages/` - List messages (paginated)
- `GET /api/messages/{id}/` - Get message detail
- `PUT /api/messages/{id}/` - Update message
- `DELETE /api/messages/{id}/` - Delete message

## Testing Scenarios

### Pagination Testing
- Send more than 20 messages
- Use `page` parameter to navigate pages
- Check pagination metadata in response

### Filtering Testing
- Filter messages by sender email
- Filter messages by date range
- Filter messages by conversation
- Filter conversations by participant

### Security Testing
- Ensure 401 for unauthenticated requests
- Ensure 403 for unauthorized access to private conversations
- Ensure users can only modify their own messages