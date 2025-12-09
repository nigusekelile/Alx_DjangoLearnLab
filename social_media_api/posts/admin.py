from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('created_at', 'is_published', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at', 'likes_count', 'comments_count')
    fieldsets = (
        ('Basic Information', {
            'fields': ('author', 'title', 'content', 'image', 'is_published')
        }),
        ('Statistics', {
            'fields': ('likes_count', 'comments_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_at', 'likes_count')
    list_filter = ('created_at', 'author', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at', 'likes_count', 'replies_count')
    fieldsets = (
        ('Basic Information', {
            'fields': ('post', 'author', 'content', 'parent_comment')
        }),
        ('Statistics', {
            'fields': ('likes_count', 'replies_count', 'created_at', 'updated_at')
        }),
    )