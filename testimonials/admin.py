from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "trip", "rating", "created_at")
    list_filter = ("rating", "trip")
