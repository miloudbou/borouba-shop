from django import forms
from django.contrib.auth.models import User
from .models import Product 
from .models import SiteSettings

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

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='اسم المستخدم')
    password = forms.CharField(widget=forms.PasswordInput, label='كلمة المرور')



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'price', 'currency',
            'image_url', 'affiliate_link', 'aliexpress_product_id',
            'is_offer', 'is_flash_sale', 'flash_sale_end'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'flash_sale_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    

