from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #seller dashboard
    path('seller/', views.seller_page, name='seller'),
    
    # Shopping cart page
    path('Cart/', views.shopping_cart, name='Cart'),
    path('add/<int:product_id>/', views.addProductCart, name='addProductCart'),
    path('remove/<int:item_id>/', views.removeFromCart, name='removeFromCart'),

    # Checkout page
    path('Checkout/', views.Checkout, name='Checkout'),


     #delte a product 
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

 # alec's script to handoff the product id value specified at the end of the url
    path('product/<int:product_id>/', views.productRecordHandoff, name='product_detail'), 

    #alec's cart path to salida
    #path('cart/', views.cart_view, name='cart'),
]







