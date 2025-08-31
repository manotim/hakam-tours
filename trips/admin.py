from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Category, Trip, Package, TripImage


# -----------------------
# Custom MultiFileInput
# -----------------------
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class TripAdminForm(forms.ModelForm):
    new_images = forms.ImageField(
        widget=MultiFileInput(attrs={"multiple": True}),
        required=False,
        help_text="You can select multiple images to upload."
    )

    class Meta:
        model = Trip
        fields = "__all__"


class TripImageInline(admin.TabularInline):
    model = TripImage
    extra = 1
    readonly_fields = ["preview"]

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" style="border-radius:8px;" />')
        return "No Image"


class PackageInline(admin.StackedInline):
    model = Package
    extra = 1
    fields = ("name", "description", "price", "max_people", "included", "excluded")
    show_change_link = True


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    form = TripAdminForm
    list_display = ("title", "category", "start_date", "end_date", "is_current", "is_hot")
    list_filter = ("category", "start_date", "is_current", "is_hot")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PackageInline, TripImageInline]

    def save_model(self, request, obj, form, change):
        """Save Trip and handle new multiple image uploads."""
        super().save_model(request, obj, form, change)

        for image in request.FILES.getlist("new_images"):
            TripImage.objects.create(trip=obj, image=image)
