# API Testing Documentation

## Overview
This document describes the comprehensive test suite for the Django REST Framework APIs. The tests cover CRUD operations, filtering, searching, ordering, permissions, and error handling.

## Test Structure

### Test Classes

1. **BaseTestCase** (APITestCase)
   - Base class with common setup methods
   - Creates test users, authors, and books
   - Sets up API client and URLs

2. **BookCRUDTests**
   - Tests Create, Read, Update, Delete operations
   - Tests authentication and permission controls
   - Tests validation rules

3. **FilteringSearchingOrderingTests**
   - Tests filtering by various fields
   - Tests search functionality
   - Tests ordering by single and multiple fields
   - Tests combined query operations

4. **AuthorAPITests**
   - Tests Author list and detail endpoints
   - Tests author filtering and ordering

5. **SerializerTests** (TestCase)
   - Tests serializer validation
   - Tests field-level validation

6. **ModelTests** (TestCase)
   - Tests model string representations
   - Tests model ordering and relationships

7. **ErrorHandlingTests**
   - Tests 404 responses for non-existent resources
   - Tests invalid data submissions

## Running Tests

### Run All Tests
```bash
python manage.py test api