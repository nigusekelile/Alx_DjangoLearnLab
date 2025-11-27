# API Views Documentation

## Overview
This document describes the custom views and generic views implemented for the Book model CRUD operations.

## View Configurations

### BookListView
- **Purpose**: List all books with filtering and search
- **URL**: `GET /api/books/`
- **Permissions**: AllowAny (public access)
- **Features**:
  - Filter by: `publication_year`, `author`
  - Search: `title` field
  - Order by: `title`, `publication_year`, `created_at`
  - Default ordering: `title` ascending

### BookDetailView
- **Purpose**: Retrieve single book by ID
- **URL**: `GET /api/books/<id>/`
- **Permissions**: AllowAny (public access)

### BookCreateView
- **Purpose**: Create new book
- **URL**: `POST /api/books/create/`
- **Permissions**: IsAuthenticated
- **Custom Behavior**: Returns custom success response with created book data

### BookUpdateView
- **Purpose**: Update existing book (full or partial)
- **URL**: `PUT/PATCH /api/books/<id>/update/`
- **Permissions**: IsAuthenticated
- **Custom Behavior**: Supports partial updates, custom response format

### BookDeleteView
- **Purpose**: Delete book
- **URL**: `DELETE /api/books/<id>/delete/`
- **Permissions**: IsAuthenticated
- **Custom Behavior**: Returns success message without deleted data

## Permission Classes

### Built-in Permissions Used
- `AllowAny`: Complete public access
- `IsAuthenticated`: Requires user authentication

### Custom Permissions Available
- `IsAuthenticatedOrReadOnly`: Read access for all, write for authenticated
- `IsOwnerOrReadOnly`: Object-level permissions (for future use)

## Testing Endpoints

### Public Endpoints (No Authentication)
```bash
# List books with filters
curl "http://localhost:8000/api/books/?publication_year=2020"
curl "http://localhost:8000/api/books/?search=harry"
curl "http://localhost:8000/api/books/?ordering=-publication_year"

# Get book detail
curl "http://localhost:8000/api/books/1/"