from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth.decorators import login_required# type: ignore
from django.urls import reverse# type: ignore
from .models import Cart, CartItem, Wishlist, Product, Order,HostingService
from .forms import OrderForm
import json
from django.conf import settings# type: ignore
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse # type: ignore
from .models import Product
from django.contrib import messages# type: ignore
from django.views.decorators.csrf import csrf_exempt, csrf_protect# type: ignore
from pathlib import Path
from django.views.decorators.http import require_POST# type: ignore
from .utils import send_order_notification
from django.core.mail import send_mail


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def service(request):
    return render(request, 'service.html')


def why(request):
    return render(request, 'why.html')

def all_products_and_services(request):
    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)
    with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
        services = json.load(f)

    combined_items = products + services

    return render(request, 'all_products_and_services.html', {'items': combined_items})

def product_list(request):
    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)
    
    product = next((product for product in products if product['pk'] == pk), None)
    
    if not product:
        return HttpResponseNotFound('No Product matches the given query.')
    
    return render(request, 'product_detail.html', {'product': product})





@csrf_exempt
def add_to_cart(request, pk):
    if request.method == 'POST':
        with open(settings.BASE_DIR / 'products.json', 'r') as f:
            products = json.load(f)
        with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
            hosting_services = json.load(f)
        
        # Combine the products and hosting services into one list
        combined_products = products + hosting_services
        
        product_data = next((product for product in combined_products if product['pk'] == pk), None)
        if not product_data:
            return JsonResponse({'message': 'Product not found.'}, status=404)

        cart = request.session.get('cart', [])
        
        if pk in cart:
            return JsonResponse({'message': f'{product_data["name"]} is already in cart.', 'product_name': product_data['name']}, status=200)
        
        cart.append(pk)
        request.session['cart'] = cart

        return JsonResponse({'message': f'{product_data["name"]} added to cart.', 'product_name': product_data['name']}, status=201)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def cart(request):
    product_ids = request.session.get('cart', [])
    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)
    with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
        hosting_services = json.load(f)

    combined_products = products + hosting_services

    cart_products = [
        {**product, 'image': product['images'][0]}
        for product in combined_products
        if product['pk'] in product_ids
    ]

    total_price = sum(product['price'] for product in cart_products)
    form = OrderForm()

    return render(request, 'cart.html', {'products': cart_products, 'total_price': total_price, 'form': form})

def cart_count(request):
    count = len(request.session.get('cart', []))
    return JsonResponse({'cart_count': count})

@csrf_exempt
@require_POST
def clear_cart(request):
    try:
        del request.session['cart']
    except KeyError:
        pass  # Handle if 'cart' key doesn't exist

    return JsonResponse({'message': 'Cart cleared successfully.'}, status=200)



@csrf_exempt
@require_POST
def remove_from_cart(request, pk):
    cart = request.session.get('cart', [])

    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
        
        with open(settings.BASE_DIR / 'products.json', 'r') as f:
            products = json.load(f)
        with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
            hosting_services = json.load(f)
        
        combined_products = products + hosting_services

        product_data = next((product for product in combined_products if product['pk'] == pk), None)
        
        if product_data:
            return JsonResponse({'message': f'{product_data["name"]} removed from cart.', 'product_name': product_data['name']}, status=200)
        else:
            return JsonResponse({'message': 'Product removed from cart successfully.'}, status=200)
    else:
        return JsonResponse({'message': 'Product not found in cart.'}, status=404)
    


@csrf_exempt
def add_to_wishlist(request, pk):
    if request.method == 'POST':
        with open(Path(settings.BASE_DIR) / 'products.json', 'r') as f:
            products = json.load(f)
        with open(Path(settings.BASE_DIR) / 'hosting.json', 'r') as f:
            hosting_services = json.load(f)
        
        combined_products = products + hosting_services

        product_data = next((product for product in combined_products if product['pk'] == pk), None)
        
        if not product_data:
            return JsonResponse({'message': 'Product not found.'}, status=404)
        wishlist = request.session.get('wishlist', [])
        if pk in wishlist:
            return JsonResponse({'message': f'{product_data["name"]} is already in wishlist.', 'product_name': product_data['name']}, status=200)
        wishlist.append(pk)
        request.session['wishlist'] = wishlist

        return JsonResponse({'message': f'{product_data["name"]} added to wishlist.', 'product_name': product_data['name']}, status=201)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def wishlist(request):
    product_ids = request.session.get('wishlist', [])
    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)
    with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
        hosting_services = json.load(f)

    combined_products = products + hosting_services

    wishlist_products = [
        {**product, 'image': product['images'][0]} 
        for product in combined_products 
        if product['pk'] in product_ids
    ]
    
    return render(request, 'wishlist.html', {'products': wishlist_products})


