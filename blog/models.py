from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField  # ✅ import CKEditor RichTextField
from ckeditor_uploader.fields import RichTextUploadingField  # ✅ if you want image/file uploads


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(
        help_text="A short summary for previews", blank=True
    )

    # Hero / featured image
    cover_image = models.ImageField(upload_to="blog/covers/", blank=True, null=True)

    # Rich content (text + images between sections)
    content = RichTextUploadingField(   # ✅ allows image uploads inside content
        help_text="Main article body (rich-text editor with image upload support)"
    )

    # Optional photo gallery
    gallery_images = models.ManyToManyField(
        "BlogImage",
        related_name="posts",
        blank=True,
        help_text="Additional inline images for the article"
    )

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogImage(models.Model):
    """Extra images that can be placed in gallery sections"""
    image = models.ImageField(upload_to="blog/gallery/")
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or f"Image {self.id}"
