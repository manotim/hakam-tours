from django.db import models
from cloudinary.models import CloudinaryField  # ✅ import CloudinaryField

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    # photo = models.ImageField(upload_to="team/", blank=True, null=True)  # ❌ local storage
    photo = CloudinaryField("image", blank=True, null=True)  # ✅ cloud storage

    def __str__(self):
        return self.name
