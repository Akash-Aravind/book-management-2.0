from django.urls import path, include, re_path
from . import views
from django.views.static import serve
from django.conf import settings
app_name = "root"

urlpatterns = [

    path('', views.HomePage.as_view(), name="home"),
    path('accounts/', include('allauth.urls'), name="account"),
    path('details/<str:title>/',
         views.DetailPage.as_view(), name="detail"),

    path('search/', views.SearchPage, name="search"),
    path('search/details/<str:title>/',
         views.DetailPage.as_view(), name="detail2"),

    path('wishlist/<int:isbn>/<str:title>/', views.wishlist, name="wishls"),
    path('wishlist/', views.WishListView.as_view(), name="wish"),

    path('wishlist/details/<str:title>/',
         views.DetailPage.as_view(), name="detail3"),

    path('wishlist/remove/<str:isbnum>/', views.removewishlist, name="remove")
]
