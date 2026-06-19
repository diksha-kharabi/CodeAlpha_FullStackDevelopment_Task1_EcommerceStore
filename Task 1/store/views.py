from django.shortcuts import render, redirect
from .models import Product, Cart


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, id):
    product = Product.objects.get(id=id)

    Cart.objects.create(
        product=product,
        quantity=1
    )

    return redirect('/')


def cart(request):
    cart_items = Cart.objects.all()

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


from .models import Product, Cart, Order

def checkout(request):
    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    Order.objects.create(total_amount=total)

    cart_items.delete()

    return redirect('/')


from django.contrib.auth.models import User
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/')

    return render(request, 'register.html')


from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('/')