def wishlist_count(request):
    count = len(request.session.get('wishlist', []))
    return JsonResponse({'wishlist_count': count})


@csrf_exempt
@require_POST
def remove_from_wishlist(request, pk):
    if 'wishlist' not in request.session:
        request.session['wishlist'] = []

    wishlist = request.session['wishlist']

    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)
    with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
        hosting_services = json.load(f)
    
    combined_products = products + hosting_services

    product_data = next((product for product in combined_products if product['pk'] == pk), None)
    if not product_data:
        return JsonResponse({'message': 'Product not found.'}, status=404)

    if pk in wishlist:
        wishlist.remove(pk)
        request.session['wishlist'] = wishlist
        return JsonResponse({'message': f'{product_data["name"]} removed from wishlist.', 'product_name': product_data['name']}, status=200)
    else:
        return JsonResponse({'message': 'Product not found in wishlist.'}, status=404)



def contact(request):
    return render(request, 'contact.html')

@csrf_protect
def send_message(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Construct the email subject and message
        subject = f'Message from {name}'
        email_message = f'You have received a new message from your website contact form.\n\n'
        email_message += f'Name: {name}\n'
        email_message += f'Email: {email}\n\n'
        email_message += f'Message:\n{message}\n'

        # Send the email
        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            ['nyphil515@gmail.com'],  # Replace with your email address
            fail_silently=False,
        )

   # Return a JSON response
        return JsonResponse({"message": "Message sent successfully"})
    
    return render(request, 'contact.html')





@csrf_exempt
@require_POST
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart_quantities = json.loads(request.POST.get('quantities', '[]'))

            # Retrieve products and hosting services from JSON files
            with open(settings.BASE_DIR / 'products.json', 'r') as f:
                products = json.load(f)
            with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
                hosting_services = json.load(f)
            
            combined_items = products + hosting_services

            # Filter selected products and services based on cart contents
            selected_items = []
            for item in combined_items:
                for cart_item in cart_quantities:
                    if item['pk'] == int(cart_item['pk']):
                        selected_items.append({
                            'pk': item['pk'],
                            'name': item['name'],
                            'quantity': int(cart_item['quantity']),
                            'price': float(item['price']),
                            'image': item.get('image', '')
                        })

            # Calculate total price of selected items
            total_price = sum(item['price'] * item['quantity'] for item in selected_items)

            # Save order details
            order = form.save(commit=False)
            order.product_ids = json.dumps(selected_items)  # Store items with quantities as JSON string
            order.total_price = total_price
            order.save()

            # Send order notification email
            #send_order_notification(order)

            # Return order_id in JSON response
            return JsonResponse({'order_id': order.pk})

        # Handle form errors if form is not valid

    # Handle invalid requests
    return redirect('cart')

    

def invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Parse product_ids JSON string into a list of dictionaries
    product_quantities = json.loads(order.product_ids)

    # Retrieve products and hosting services related to the order from your data source (e.g., JSON files)
    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)
    with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
        hosting_services = json.load(f)

    combined_items = products + hosting_services

    # Prepare ordered products and services with quantities and details
    ordered_items = []
    for item in product_quantities:
        product = next((p for p in combined_items if p['pk'] == item['pk']), None)
        if product:
            ordered_items.append({
                'name': product['name'],
                'price': product['price'],
                'quantity': item['quantity'],
                'image': product.get('images', [''])[0] if 'images' in product else None
            })

    context = {
        'order': order,
        'products': ordered_items,
        'total_price': order.total_price,  # Ensure total price is passed to the context
    }
    return render(request, 'invoice.html', context)                        


def hosting_services(request):
    with open(settings.BASE_DIR / 'hosting.json', 'r') as f:
        services = json.load(f)
    return render(request, 'hosting_services.html', {'services': services})


def starlink_items(request):
    with open(settings.BASE_DIR / 'starlink.json', 'r') as f:
        starlink = json.load(f)
    return render(request, 'starlink_items.html', {'starlink': starlink})






def test_email(request):
    try:
        send_mail(
            'Test Email Subject',
            'This is a test email body.',
            'nyphil515@gmail.com',  # Replace with your 'from' email address
            ['recipient@example.com'],  # Replace with a valid recipient email address
            fail_silently=False,
        )
        return HttpResponse('Email sent successfully.')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')