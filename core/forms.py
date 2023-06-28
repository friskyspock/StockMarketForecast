from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

class TickerName(forms.Form):
    COMPANY_CHOICES = [
    ("","-- Select Company --"),
    ("RELIANCE.NS","Reliance Industries Limited"),
    ("TATAMOTORS.NS","Tata Motors Limited")
    ]
    ticker = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-select'}),
        choices=COMPANY_CHOICES,
        label=False)

class Steps(forms.Form):
    num_steps = forms.IntegerField(
        max_value=60,
        label=False,
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter number of steps'}))