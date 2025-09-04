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
    fields = ("name", "description", "price", "max_people", "is_special", "included", "excluded")
    show_change_link = True

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
         # ✅ Update label for visibility
        formset.form.base_fields["is_special"].label = "Special Package (✨ requires custom requests)"
        
        # ✅ Add a more explicit help text for admins
        formset.form.base_fields["is_special"].help_text = (
            "Mark this as a special package. Customers will be required to provide customization requests when booking."
        )
        return formset


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "start_date", "end_date", "is_current", "is_hot")
    list_filter = ("category", "start_date", "is_current", "is_hot")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PackageInline, TripImageInline]
