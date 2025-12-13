from django.db import models
from django.utils import timezone
from urllib.parse import urlparse, parse_qs

# ===================== CATEGORIES DE COURS =====================
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# ===================== COURS =====================
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='courses'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    youtube_url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True)
    duration = models.PositiveIntegerField(blank=True, null=True, help_text="Durée en minutes")
    level = models.CharField(
        max_length=50,
        blank=True,
        choices=[('Beginner','Beginner'),('Intermediate','Intermediate'),('Advanced','Advanced')]
    )

    # Stockage des points d'apprentissage séparés par saut de ligne
    learning_points = models.TextField(
        blank=True,
        help_text="Écrire chaque point sur une nouvelle ligne"
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def youtube_id(self):
        if not self.youtube_url:
            return None
        url_data = urlparse(self.youtube_url)
        query = parse_qs(url_data.query)
        return query.get("v", [None])[0]

    def youtube_thumbnail(self):
        video_id = self.youtube_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return None

    def duration_display(self):
        if not self.duration:
            return "Variable"
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours > 0:
            return f"{hours}h {minutes}min" if minutes > 0 else f"{hours}h"
        return f"{minutes}min"

    # Retourne les points sous forme de liste
    def learning_points_list(self):
        return self.learning_points.splitlines()

# ===================== CATEGORIES DE RESSOURCES =====================
class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Resource Categories"

    def __str__(self):
        return self.name

# ===================== RESSOURCES =====================
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='resources/', blank=True, null=True)
    category = models.ForeignKey(
        ResourceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='resources'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
