from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "trip", "package", "group_size", "created_at")
    list_filter = ("trip", "package")
    search_fields = ("name", "email", "phone")  # easier searching
