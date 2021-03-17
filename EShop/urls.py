from django.urls import path
from .views import *

app_name = 'EShop'
urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('all-products/',AllProductsView.as_view(), name='allproducts'),
    path('product/<slug:slug>/',ProductDetailView.as_view(), name='productdetail'),

    path('add-to-cart-<int:pro_id>/',AddToCartView.as_view(), name='addtocart'),
    path('my-cart/', MyCartView.as_view(), name='mycart'),
    path('manage-cart/<int:cp_id>/', ManageCartView.as_view(), name='managecart'),
    path('empty-cart/', EmptyCartView.as_view(), name='emptycart'),

    path('checkout/', CheckOutView.as_view(), name='checkout'),

    path('register/', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),
    path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),

    path('Profile/', CustomerProfileView.as_view(), name='customerprofile'),
    path('profile/order-<int:pk>/', CustomerOrderDetailView.as_view(), name='customerorderdetail'),

    path('search/', SearchView.as_view(), name='search'),


    path('admin-login/', AdminLoginView.as_view(), name='adminlogin'),
    path('admin-home/', AdminHomeView.as_view(), name='adminhome'),
    path('admin-orderdetail/<int:pk>/', AdminOrderDetailView.as_view(), name='adminorderdetail'),
    path('admin-orders-list/', AdminOrderListView.as_view(), name='adminorderlist'),
    path('admin-order-<int:pk>-change/', AdminorderStatusChangeView.as_view(), name='adminorderstatuschange'),


]