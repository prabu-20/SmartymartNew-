from django.urls import path
from .views import *

urlpatterns = [
    path('' , HomePage , name="home"),
    path('register/' , RegisterForm,name="register"),
    path('login/',login_page,name="login"),
    path('logout/',logout_page,name="logout"),
    path('collections/',Collections,name="collections"),
    path('wish_list/', WishList,name="wish_list"),
    path('fav',fav_page,name="fav"),
    path('remove_fav/<str:fid>/', removefav,name="remove_fav"),
    path('add_cart/', AddToCart,name="add_cart"),
    path('remove_cart/<str:cid>/', removecart,name="remove_cart"),
    path('collections/<str:name>/',collectionview,name="collectionsview"),
    path('collections/<str:cname>/<str:pname>/',product_details,name="product_details"),
    path('addtocart/' , add_to_cart, name="addtocart"),
    path("search/", search_view, name="search"),
]