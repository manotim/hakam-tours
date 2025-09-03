from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import BlogPost, BlogImage, Competition, Celebrity, Vote


# ----------------------
# Blog Admin
# ----------------------

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
    form = BlogPostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "published_at", "updated_at")
    list_filter = ("published_at",)
    search_fields = ("title", "content")
    readonly_fields = ("published_at", "updated_at")

    fieldsets = (
        ("Basic Info", {"fields": ("title", "slug", "excerpt", "cover_image")}),
        ("Content", {"fields": ("content",)}),
        ("Gallery", {"fields": ("gallery_images",)}),
        ("Meta", {"fields": ("published_at", "updated_at")}),
    )


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "image")


# ----------------------
# Competition Admin
# ----------------------

class CelebrityInline(admin.TabularInline):
    """Allow adding Celebrities directly inside a Competition."""
    model = Celebrity
    extra = 2
    fields = ("name", "photo", "bio")
    show_change_link = True


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "deadline", "is_active", "has_ended")
    list_filter = ("is_active", "deadline")
    search_fields = ("name", "description")
    inlines = [CelebrityInline]  # ✅ Manage celebrities inline


@admin.register(Celebrity)
class CelebrityAdmin(admin.ModelAdmin):
    list_display = ("name", "competition", "total_votes")
    list_filter = ("competition",)
    search_fields = ("name", "bio")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("voter", "celebrity", "competition", "voted_at")
    list_filter = ("competition", "celebrity", "voted_at")
    search_fields = ("voter__username", "celebrity__name", "competition__name")
