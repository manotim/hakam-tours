from django.urls import path
from .views import BookingCreateView, BookingSuccessView
from . import views

app_name = "bookings"

urlpatterns = [
    path("<slug:trip_slug>/<int:package_id>/", BookingCreateView.as_view(), name="create"),
    path("success/", BookingSuccessView.as_view(), name="success"),
    path("webhook/", views.whatsapp_webhook, name="whatsapp_webhook"),
]
