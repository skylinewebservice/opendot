import json
from pathlib import Path
from django.conf import settings
from django.core.mail import send_mail

def get_products():
    file_path = Path(settings.BASE_DIR) / 'products.json'
    with open(file_path) as f:
        data = json.load(f)
        return data.get('products', [])

def get_products():
    try:
        with open('products.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    if isinstance(data, dict):
        return data.get('products', [])
    else:
        return []
    

def send_order_notification(order):
    subject = f'New Order #{order.pk}'
    message = f'You have received a new order.\n\nOrder Details:\n\n'
    message += f'Order ID: {order.pk}\n'
    message += f'Customer: {order.name}\n'
    message += f'Email: {order.email}\n'
    message += f'Phone Number: {order.phone_number}\n'
    message += f'Total Price: {order.total_price}\n\n'
    message += 'Products:\n'

    products = json.loads(order.product_ids)
    for item in products:
        message += f'{item["quantity"]} x {item["name"]} - ${item["price"]}\n'

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.EMAIL_HOST_USER],  # Change this to the recipient's email address
        fail_silently=False,
    )

