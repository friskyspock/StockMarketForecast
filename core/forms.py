from django import forms
from core.models import TickerList

tlist = TickerList.objects.values_list('Symbol','Name')
COMPANY_CHOICES = [("","-- Select Company --")] + list(tlist)

class TickerName(forms.Form):
    ticker = forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-select'}),
        choices=COMPANY_CHOICES,
        label=False)

class Steps(forms.Form):
    num_steps = forms.IntegerField(
        max_value=60,
        label=False,
        widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter number of steps'}))