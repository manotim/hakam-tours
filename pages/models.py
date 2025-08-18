from django.db import models

# Create your models here.
from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
