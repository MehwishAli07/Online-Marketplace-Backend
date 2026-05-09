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

    # ShoppingCart Page
@login_required
def shopping_cart(request):
        return render(request, "Shopping_Cart.html", {
            "cart_items": [],
            "total": 0
        })
    user_profile=UserProfile.objects.get(user=request.user)
    user_cart = Cart.objects.filter(user=user_profile).first()
    cart_items = CartItem.objects.filter(cart=user_cart)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "Shopping_Cart.html", {
    "cart_items": cart_items,
    "total": total
})

    # Checkout Page
@login_required
def Checkout(request):
    user_profile=UserProfile.objects.get(user=request.user)
    cart = Cart.objects.filter(user=user_profile).first()
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        #Saving the order
        order = Order.objects.create(
            user=user_profile,
            billing=request.POST['full_name'],
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            country=request.POST['country'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip_code=request.POST['zip_code'],
        )
        # Saving the items to cart
        for item in cart_items:
            OrderItem.objects.create(
                 order=order,
                 product=item.product,
                 quantity=item.quantity,
                 priceAtPurchase=item.product.price,
           )
        # After checkout cart clears
        cart_items.delete()
        return redirect('/Checkout/?ordered=true')
    return render(request, 'Checkout.html',{
        'cart_items': cart_items,
        'total':total,
    })

#Alec's Product Record Handoff function.. this is what allows records to move between caden, alec, and salida's urls so we can
#source database from each webpage but ensure the same product is being referenced. this function is to be used on the reciever url page 
def productRecordHandoff(inputRequest, product_id):

    product = get_object_or_404(Product, id=product_id)#grab product id 
    
    return render(inputRequest, 'product_details.html', { #put the product into necessary webpage
        'product': product
    })

def addProductCart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product = product,
    user = request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('Cart')

def removeFromCart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('Cart')



