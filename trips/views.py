from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count   
from .models import Trip, Category

class TripListView(ListView):
    model = Trip
    template_name = "trips/trip_list.html"
    context_object_name = "trips"
    paginate_by = 6   # 6 trips per page

    def get_queryset(self):
        # Optimize queries + add average rating & review count
        qs = (
            Trip.objects.all()
            .prefetch_related("packages", "testimonials", "wishlisted_by", "images")  # 👈 include images
            .annotate(
                avg_rating=Avg("testimonials__rating"),
                review_count=Count("testimonials"),
            )
        )
        # Apply hot filter if ?hot=1
        if self.request.GET.get("hot") == "1":
            qs = qs.filter(is_hot=True)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Expose the "hot" filter state to the template
        context["is_hot_filter"] = self.request.GET.get("hot") == "1"

        # Pass wishlist trip IDs for highlighting hearts
        if self.request.user.is_authenticated:
            context["wishlist_ids"] = set(
                self.request.user.wishlisted_trips.values_list("id", flat=True)
            )
        else:
            context["wishlist_ids"] = set()
        return context

@login_required
def toggle_wishlist(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.user in trip.wishlisted_by.all():
        trip.wishlisted_by.remove(request.user)
    else:
        trip.wishlisted_by.add(request.user)
    return redirect("trips:trip_detail", slug=trip.slug)


@login_required
def wishlist(request):
    trips = Trip.objects.filter(wishlisted_by=request.user)
    return render(request, "trips/wishlist.html", {"trips": trips})




class TripDetailView(DetailView):
    model = Trip
    template_name = "trips/trip_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        trip = self.object

        # Prefetch related objects for performance
        ctx["packages"] = trip.packages.all()
        ctx["images"] = trip.images.all()  # 👈 New: all gallery photos
        ctx["testimonials"] = (
            getattr(trip, "testimonials", []).all()
            if hasattr(trip, "testimonials")
            else []
        )
        return ctx
class CategoryListView(ListView):
    model = Category
    template_name = "trips/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "trips/category_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["trips"] = self.object.trips.all()
        return ctx

class SafariListView(ListView):
    model = Category
    template_name = "trips/safari_list.html"
    context_object_name = "safari_categories"

    def get_queryset(self):
        return Category.objects.filter(is_safari=True)
    
