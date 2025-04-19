from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from .models import Pizza,Cart,PizzaCategory,CartItems,OrderDetails
from django.contrib.auth import logout as auth_logout
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

def custom_logout(request):
    auth_logout(request)
    return redirect("home")


def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        return render(request, "Cart.html", {"carts": cart})
    except Cart.DoesNotExist:
        return render(request, "Cart.html", {"carts": None})
    
def remove_item(request, item_uid):
    try:
        item = CartItems.objects.get(uid=item_uid, cart__user=request.user)
        item.delete()
        messages.success(request, "Item removed from cart")
    except CartItems.DoesNotExist:
        messages.error(request, "Item not found in your cart")
    return redirect('cart')    



def Oder(request):
    Orders = Cart.objects.filter(is_paid=True, user=request.user).order_by('-created_at')
    return render(request, "Order.html", {"Oders": Orders})



def checkout(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        if request.method == "POST":
            # Process the order
            full_name = request.POST.get('full_name')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            payment_method = request.POST.get('payment_method')
            
            # Create order details
            OrderDetails.objects.create(
                cart=cart,
                full_name=full_name,
                address=address,
                phone=phone,
                payment_method=payment_method
            )
            
            # Mark cart as paid
            cart.is_paid = True
            cart.save()
            
            messages.success(request, "Order placed successfully!")
            return redirect('Order')
            
        return render(request, "checkout.html", {"cart": cart})
    except Cart.DoesNotExist:
        messages.error(request, "No active cart found")
        return redirect('home')