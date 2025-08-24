import os
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_initial_superuser(sender, **kwargs):
    """
    Creates a superuser once, using env vars.
    Works with custom user models (uses USERNAME_FIELD).
    Safe to run many times due to existence check.
    """
    User = get_user_model()

    username_field = User.USERNAME_FIELD  # e.g. "username" or "email"

    # Pick username from correct env var
    username = os.environ.get(
        "DJANGO_SUPERUSER_EMAIL" if username_field == "email" else "DJANGO_SUPERUSER_USERNAME"
    )
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

    if not username or not password:
        return  # don’t try to create without creds

    if User.objects.filter(**{username_field: username}).exists():
        return  # already exists, skip

    create_kwargs = {username_field: username}
    if email and username_field != "email":
        create_kwargs["email"] = email

    User.objects.create_superuser(**create_kwargs, password=password)
    print(f"✅ Superuser {username} created")
