from django.urls import path
from .views import *
from . import views

app_name = 'EShop'
urlpatterns = [

    # root pages
    path('', HomeView.as_view(), name='home'),
    path('About/', AboutView.as_view(), name='about'),
    path('Contact/', ContactView.as_view(), name='contact'),
    path('All-products/', AllProductsView.as_view(), name='allproducts'),
    path('Product/<slug:slug>/', ProductDetailView.as_view(), name='productdetail'),

    # cart urls
    path('Add-to-cart-<int:pro_id>/', AddToCartView.as_view(), name='addtocart'),
    path('My-cart/', MyCartView.as_view(), name='mycart'),
    path('Manage-cart/<int:cp_id>/', ManageCartView.as_view(), name='managecart'),
    path('Empty-cart/', EmptyCartView.as_view(), name='emptycart'),

    # checkout url
    path('Checkout/', CheckOutView.as_view(), name='checkout'),

    # authentication urls
    path('Register/', CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),
    path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
    path('reset-password/', ResetPasswordView.as_view(), name='resetpassword'),

    # my profile url
    path('Profile/', CustomerProfileView.as_view(), name='customerprofile'),
    path('profile/order-<int:pk>/', CustomerOrderDetailView.as_view(),
         name='customerorderdetail'),

    # serching url
    path('search/', SearchView.as_view(), name='search'),

    # admin urls
    path('admin-login/', AdminLoginView.as_view(), name='adminlogin'),
    path('admin-home/', AdminHomeView.as_view(), name='adminhome'),
    path('admin-orderdetail/<int:pk>/',
         AdminOrderDetailView.as_view(), name='adminorderdetail'),
    path('admin-orders-list/', AdminOrderListView.as_view(), name='adminorderlist'),
    path('admin-order-<int:pk>-change/',
         AdminorderStatusChangeView.as_view(), name='adminorderstatuschange'),
    path('admin-product-list/', AdminProductListView.as_view(),
         name='adminproductlist'),
    path('admin-product-detail/<int:pk>/',
         AdminProductDetailView.as_view(), name='adminproductdetail'),
    path('admin-product-create/', AdminProductCreateView.as_view(),
         name='adminproductcreate'),

    path('admin-product-create-many/',
         AdminProductCreateView.as_view(), name='adminproductcreatemany')

]
