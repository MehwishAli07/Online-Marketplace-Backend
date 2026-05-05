from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile

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