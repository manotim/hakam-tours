from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from trips.models import Trip, Package


class Booking(models.Model):
    MODE_OF_TRAVEL_CHOICES = [
        ("flight", "Flight"),
        ("road", "Road"),
        ("rail", "Rail"),
        ("cruise", "Cruise"),
    ]

    HOTEL_CHOICES = [
        ("3_star", "3 Star"),
        ("4_star", "4 Star"),
        ("5_star", "5 Star"),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="bookings")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="bookings")

    # Guest details
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Travel details
    group_size = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    mode_of_travel = models.CharField(max_length=20, choices=MODE_OF_TRAVEL_CHOICES, default="flight")
    hotel = models.CharField(max_length=20, choices=HOTEL_CHOICES, default="3_star")
    nationality = models.CharField(max_length=100, default="Unknown")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.trip.title} ({self.package.name})"
