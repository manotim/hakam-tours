from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_list(request):
    # Order posts by published_at (newest first)
    posts = BlogPost.objects.all().order_by('-published_at')
    return render(request, "blog/blog_list.html", {"posts": posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blog/blog_detail.html", {"post": post})
