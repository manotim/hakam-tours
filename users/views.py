from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()   # create user but don't log in
            return redirect("login")  # send them to login page
        else:
            # This will print the validation errors in your terminal / console
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def profile(request):
    # Get wishlist trips for the logged-in user
    wishlist_trips = request.user.wishlisted_trips.all()
    return render(request, "users/profile.html", {
        "wishlist_trips": wishlist_trips,
    })
