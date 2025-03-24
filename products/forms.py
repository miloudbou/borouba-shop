from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)

class GuestOrderForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
