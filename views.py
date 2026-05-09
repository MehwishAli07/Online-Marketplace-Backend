from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile, Category, ProductCategory
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import re
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import UserProfile

# Create your views here.

#basic pages

#home page
def home(request):
    return render(request, 'index.html')

@login_required
# Seller update
def seller_page(request):
    #get logged-in user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # HANDLE POST REQUESTS
    if request.method == "POST":

        # Become Seller
        if "become_seller" in request.POST:
            profile.isSeller = True
            profile.save()
            return redirect("seller")
    

        #Only allow product actions if user is seller
        if profile.isSeller:

            # Get product_id (if exists → means EDIT mode)
            product_id = request.POST.get("product_id")

            # Get form data
            name = request.POST.get("name")
            description = request.POST.get("description")
            price = Decimal(request.POST.get("price", "0"))
            productimg = request.FILES.get("image")

            if product_id:
                product = get_object_or_404(
                    Product,
                    id=product_id,
                    seller=profile
                )

                product.name = name
                product.description = description
                product.price = price

                # Only update image if new one uploaded
                if productimg:
                    product.productimg = productimg

                product.save()

        
            # Create new product
            else:
                Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    productimg=productimg,
                    seller=profile
                )

            return redirect("seller")

   
    # Get products for current seller
    products = Product.objects.filter(seller=profile)

    # redner page
    return render(request, "seller.html", {
        "products": products,
        "profile": profile
    })   

#delete product
@login_required
def delete_product(request, product_id):
    # get logged-in user's profile
    profile = UserProfile.objects.get(user=request.user)

    # get product belonging to this user only
    product = Product.objects.get(id=product_id, seller=profile)

    # only delete if request is POST (safety)
    if request.method == "POST":
        product.delete()

    # redirect back to seller page
    return redirect("seller")

#Alec's Product Record Handoff function.. this is what allows records to move between caden, alec, and salida's urls so we can
#source database from each webpage but ensure the same product is being referenced. this function is to be used on the reciever url page 
def productRecordHandoff(inputRequest, product_id):

    product = get_object_or_404(Product, id=product_id)#grab product id 
    
    
    return render(inputRequest, 'product_details.html', { #put the product into necessary webpage
        'product': product
    })

#script to connect alec's checkout button to salida's checkout page 
def checkout_view(request):
    """
    Renders Salida's checkout page.
    """
    return render(request, 'Checkout.html')

# Online_Marketplace/views.py
from .models import Cart, CartItem  # These match your models.py

#alec's function to send the product and the number of products selected from productdetails page to the backend shopping cart 
def add_to_cart(request, product_id):
    
    #get user profile and their cart 
    user_profile = UserProfile.objects.get(user=request.user)
    user_cart = Cart.objects.get(user=user_profile)
    
    #get product usear clicked on and get the quantity
    product_to_add = get_object_or_404(Product, id=product_id)
    qty = request.POST.get('quantity_selection', 1)

    #make a record in the cart item table in the backend... 
    CartItem.objects.create(
        cart=user_cart,
        product=product_to_add,
        quantity=qty
    )

    #send the user to salida's checkout page.. 
    if request.POST.get('action') == 'buy_now':
        return redirect('checkout_page')
    
    return redirect('home')

from django.contrib import messages

#alecs function to handle login page errors, messages, lockout, and standard 
def login_view(request):

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        try:
            #look up the user and their profile 
            user_obj = User.objects.get(username=user_name)
            profile = UserProfile.objects.get(user=user_obj)  
            #if the account is already locked then block 
            if profile.is_locked:
                messages.error(request, "your account is locked.")
                return render(request, 'login.html')
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            profile = None 

        #authenticate the user 
        user = authenticate(request, username=user_name, password=pass_word)

        #if user exists in backend database 
        if user is not None:
            #reset login attempts and login 
            if profile:
                profile.login_attempts = 0
                profile.save()
                profile.refresh_from_db()
            login(request, user)
            return redirect('home')

        #throw the logic for login attemps number 
        else:
            if profile:
                profile.login_attempts += 1
                if profile.login_attempts >= 6:
                    profile.is_locked = True
                profile.save()
                profile.refresh_from_db()
                
                # message based on how many tries they have left
                if profile.is_locked:
                    messages.error(request, "You have failed to login too many times. Your account is now locked.")
                else:
                    left = 6 - profile.login_attempts
                    messages.error(request, f"Invalid password. You have {left} attempts remaining.")

            #logic for if the user doesn't even exist in the database 
            else:
                messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    # if get request, just show the page 
    return render(request, 'login.html')


# alec's function to get the account page 
def account_view(request):
    return render(request, 'account.html')

# alec's function to get the logout page 
def logout_view(request):
    logout(request) 
    return render(request, 'logout.html') 

# caden's products
def Products_view(request):
    query = request.GET.get("q", "")
    selected_categories = request.GET.getlist("category")

    products = Product.objects.all()

    # Search filter
    if query:
        products = products.filter(name__icontains=query)

    # Category filter
    if selected_categories:
        products = products.filter(
            productcategory__category__categoryName__in=selected_categories
        ).distinct()

    # Load all categories for the filter list
    categories = Category.objects.all()
    #grab info from database and sends it to the render page
    return render(request, "Products.html", {
        "products": products,
        "categories": categories,
        "selected_categories": selected_categories,
        "query": query,
    })

#alec's function to send the account creation fields to the backend tables that django has set up
def register_user(request):

    if request.method == 'POST':
        un = request.POST.get('username')
        pw = request.POST.get('password')
        em = request.POST.get('email')
        role = request.POST.get('account_type') == 'seller'

        # validation check.. give a message if the user enters the wrong type of password 
        if not re.search(r"\d", pw) or not re.search(r"[ !@#$%^&*(),.?\":{}|<>]", pw):
            return render(request, 'createAccount.html', {'error': 'password needs a number and symbol.'})

        #validation check for the username already existing 
        if User.objects.filter(username=un).exists():
            return render(request, 'createAccount.html', {'error': 'that username already exists!'})

        # save info into the database 
        try:
            with transaction.atomic():
                # create the user and update the profile 
                new_account = User.objects.create_user(username=un, password=pw, email=em)
                user_profile = UserProfile.objects.get(user=new_account)
                user_profile.isSeller = role
                user_profile.save()
                
                # now make the cart and attach it to the user 
                Cart.objects.get_or_create(user=user_profile)

            # success message after the account has been created 
            messages.success(request, f'Account created for {un}! You can now login.')
            return redirect('login')

        # if something goes wrong through this 
        except Exception as e:
            return render(request, 'createAccount.html', {'error': f'Database error: {e}'})
    
    # return the request to create the account 
    return render(request, 'createAccount.html')

