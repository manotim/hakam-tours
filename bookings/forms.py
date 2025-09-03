from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "name", "email", "phone",
            "group_size", "start_date", "end_date",
            "mode_of_travel", "hotel", "nationality"
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        group_size = cleaned_data.get("group_size")

        print("🔎 Running BookingForm.clean() with:", cleaned_data)  # DEBUG PRINT

        # Ensure group size is positive
        if group_size and group_size < 1:
            self.add_error("group_size", "Group size must be at least 1.")

        # Ensure end date is after start date
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date must be after the start date.")

        return cleaned_data
