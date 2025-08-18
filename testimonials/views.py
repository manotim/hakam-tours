from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from .models import Testimonial
from .forms import TestimonialForm
from trips.models import Trip

class TestimonialCreateView(CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = "testimonials/testimonial_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, slug=kwargs["trip_slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.trip = self.trip
        return super().form_valid(form)

    def get_success_url(self):
        return self.trip.get_absolute_url()
