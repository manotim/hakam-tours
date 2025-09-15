from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from .models import Booking
from django.urls import reverse
from .forms import BookingForm
from trips.models import Trip, Package
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .utils import send_whatsapp_message, send_telegram_message


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        verify_token = "tembea123"
        hub_challenge = request.GET.get("hub.challenge")
        hub_mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")

        if hub_mode == "subscribe" and token == verify_token:
            return HttpResponse(hub_challenge)
        else:
            return HttpResponse("Verification failed", status=403)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            print("📩 Incoming WhatsApp event:", data)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        return HttpResponse("EVENT_RECEIVED", status=200)

@method_decorator([login_required, user_passes_test(lambda u: u.is_staff)], name="dispatch")
class BookingDashboardView(ListView):
    model = Booking
    template_name = "bookings/dashboard.html"
    context_object_name = "bookings"
    paginate_by = 20  # Show 20 per page

    def get_queryset(self):
        return Booking.objects.select_related("trip", "package").order_by("-created_at")
    
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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["package"] = self.package   # ✅ inject package into form
        return kwargs

    def form_valid(self, form):
        print("✅ form_valid triggered!")  # DEBUG PRINT
        form.instance.trip = self.trip
        form.instance.package = self.package

        if form.instance.start_date and form.instance.end_date:
            form.instance.duration = (form.instance.end_date - form.instance.start_date).days

        booking = form.save()

        # WhatsApp notification
        try:
            admin_number = "254759411378"
            whatsapp_message = (
                f"📢 New Booking Alert!\n\n"
                f"🌍 Trip: {self.trip.title}\n"
                f"🎫 Package: {self.package.name}\n"
                f"👤 Name: {booking.name}\n"
                f"✉️ Email: {booking.email}\n"
                f"📞 Phone: {booking.phone}\n"
                f"👥 Travelers: {booking.group_size}\n"
                f"🗓️ Start: {booking.start_date}\n"
                f"🗓️ End: {booking.end_date}\n"
                f"⏳ Duration: {booking.duration} days\n"
                f"🚍 Mode: {booking.get_mode_of_travel_display()}\n"
                f"🏨 Hotel: {booking.get_hotel_display()}\n"
                f"🌐 Nationality: {booking.nationality}"
            )
            if self.package.is_special and booking.special_requests:
                whatsapp_message += f"\n✨ Special Requests: {booking.special_requests}"

            wa_response = send_whatsapp_message(admin_number, whatsapp_message)
            print("📤 WhatsApp API response:", wa_response)
        except Exception as e:
            print("⚠️ WhatsApp error:", e)

        # Telegram notification
        try:
            telegram_message = (
                f"📢 <b>New Booking Alert!</b>\n\n"
                f"🌍 <b>Trip:</b> {self.trip.title}\n"
                f"🎫 <b>Package:</b> {self.package.name}\n"
                f"👤 <b>Name:</b> {booking.name}\n"
                f"✉️ <b>Email:</b> {booking.email}\n"
                f"📞 <b>Phone:</b> {booking.phone}\n"
                f"👥 <b>Travelers:</b> {booking.group_size}\n"
                f"🗓️ <b>Start:</b> {booking.start_date}\n"
                f"🗓️ <b>End:</b> {booking.end_date}\n"
                f"⏳ <b>Duration:</b> {booking.duration} days\n"
                f"🚍 <b>Mode:</b> {booking.get_mode_of_travel_display()}\n"
                f"🏨 <b>Hotel:</b> {booking.get_hotel_display()}\n"
                f"🌐 <b>Nationality:</b> {booking.nationality}\n"
                f"🕒 <b>Time:</b> {booking.created_at.strftime('%Y-%m-%d %H:%M')}"
            )
            if self.package.is_special and booking.special_requests:
                telegram_message += f"\n✨ <b>Special Requests:</b> {booking.special_requests}"

            tg_response = send_telegram_message(telegram_message)
            print("📤 Telegram API response:", tg_response)
        except Exception as e:
            print("⚠️ Telegram error:", e)

        return redirect(
            f"{reverse('bookings:success')}?trip={self.trip.slug}&package={self.package.id}"
        )

    def form_invalid(self, form):
        print("❌ form_invalid triggered!")
        print("Errors:", form.errors.as_json())  # DEBUG PRINT
        return super().form_invalid(form)
