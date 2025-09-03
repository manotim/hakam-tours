from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("vote/<slug:competition_slug>/<int:celebrity_id>/", views.vote_celebrity, name="vote_celebrity"),
]
