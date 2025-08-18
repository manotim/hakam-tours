from django.urls import path
from .views import BookingCreateView, BookingSuccessView

app_name = "bookings"

urlpatterns = [
    path("<slug:trip_slug>/<int:package_id>/", BookingCreateView.as_view(), name="create"),
    path("success/", BookingSuccessView.as_view(), name="success"),
]
