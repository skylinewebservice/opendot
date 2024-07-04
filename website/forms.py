from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone Number', max_length=20, widget=forms.TextInput(attrs={'placeholder': '+1234567890'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'opendot@open'}))
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_CHOICES, widget=forms.RadioSelect, )

    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'phone_number', 'payment_method']
