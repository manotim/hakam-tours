from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.package = kwargs.pop("package", None)  # ✅ grab package from kwargs
        super().__init__(*args, **kwargs)

        # ✅ If this is a special package, hide mode_of_travel & hotel
        if self.package and self.package.is_special:
            self.fields.pop("mode_of_travel", None)
            self.fields.pop("hotel", None)

            # Make special_requests required
            if "special_requests" in self.fields:
                self.fields["special_requests"].required = True

    class Meta:
        model = Booking
        fields = [
            "name", "email", "phone",
            "group_size", "start_date", "end_date",
            "mode_of_travel", "hotel",
            "nationality", "special_requests",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "special_requests": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe your custom package here..."}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        special_requests = cleaned_data.get("special_requests")

        # ✅ Validate special_requests for special packages
        if self.package and self.package.is_special and not special_requests:
            self.add_error("special_requests", "Please describe your custom package.")

        # ✅ Validate dates
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date must be after start date.")

        return cleaned_data
