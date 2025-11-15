# LibraryProject/relationship_app/admin.py
from django.contrib import admin
from .models import UserProfile, Author, Book, Library, Librarian

# REMOVE the CustomUser registration from here
# CustomUser should only be registered in bookshelf/admin.py

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__username', 'role')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'created_by', 'created_at')
    list_filter = ('author', 'publication_year', 'created_at')
    search_fields = ('title', 'author__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')
    filter_horizontal = ('books',)
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
    search_fields = ('name', 'library__name')
