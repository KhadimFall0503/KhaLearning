from django.contrib import admin
from .models import Course, Category, Resource, ResourceCategory

# ===================== ADMIN CATEGORIES =====================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ===================== ADMIN COURS =====================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration_display', 'level', 'is_featured')
    list_filter = ('category', 'level', 'is_featured')
    search_fields = ('title', 'description', 'author')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'category', 'author', 'level', 
                'duration', 'youtube_url', 'image', 'learning_points', 'is_featured'
            )
        }),
    )

# ===================== ADMIN CATEGORIES DE RESSOURCES =====================
@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ===================== ADMIN RESSOURCES =====================
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description', 'url')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'url', 'image', 'category', 'is_featured'
            )
        }),
    )
