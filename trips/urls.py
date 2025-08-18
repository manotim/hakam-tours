from django.urls import path
from .views import TripDetailView, CategoryListView, CategoryDetailView, TripListView
from . import views

app_name = "trips"


urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/<slug:slug>/", CategoryDetailView.as_view(), name="category_detail"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/toggle/<int:trip_id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("", TripListView.as_view(), name="trip_list"),
    path("<slug:slug>/", TripDetailView.as_view(), name="trip_detail"),  # keep slug last
]