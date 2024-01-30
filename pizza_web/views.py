from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, FoodItem, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

# Create your views here.

def register(request):
    
    if request.user.is_authenticated:
            messages.error(request, 'You are already logged in.')
            return redirect('product_page')
        
    if request.method == 'POST':
        username = request.POST['reg-email']
        password = request.POST['reg-password']
        re_password = request.POST['reg-re-password']
        name = request.POST['reg-name']

        # Check if passwords match
        if password != re_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'login_register_page/login_register.html')
        
        try:
            # Validate the password using Django's validators
            validate_password(password, user=User)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return render(request, 'login_register_page/login_register.html')

        # Check if the username (email) is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Email is already taken. Please choose a different one.')
            return render(request, 'login_register_page/login_register.html')

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.first_name = name
        user.save()

        # Create UserProfile
        UserProfile.objects.create(user=user, name=name)

        # Log in the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_page')  # Replace 'dashboard' with your actual URL

    return render(request, 'login_register_page/login_register.html')

def user_login(request):
    
    if request.user.is_authenticated:
            messages.error(request, 'You are already logged in.')
            return redirect('product_page')
        

    if request.method == 'POST':
        username = request.POST['login-email']
        password = request.POST['login-password']

        # Authenticate and login the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_page')  # Replace 'dashboard' with your actual URL
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login_register_page/login_register.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def product_page(request):
    pizza_products = FoodItem.objects.filter(item_type='pizza')
    burger_products = FoodItem.objects.filter(item_type='burger')
    sandwich_products = FoodItem.objects.filter(item_type='sandwich')
    dessert_products = FoodItem.objects.filter(item_type='dessert')
    drinks_products = FoodItem.objects.filter(item_type='drinks')
    
    context = {
        'pizza_products': pizza_products,
        'burger_products': burger_products,
        'sandwich_products': sandwich_products,
        'dessert_products': dessert_products,
        'drinks_products': drinks_products,
    }
    
    
    return render(request, 'product_page/product.html', context)

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = FoodItem.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)

    # Check if the item is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        # If the item already exists in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    # Redirect to the product page or any other page as per your requirement
    return redirect('product_page')

@login_required(login_url='login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total cost based on the quantity of each item
    total_cost = sum(item.product.discounted_price * item.quantity for item in cart_items)
    total_cost = round(total_cost, 2)

    context = {'cart_items': cart_items, 'total_cost': total_cost}
    return render(request, 'cart_page/cart.html', context)

@login_required(login_url='login')
def update_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()

    # Calculate the total cost based on the quantity of each item
    cart_items = CartItem.objects.filter(cart=cart_item.cart)
    total_cost = sum(item.product.discounted_price * item.quantity for item in cart_items)
    total_cost = round(total_cost, 2)

    cart_item.cart.total_cost = total_cost
    cart_item.cart.save()

    return redirect('view_cart')

@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()

    return redirect('view_cart')