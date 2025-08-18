from django.contrib import admin
from .models import Category, Trip, Package

class PackageInline(admin.TabularInline):
    model = Package
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "end_date", "is_current")
    list_filter = ("category", "start_date")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PackageInline]   # manage packages directly inside trip

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "trip", "price", "max_people")
