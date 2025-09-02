from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Trip, Package, TripImage


class TripImageInline(admin.TabularInline):
    model = TripImage
    extra = 1
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="120" style="border-radius:8px;" />')
        return "No Image"


class PackageInline(admin.StackedInline):
    model = Package
    extra = 1
    fields = ("name", "description", "price", "max_people", "included", "excluded")
    show_change_link = True


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "end_date", "is_current", "is_hot")
    list_filter = ("category", "start_date", "is_current", "is_hot")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PackageInline, TripImageInline]
