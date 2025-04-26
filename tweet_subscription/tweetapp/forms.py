from django import forms

class PaymentForm(forms.Form):
    plan_id = forms.IntegerField(widget=forms.HiddenInput())
