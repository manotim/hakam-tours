from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from django.core.mail import send_mail
from .models import Booking
from .forms import BookingForm
from trips.models import Trip, Package

class BookingSuccessView(TemplateView):
    template_name = "bookings/success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_slug = self.request.GET.get("trip")
        package_id = self.request.GET.get("package")
        if trip_slug and package_id:
            context["trip"] = get_object_or_404(Trip, slug=trip_slug)
            context["package"] = get_object_or_404(Package, id=package_id, trip=context["trip"])
        return context


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "bookings/booking_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, slug=kwargs["trip_slug"])
        self.package = get_object_or_404(Package, id=kwargs["package_id"], trip=self.trip)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Attach trip & package automatically
        form.instance.trip = self.trip
        form.instance.package = self.package
        booking = form.save()

        # Send confirmation email to traveler
        send_mail(
            subject=f"Booking Confirmation — {self.trip.title}",
            message=f"Hello {booking.name},\n\n"
                    f"Thank you for booking {self.trip.title} "
                    f"({self.package.name}).\n"
                    f"We have received your details and will contact you shortly.\n\n"
                    f"- Tembea Tours Team",
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[booking.email],
        )

        # Send notification to admin/business
        send_mail(
            subject=f"New Booking — {self.trip.title}",
            message=f"New booking received for {self.trip.title}\n\n"
                    f"Name: {booking.name}\n"
                    f"Email: {booking.email}\n"
                    f"Phone: {booking.phone}\n"
                    f"Package: {self.package.name}\n"
                    f"Travelers: {booking.group_size}\n\n",
            from_email=None,
            recipient_list=["admin@tembea.com"],  # replace later with real email
        )

        # Redirect to success page with trip/package for context
        return redirect(f"{redirect('bookings:success').url}?trip={self.trip.slug}&package={self.package.id}")
