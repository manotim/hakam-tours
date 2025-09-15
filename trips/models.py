from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.db.models import Avg
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True) 
    description = models.TextField(blank=True)
    image = CloudinaryField("image", blank=True, null=True)
    is_safari = models.BooleanField(default=False, help_text="Mark this category as Safari type")

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Trip(models.Model):
    """A trip belonging to a category (town/region)."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="trips")
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=True) 
    cover_image = CloudinaryField("image", blank=True, null=True)
    wishlisted_by = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="wishlisted_trips",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_hot = models.BooleanField(default=False, help_text="Mark as hot trip to feature on home page")

    def get_min_price(self):
        """Return cheapest package price or None if no packages exist."""
        cheapest = self.packages.order_by("price").first()
        return cheapest.price if cheapest else None
    
    def average_rating(self):
        """Returns average rating from testimonials (1–5) or None."""
        if hasattr(self, "testimonials"):
            return self.testimonials.aggregate(avg=Avg("rating"))["avg"]
        return None

    class Meta:
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("trips:trip_detail", args=[self.slug])

    @property
    def status(self):
        today = timezone.now().date()
        if self.end_date < today:
            return "past"
        return "current"

class TripImage(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField("image")


    def __str__(self):
        return f"Image for {self.trip.title}"


class Package(models.Model):
    """A trip can have multiple packages (Standard, VIP, Group, etc.)."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_people = models.PositiveIntegerField(default=1)
    is_special = models.BooleanField(default=False)  # ✅ New field

    # ✅ New fields
    included = models.TextField(
        blank=True,
        help_text="Enter one item per line for things included in this package"
    )
    excluded = models.TextField(
        blank=True,
        help_text="Enter one item per line for things NOT included in this package"
    )

    def __str__(self):
        return f"{self.name} — {self.trip.title}"

    # ✅ Helpers to return items as lists
    def get_included_list(self):
        return [item.strip() for item in self.included.splitlines() if item.strip()]

    def get_excluded_list(self):
        return [item.strip() for item in self.excluded.splitlines() if item.strip()]

