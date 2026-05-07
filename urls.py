from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #seller dashboard
    path('seller/', views.seller_page, name='seller'),
    
    path('Cart/', views.Cart, name='Cart'),
    #delte a product 

    path('Checkout/', views.Checkout, name='Checkout'),
    
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

 # alec's script to handoff the product id value specified at the end of the url
    path('product/<int:product_id>/', views.productRecordHandoff, name='product_detail'), 

    #alec's cart path to salida
    #path('cart/', views.cart_view, name='cart'),
]




