from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile
from django.shortcuts import redirect, get_object_or_404
from .models import Cart, CartItem, Product, UserProfile

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

# alec's function to get the create Account page 
def createAccount_view(request):
    # Make sure 'login.html' matches your file name exactly
    return render(request, 'createAccount.html')

# alec's function to get the account page 
def account_view(request):
    # Make sure 'login.html' matches your file name exactly
    return render(request, 'account.html')

# caden's products
def Products_view(request):
    # Make sure 'login.html' matches your file name exactly
    return render(request, 'Products.html')