from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #seller dashboard
    path('seller/', views.seller_page, name='seller'),
    
    # Shopping cart page
    path('ShoppingCart/', views.shopping_cart, name='ShoppingCart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.removeFromCart, name='removeFromCart'),

    # Checkout page
    path('Checkout/', views.Checkout, name='Checkout'),


     #delte a product 
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

 # alec's script to handoff the product id value specified at the end of the url
    path('product/<int:product_id>/', views.productRecordHandoff, name='product_detail'), 


    # alec's login page path 
    path('login/', views.login_view, name='login'),

    # alec's createAccount page path 
    path('createAccount/', views.register_user, name='createAccount'),

    # alec's account page path 
    path('account/', views.account_view, name='account'),

    # alec's logout page path 
    path('logout/', views.logout_view, name='logout'),

    #cadens' products page 
    path('Products/', views.Products_view, name='Products'),

    # Add this line to your urlpatterns
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]




