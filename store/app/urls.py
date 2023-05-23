from django.contrib.auth import views as auth_view
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('k', views.home, name="home"),
    path('admin', views.admin, name="admin_dashboard"),
    path('user', views.user, name="user_dashboard"),
    path('productview/', views.ProductView.as_view(), name="product-view"),
    path('productadd/', views.productadd, name="product-add"),
    path('productupdate/<str:pk>/', views.ProductUpdate.as_view(), name="productupdate"),
    path('enable/<str:pk>/', views.enableview, name='productenable'),
    path('product/disable/', views.disableview, name='productedisable'),
    path('update_products/', UpdateProduct.as_view(), name='update_product'),

    path('subproduct/', views.subproductview, name="subproductview"),
    # path('subproductadd/', views.subproductadd, name="subproductadd"),
    path('variants/create/', CreateVariantView.as_view(), name='subproductadd'),



    path('varient/<int:pk>/update/', SubProductUpdate.as_view(), name='subproductupdate'),
    path('varenable/<str:pk>/', views.enablevariant, name='variantenable'),
    path('vardisable/dis', views.disablevariant, name='variantdisable'),

    path('cart', views.CartView.as_view(), name="userview"),



    path('add-to-cartss/<int:product_id>/', views.add_to_carts, name='addtocarts'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # path('cart/', views.cart, name='cart'),

    path('cart/update/<int:pk>/<str:action>/', views.cart_updates, name='cart_update'),
    path('productcart/updates/<int:pk>/<str:action>/', product_cart_updates, name='cart_updates'),#ajax


    path('', views.UserProduct.as_view(), name="userproduct"),
    path('guest/user', views.UserProduct.as_view(), name="questview"),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='productdetail'),
    path('product/<int:pk>/', views.productdetail, name='product-detail'),
    #


    path('register/', views.register, name='register'),

    # path('login/', LoginView.as_view(template_name='userlogin/login.html'), name='login'),
    path('login/', views.custom_login, name='login'),
    path('login/accounts/dashboard/', dashboard, name='dashboard'),
    path('', auth_view.LogoutView.as_view(template_name='user/productview.html'), name="logoutss"),
    path('logout/', logout_view, name='logout'),

    path('wishlist', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wish/delete/<int:pk>/', YourModelDeleteView.as_view(), name='wish-delete'),
    path('wishto-cart/<int:product_id>/', views.wishtocart, name='wish-tocart'),

    path('checkout/', views.checkout, name='check_out'),
    path('checkoutform/', views.checkoutform, name='checkouts'),


    path('order/list', views.OrderList.as_view(), name="orderlist"),
    path('address/', views.useraddress, name='user_shipping'),
    path('myorder/', views.myorder, name='my_order'),
    path('myorder/<str:order_id>/', views.myorder_detail, name='myorder_detail'),

    path('profileview/', views.UserProfileView, name='myprofile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change/pswd/', views.changepswd, name='chpswd'),
    path('profileviewsss/', views.ProfileView, name='dashUserprofile'),

    path('order/success/<int:order_id>/', OrderSuccessView.as_view(), name='ordersuccess'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('cart/quantity/', views.cartquantity, name='cartquantity'),

    # password reset
    path('password_reset/', PasswordResetView.as_view(template_name='forgot/password_reset_email.html'),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='forgot/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='forgot/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='forgot/password_reset_complete.html'),
         name='password_reset_complete'),

    # path('login/user', views.LoginUser.as_view(), name="login_user"),
    path('login/user', product_list, name='login_user'),

    path('order/<str:order_id>/', views.order_detail, name='order_detail'),

    path('checkout/product/<int:product_id>/', views.directbuy, name='direct_buy'),
    path('direct/order/form/<int:product_id>/', views.directorderform, name='dirctfrm'),
    path('direct/success/order/<int:order_id>/', DirectOrdersuccess.as_view(), name='directordersuccess'),

    path('password/change/', MyPasswordChangeView.as_view(), name='password_change'),

    # path('update/<int:pk>/', views.update_varient, name='update_varient'),

    path('add-to-carts/<int:product_id>/', GuestAddToCartView.as_view(), name='add_to_cart'),
    path('guest/cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart_to_wish/<int:product_id>/', Cart_To_Wish.as_view(), name='cart_to_wish'),

    path('cart/delete/<int:pk>/', delete_cart_product.as_view(), name='delete_cart_products'),

    path('guest/cart/update/<int:pk>/<str:action>/', views.guest_cart_updates, name='cart_guest_update'),

    path('signupv/', views.signup, name='signup'),
    # path('signupv/', SignupView.as_view(), name='signup'),

    # path('delete/guest/<int:product_id>/', DeleteGuestCart.as_view(), name='delete_product'),
    path('guest/delete/<int:product_id>/', delete_product, name='delete_product'),

    path('cart/', CartViews.as_view(), name='cart'),
    path('cart/delete/<int:pk>/', CartView.as_view(), name='delete_cart_product'),

    path('updatesdisable/<int:pk>/', views.updatedisable, name='updatedisable'),

    path('add-to-wish/<int:product_id>/', GuestAddToWishView.as_view(), name='add_to_wish'),

    path('guest/wish/', WishDetailView.as_view(), name='wish_detail'),

    path('wish/guest/delete/<int:product_id>/', delete_wish_product, name='delete_wish_product'),

    path('order/<int:pk>/change-status/', views.change_order_status, name='change_order_status'),


    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),


    path('guest/checkout/product/<int:product_id>/', GuestDirectBuy.as_view(), name='guest_direct_buy'),

    path('re-order/<str:order_id>/', re_order, name='re_order'),


    path('order/approve/<str:product_id>/', views.admin_order_approves, name='order_cancel_approve'),
    path('order/approve/updation/<str:product_id>/<str:action>/', views.admin_order_approves_updation, name='order_cancel_approve_updation'),

    path('filter-products/', views.filter_products, name='filter_products'),

    path('search/', views.search_product, name='search_product'),

]
