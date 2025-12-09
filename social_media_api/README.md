# Social Media API - User Authentication

## Project Overview
A Django REST Framework-based Social Media API with complete user authentication system.

## Features
- Custom User Model with extended fields (bio, profile picture, followers)
- Token-based authentication
- User registration, login, and logout
- User profile management
- Follow/Unfollow functionality
- Password change functionality

## Posts and Comments Features

### New Endpoints:

#### Posts:
- `GET /api/posts/` - List all posts with pagination and search
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Get post details
- `PUT/PATCH /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post
- `POST /api/posts/{id}/like/` - Like/unlike post
- `GET /api/posts/{id}/comments/` - Get post comments

#### Comments:
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/{id}/` - Get comment details
- `PUT/PATCH /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment
- `POST /api/comments/{id}/like/` - Like/unlike comment
- `GET /api/comments/{id}/replies/` - Get comment replies

### Features:
- Pagination (10 items per page, configurable)
- Search by title and content
- Filter by author
- Sorting by date and likes
- Image upload for posts
- Like/unlike functionality
- Nested comments
- Permission-based access control