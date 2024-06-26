from django.urls import path
from .views import view_products,cart,category_products,cart_details,update_cart,shipping,process_order,register,login,logout
urlpatterns=[
    path('products',view_products),
    path('category/<str:category>',category_products),
    path('addcart',cart),
    path('updatecart',update_cart),
    path('cartdetails',cart_details),
    path('shipping',shipping),
    path('processorder',process_order),
    path('register',register),
    path('login',login),
    path('logout',logout)
]