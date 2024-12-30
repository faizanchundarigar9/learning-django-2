from django import forms

class CheckoutForm(forms.Form):
    country = forms.CharField(max_length = 30)
    district = forms.CharField(max_length = 30)
    city = forms.CharField(max_length = 30)
    

