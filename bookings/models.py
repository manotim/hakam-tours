from django.db import models
from django.core.validators import MinValueValidator
from trips.models import Trip, Package

class Booking(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="bookings")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="bookings")
    name = models.CharField(max_length=200)  # for guest bookings
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    group_size = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]  # enforce min=1 even at DB level
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.trip.title} ({self.package.name})"
