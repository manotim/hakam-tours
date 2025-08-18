from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["name", "email", "phone", "group_size"]
        widgets = {
            "group_size": forms.NumberInput(attrs={"min": 1}),
        }
