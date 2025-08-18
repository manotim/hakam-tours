from django.urls import path
from .views import TestimonialCreateView

app_name = "testimonials"

urlpatterns = [
    path("<slug:trip_slug>/new/", TestimonialCreateView.as_view(), name="create"),
]
