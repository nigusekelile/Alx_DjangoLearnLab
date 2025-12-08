from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_verified', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Social Media Info', {'fields': ('bio', 'profile_picture', 'followers')}),
        ('Verification', {'fields': ('is_verified',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Social Media Info', {'fields': ('bio', 'profile_picture')}),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website')
    search_fields = ('user__username', 'user__email', 'location')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)