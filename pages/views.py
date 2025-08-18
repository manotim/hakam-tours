from django.views.generic import TemplateView, ListView, DetailView
from team.models import TeamMember
from trips.models import Trip
from .models import Testimonial, BlogPost
import random


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_trips"] = Trip.objects.filter(is_current=True)
        ctx["past_trips"] = Trip.objects.filter(is_current=False)
        return ctx


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["team_members"] = TeamMember.objects.all()
        all_testimonials = list(Testimonial.objects.all())
        ctx["sample_testimonials"] = random.sample(all_testimonials, min(3, len(all_testimonials)))
        return ctx


class BlogListView(ListView):
    model = BlogPost
    template_name = "pages/blog_list.html"
    context_object_name = "posts"
    ordering = ["-published_at"]


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "pages/blog_detail.html"
    context_object_name = "post"
