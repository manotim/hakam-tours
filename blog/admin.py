from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import BlogPost, BlogImage


# Custom form to use CKEditor in the admin
class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = BlogPost
        fields = "__all__"


class BlogImageInline(admin.TabularInline):
    model = BlogPost.gallery_images.through
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm  # <-- attach custom form with CKEditor
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "published_at", "updated_at")
    list_filter = ("published_at",)
    search_fields = ("title", "content")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "excerpt", "cover_image")
        }),
        ("Content", {
            "fields": ("content",)
        }),
        ("Gallery", {
            "fields": ("gallery_images",)
        }),
        ("Meta", {
            "fields": ("published_at", "updated_at"),
        }),
    )
    readonly_fields = ("published_at", "updated_at")


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "image")
