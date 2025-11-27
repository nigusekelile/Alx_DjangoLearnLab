# API Filtering, Searching, and Ordering Documentation

## Overview
This document describes the advanced query capabilities available for the Book API endpoints, including filtering, searching, and ordering features.

## Base URL
All endpoints are relative to: `http://localhost:8000/api/`

## Book List Endpoint
**GET** `/books/`

### Filtering Parameters

#### Exact Matching
- `publication_year` - Exact publication year
  ```http
  GET /api/books/?publication_year=1997