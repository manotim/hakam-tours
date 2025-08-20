from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("trips/", include("trips.urls")), 
    path("bookings/", include("bookings.urls")),
    path("testimonials/", include("testimonials.urls")),
    path("users/", include("users.urls")),
    path("blog/", include("blog.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path("users/logout/", LogoutView.as_view(next_page="/"), name="logout"),

    # CKEditor uploader
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
