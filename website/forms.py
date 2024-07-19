from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_CHOICES, widget=forms.RadioSelect, )

    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'phone_number', 'payment_method']
