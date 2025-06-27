from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name="Home"),
    path('product/<slug:slug>', product, name="Product"),
    path('product-list/<slug:slug>', product_list, name="Product_List"),
    path('search-results/', SearchView.as_view(), name="Search Results"),
    path('register/', RegisterUser.as_view(), name="Register"),
    path('login/', LoginUser.as_view(), name="Login"),
    path('logout/', logout_user, name="Log out"),
    path('checkout/', checkout, name="Checkout"),
    path('payment/', payment, name="Payment"),
    path('favourites/', favourites, name="Favourites"),

]

htmxpatterns = [
    path('search/', search_tab, name="Tab Results"),
    path('cart/', cart, name="Cart"),
    path('update-cart/<slug:slug>/<str:button_value>', update_cart, name="Update Cart"),
    path('add-to-cart/<slug:slug>', add_to_cart, name="Add to cart"),
    path('add-product-page/<slug:slug>', add_product_page, name="Add product page"),
    path('add-favourite/<slug:slug>', add_to_favourites, name="Add to Favourites"),
    path('cart/quantity-fragment/', cart_quantity, name="Update cart quantity")
]

urlpatterns += htmxpatterns