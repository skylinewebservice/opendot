from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Cart, CartItem, Wishlist, Product, Order
from .forms import OrderForm
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from .models import Product
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from django.views.decorators.http import require_POST




def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def service(request):
    return render(request, 'service.html')


def why(request):
    return render(request, 'why.html')


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

        product_data = next((product for product in products if product['pk'] == pk), None)
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

    cart_products = [
        {**product, 'image': product['images'][0]}
        for product in products
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

        product_data = next((product for product in products if product['pk'] == pk), None)
        
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
        product_data = next((product for product in products if product['pk'] == pk), None)
        
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

    wishlist_products = [
        {**product, 'image': product['images'][0]} 
        for product in products 
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

    product_data = next((product for product in products if product['pk'] == pk), None)
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


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart_quantities = json.loads(request.POST.get('quantities', '[]'))

            # Retrieve products from JSON file or database
            with open(settings.BASE_DIR / 'products.json', 'r') as f:
                products = json.load(f)

            # Filter selected products based on cart contents
            selected_products = []
            for product in products:
                for item in cart_quantities:
                    if product['pk'] == int(item['pk']):
                        selected_products.append({
                            'pk': product['pk'],
                            'name': product['name'],
                            'quantity': int(item['quantity']),
                            'price': float(product['price']),
                            'image': product.get('image', '')
                        })

            # Calculate total price of selected products
            total_price = sum(product['price'] * product['quantity'] for product in selected_products)

            # Save order details
            order = form.save(commit=False)
            order.product_ids = json.dumps(selected_products)  # Store products with quantities as JSON string
            order.total_price = total_price
            order.save()

            # Clear cart after order is placed
            # request.session['cart'] = []

            # Return order_id in JSON response
            return JsonResponse({'order_id': order.pk})

        # Handle form errors if form is not valid

    # Handle invalid requests
    return redirect('cart')

def invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Parse product_ids JSON string into a list of dictionaries
    product_quantities = json.loads(order.product_ids)

    # Retrieve products related to the order from your data source (e.g., JSON file)
    with open(settings.BASE_DIR / 'products.json', 'r') as f:
        products = json.load(f)

    # Prepare ordered products with quantities and details
    ordered_products = []
    for item in product_quantities:
        product = next((p for p in products if p['pk'] == item['pk']), None)
        if product:
            ordered_products.append({
                'name': product['name'],
                'price': product['price'],
                'quantity': item['quantity'],
                'image': product.get('images', [''])[0] if 'images' in product else None
            })

    context = {
        'order': order,
        'products': ordered_products,
        'total_price': order.total_price,  # Ensure total price is passed to the context
    }
    return render(request, 'invoice.html', context)