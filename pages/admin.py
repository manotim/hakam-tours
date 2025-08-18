from django.contrib import admin
from .models import Testimonial, BlogPost

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at")
    prepopulated_fields = {"slug": ("title",)}
