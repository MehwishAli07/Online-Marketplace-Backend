from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #seller dashboard
    path('seller/', views.seller_page, name='seller'),
    
    #delte a product 
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]



