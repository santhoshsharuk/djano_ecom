from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, _ = CartItem.objects.get_or_create(product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def cart(request):
    items = CartItem.objects.all()
    return render(request, 'store/cart.html', {'items': items})

def checkout(request):
    order = Order.objects.create()
    for item in CartItem.objects.all():
        order.items.add(item)
    CartItem.objects.all().delete()
    return render(request, 'store/checkout.html', {'order': order})

# Update cart (increase/decrease quantity)
def update_cart(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart')


def remove_from_cart(request, item_id):
    # Get the cart item by its ID and delete it
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    
    # Redirect back to the cart page after removal
    return redirect('cart')


def checkout(request):
    # Your checkout logic here
    return render(request, 'store/checkout.html')