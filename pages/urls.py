from django.urls import path
from .views import HomeView, AboutView, BlogListView, BlogDetailView

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("blog/", BlogListView.as_view(), name="blog_list"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog_detail"),
]
