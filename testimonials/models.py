from django.db import models
from trips.models import Trip

class Testimonial(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="testimonials")
    name = models.CharField(max_length=200)  # visitor’s name
    rating = models.PositiveSmallIntegerField(default=5)  # 1–5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.trip.title} ({self.rating}★)"
