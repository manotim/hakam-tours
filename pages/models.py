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



