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
    # 1. Get the current user's profile and their specific cart
    # (Assuming the user is logged in)
    user_profile = UserProfile.objects.get(user=request.user)
    user_cart = Cart.objects.get(user=user_profile)
    
    # 2. Get the product they clicked on
    product_to_add = get_object_or_404(Product, id=product_id)
    
    # 3. Get the quantity from your dropdown menu
    qty = request.POST.get('quantity_selection', 1)

    # 4. Create the record in the CartItem table
    CartItem.objects.create(
        cart=user_cart,
        product=product_to_add,
        quantity=qty
    )

    # 5. Send them to the checkout page
    if request.POST.get('action') == 'buy_now':
        return redirect('checkout_page')
    
    return redirect('home')

# alec's function to get the login page 
def login_view(request):
    # Make sure 'login.html' matches your file name exactly
    return render(request, 'login.html')


# alec's function to get the account page 
def account_view(request):
    # Make sure 'login.html' matches your file name exactly
    return render(request, 'account.html')

# alec's function to get the logout page 
def logout_view(request):
    # Make sure 'login.html' matches your file name exactly
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

        # 1. Validation checks
        if not re.search(r"\d", pw) or not re.search(r"[ !@#$%^&*(),.?\":{}|<>]", pw):
            return render(request, 'createAccount.html', {'error': 'Password needs a number and symbol.'})

        if User.objects.filter(username=un).exists():
            return render(request, 'createAccount.html', {'error': 'Username already exists!'})

        # 2. The "Atomic" Database Save
# 2. The "Atomic" Database Save
        try:
            with transaction.atomic():
                # Step A: Create User (Triggers signal)
                new_account = User.objects.create_user(username=un, password=pw, email=em)
                
                # Step B: Get and update the profile
                user_profile = UserProfile.objects.get(user=new_account)
                user_profile.isSeller = role
                user_profile.save()
                
                # Step C: Create the Cart
                Cart.objects.get_or_create(user=user_profile)

            # Place these AFTER the atomic block is finished
            messages.success(request, f'Account created for {un}! You can now login.')
            print(f"--- DEBUG: Success! {un} created. ---")
            return redirect('login')

        except Exception as e:
            print(f"--- DEBUG: Something went wrong: {e} ---")
            # This 'error' key is what your HTML template looks for
            return render(request, 'createAccount.html', {'error': f'Database error: {e}'})
    
    # This return MUST be outside the 'if POST' block but inside the function
    return render(request, 'createAccount.html')