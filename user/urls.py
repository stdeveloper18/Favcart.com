from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('home/', views.index),
    path('', views.index),
    path('about/', views.about),
    path('product/', views.product),
    path('myorder/', views.myorder),
    path('enquiry/', views.enquiry),
    path('signup/', views.signup),
    path('profile/', views.myprofile),
    path('signin/', views.signin),
    path('mens/', views.mens),
    path('womens/', views.womens),
    path('kids/', views.kids),
    path('viewproduct/', views.viewproduct),
    path('signout/', views.signout),
    path('myordr/', views.myordr),
    path('mcart/', views.mycart),
    path('showcart/', views.showcart),
    path('cpdetail/', views.cpdetail),
    path('mypage/', views.mypage),
    path('search/', views.search),

]