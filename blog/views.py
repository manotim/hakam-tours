from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import BlogPost, Competition, Celebrity, Vote

def blog_list(request):
    posts = BlogPost.objects.all().order_by("-published_at")
    competition = Competition.objects.filter(is_active=True).order_by("-deadline").first()

    # For chart
    chart_data = []
    if competition:
        for celeb in competition.celebrities.all():
            chart_data.append({
                "name": celeb.name,
                "votes": celeb.total_votes(),
                "color": celeb.color
            })

    # ✅ check if user has voted
    user_voted = False
    if request.user.is_authenticated and competition:
        user_voted = Vote.objects.filter(competition=competition, voter=request.user).exists()

    return render(request, "blog/blog_list.html", {
        "posts": posts,
        "competition": competition,
        "chart_data": chart_data,
        "user_voted": user_voted,  # ✅ pass to template
    })

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blog/blog_detail.html", {"post": post})

@login_required
def vote_celebrity(request, competition_slug, celebrity_id):
    competition = get_object_or_404(Competition, slug=competition_slug)
    celebrity = get_object_or_404(Celebrity, id=celebrity_id, competition=competition)

    if competition.has_ended():
        messages.error(request, "Voting has ended for this competition.")
        return redirect("blog:blog_list")

    # Check if user has already voted
    if Vote.objects.filter(competition=competition, voter=request.user).exists():
        messages.warning(request, "You have already voted in this competition.")
        return redirect("blog:blog_list")

    # Save vote
    Vote.objects.create(competition=competition, celebrity=celebrity, voter=request.user)
    messages.success(request, f"You voted for {celebrity.name}!")
    return redirect("blog:blog_list")