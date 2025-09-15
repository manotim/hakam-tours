from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from cloudinary.models import CloudinaryField  # ✅ import CloudinaryField


# -------------------
# Blog
# -------------------
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(blank=True, help_text="A short summary for previews")
    cover_image = CloudinaryField("image", blank=True, null=True)  # ✅ Cloudinary
    content = RichTextUploadingField()
    gallery_images = models.ManyToManyField("BlogImage", related_name="posts", blank=True)
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
    image = CloudinaryField("image")  # ✅ Cloudinary
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or f"Image {self.id}"


# -------------------
# Voting Competition
# -------------------
class Competition(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def has_ended(self):
        return timezone.now() > self.deadline

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Celebrity(models.Model):
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name="celebrities"
    )
    name = models.CharField(max_length=255)
    photo = CloudinaryField("image")  # ✅ Cloudinary
    bio = models.TextField(blank=True)

    COLORS = [
        "#f87171",  # red-400
        "#60a5fa",  # blue-400
        "#34d399",  # green-400
        "#facc15",  # yellow-400
        "#a78bfa",  # purple-400
        "#fb923c",  # orange-400
        "#2dd4bf",  # teal-400
    ]

    def __str__(self):
        return self.name

    def total_votes(self):
        return self.votes.count()

    @property
    def color(self):
        # Assign color based on ID, wrap around COLORS list
        return self.COLORS[self.id % len(self.COLORS)]


class Vote(models.Model):
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name="votes"
    )
    celebrity = models.ForeignKey(
        Celebrity, on_delete=models.CASCADE, related_name="votes"
    )
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("competition", "voter")  # ✅ one vote per competition

    def __str__(self):
        return f"{self.voter.username} → {self.celebrity.name}"
