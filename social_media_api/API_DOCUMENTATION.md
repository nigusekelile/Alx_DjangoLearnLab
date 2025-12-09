# Social Media API - Posts & Comments Documentation

## Posts Endpoints

### List Posts
**GET** `/api/posts/`

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)
- `search` - Search in title or content
- `author` - Filter by author username
- `ordering` - Sort by fields: `created_at`, `-created_at`, `likes_count`, etc.

**Response:**
```json
{
    "count": 100,
    "next": "http://api.example.com/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com"
            },
            "title": "My First Post",
            "excerpt": "This is the beginning...",
            "image": null,
            "created_at": "2024-01-01T12:00:00Z",
            "likes_count": 10,
            "comments_count": 5
        }
    ]
}