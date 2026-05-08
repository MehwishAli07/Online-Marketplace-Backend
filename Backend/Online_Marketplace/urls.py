from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #seller dashboard
    path('seller/', views.seller_page, name='seller'),
    
    #delte a product 
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # alec's script to handoff the product id value specified at the end of the url
    path('product/<int:product_id>/', views.productRecordHandoff, name='product_detail'), 

    #alec's checkout path button 
    path('checkout/', views.checkout_view, name='checkout_page'),

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
]
