from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Pizza,Cart,PizzaCategory,CartItems

def home(request):
    pizzas = Pizza.objects.all()
    return render(request, 'home.html', {'pizzas': pizzas})

def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login')
                
        except Exception as e:
            messages.error(request, f"Error during login: {str(e)}")
            return redirect('login')
            
    return render(request, "Login.html")

def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            
            # Check if passwords match
            if password1 != password2:
                messages.error(request, "Passwords do not match")
                return redirect('register')
                
            # Check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('register')
                
            # Check if email exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return redirect('register')
                
            # Create user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1
            )
            
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('register')
            
    return render(request, "register.html")

def add_cart(request, pizza_uid):
    user=request.user;
    pizza_obj=Pizza.objects.get(uid=pizza_uid);
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    cart_Items=CartItems.objects.create(
        cart=cart,
        Pizza=pizza_obj
    )
    return redirect('home')