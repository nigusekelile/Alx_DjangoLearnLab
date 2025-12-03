# Django Blog Application
## Feature Documentation

This section documents the blog-post features, how to use them, and special notes about permissions and data handling.

### Overview
- Each blog post contains: title, slug, content (rich text/HTML), excerpt, author, status (draft/published), tags, featured image, read_time, published_at, created_at, updated_at.
- Posts are created and managed in the site UI and via standard Django views/serializers for API consumers.

### Creating a Post
- UI: authenticated users use the "New Post" form. Required fields: title, content. Slugs may be auto-generated from title.
- API: POST /api/posts/ (example JSON)
    {
        "title": "My Post",
        "slug": "my-post",
        "content": "<p>HTML or sanitized rich text</p>",
        "status": "published",
        "tags": ["django","tips"]
    }
- Notes:
    - Slug must be unique; collisions will return a validation error.
    - Content is accepted as HTML from the rich text editor but is sanitized server-side before saving.

### Reading / Viewing Posts
- Published posts are visible to all visitors.
- Draft posts are visible only to the author and staff/superusers.
- Pagination is applied on list views (configurable page size).

### Editing Posts
- Only the post author, staff, or superusers may edit a post.
- Editing via UI preserves created_at and updates updated_at.
- Server-side permission check example:
    ```
    if request.user == post.author or request.user.is_staff:
            # allow edit
    else:
            # return forbidden
    ```

### Deleting Posts
- Delete allowed for the author, staff, and superusers unless project config enforces soft-deletes.
- Deletions may be irreversible by default—consider enabling soft-delete or maintaining backups.

### Rich Text & Content Sanitization
- Rich text is stored as HTML. Before saving, the app sanitizes user-provided HTML to remove dangerous tags/attributes.
- Recommended sanitizers: bleach (allow list of safe tags/attrs) or the rich-text editor's built-in sanitizer.
- Preserve basic formatting, headings, lists, links, images.

### Media & File Handling
- Images are stored in MEDIA_ROOT with unique filenames (UUID or timestamp prefixes).
- Enforce upload limits (file size and dimensions) and validate content type.
- Serve media via a proper static/media server in production (e.g., AWS S3, cloud storage, or CDN).

### Tags & Related Posts
- Tags are a many-to-many relation. Tag creation may be limited to authenticated users.
- Related posts are suggested by shared tags or same author; ranking logic can be simple tag-overlap count or extended with similarity algorithms.

### Read Time Estimation
- Read time can be computed on save or on-the-fly based on word count (e.g., words / 200 wpm).
- Store as a small integer field read_time_minutes for quick display.

### Search (to be implemented / recommended approaches)
- Simple: database ILIKE queries on title/content for basic search.
- Recommended: full-text search (Postgres tsvector) or external engines (Elasticsearch / Meilisearch) for scalability and relevance ranking.

### Permissions Summary
- Anonymous: read published posts.
- Authenticated user: create posts, edit/delete own posts.
- Staff: moderate content, edit/delete any post.
- Superuser: full access.
- Always enforce checks server-side in views/serializers/templates.

### Data Integrity and Security Notes
- Sanitize all user input (especially HTML).
- Protect forms and endpoints with CSRF and authentication.
- Validate and sanitize filenames and user-supplied metadata.
- Limit attachment sizes and types.
- Back up database and media regularly.

### Dev / Deployment Notes
- Run migrations after model changes: python manage.py migrate
- Create a superuser for admin access: python manage.py createsuperuser
- Configure MEDIA_ROOT and MEDIA_URL for uploads; use cloud storage in production.
- Add tests for create/edit/delete and permission rules.

### Example Model & Permission Sketch (conceptual)
- Model fields: CharField(title), SlugField(slug, unique), TextField(content), ForeignKey(User, author), ManyToMany(Tag), ImageField(featured_image), BooleanField(is_published) or status choices, IntegerField(read_time).
- View permission logic: allow only (request.user == post.author) or request.user.is_staff.

If you need, the above items can be expanded into per-endpoint usage examples, exact serializer schemas, or test cases.
A comprehensive blog application built with Django featuring user authentication, blog post management, and interactive features.