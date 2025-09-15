from django.db import models
from cloudinary.models import CloudinaryField  # ✅ import CloudinaryField

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    # photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)  # ❌ local storage
    photo = CloudinaryField("image", blank=True, null=True)  # ✅ cloud storage
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
