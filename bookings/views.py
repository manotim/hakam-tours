from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from .models import Booking
from .forms import BookingForm
from trips.models import Trip, Package
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .utils import send_whatsapp_message, send_telegram_message


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        # Verification request from WhatsApp
        verify_token = "tembea123"
        hub_challenge = request.GET.get("hub.challenge")
        hub_mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")

        if hub_mode == "subscribe" and token == verify_token:
            return HttpResponse(hub_challenge)
        else:
            return HttpResponse("Verification failed", status=403)

    elif request.method == "POST":
        # Handle incoming WhatsApp messages
        try:
            data = json.loads(request.body)
            print("Incoming WhatsApp event:", data)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        # You can process messages here, e.g., auto-replies, logging, etc.
        return HttpResponse("EVENT_RECEIVED", status=200)


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

        # ✅ WhatsApp notification to admin
        admin_number = "254759411378"  # your verified WhatsApp number
        whatsapp_message = (
            f"📢 New Booking Alert!\n\n"
            f"Trip: {self.trip.title}\n"
            f"Package: {self.package.name}\n"
            f"Name: {booking.name}\n"
            f"Email: {booking.email}\n"
            f"Phone: {booking.phone}\n"
            f"Travelers: {booking.group_size}"
        )
        wa_response = send_whatsapp_message(admin_number, whatsapp_message)
        print("WhatsApp API response:", wa_response)

        # ✅ Telegram notification to admin
        telegram_message = (
            f"📢 <b>New Booking Alert!</b>\n\n"
            f"🌍 Trip: {self.trip.title}\n"
            f"🎫 Package: {self.package.name}\n"
            f"👤 Name: {booking.name}\n"
            f"✉️ Email: {booking.email}\n"
            f"📞 Phone: {booking.phone}\n"
            f"👥 Travelers: {booking.group_size}\n"
            f"🕒 Time: {booking.created_at.strftime('%Y-%m-%d %H:%M')}"
        )
        tg_response = send_telegram_message(telegram_message)
        print("Telegram API response:", tg_response)

        # Redirect to success page
        return redirect(
            f"{redirect('bookings:success').url}?trip={self.trip.slug}&package={self.package.id}"
        )
