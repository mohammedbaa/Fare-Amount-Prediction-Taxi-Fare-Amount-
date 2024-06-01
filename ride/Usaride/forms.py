from django import forms
from datetime import datetime
class LocationForm(forms.Form):
    pickup_latitude = forms.FloatField(required=True)
    pickup_longitude = forms.FloatField(required=True)
    dropoff_latitude = forms.FloatField(required=True)
    dropoff_longitude = forms.FloatField(required=True)
    distance = forms.FloatField(widget=forms.HiddenInput(), required=False)  # Updated for better handling
    day = forms.DateField(initial=datetime.now().date())
    hour = forms.IntegerField(initial=datetime.now().hour)
