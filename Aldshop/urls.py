from django.conf import settings
from django.conf.urls.static import static
from Aldshop import views
from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    
    path('admin_sign_in', views.admin_sign_in),
    path('admin_sign_out', views.admin_sign_out),
    path('admin_panel', views.admin_panel),
    path('admin_add_product', views.admin_add_product),
    path('admin_thankyou_for_adding_product', views.admin_thankyou_for_adding_product),
    path('admin_list_product', views.admin_list_product),
    path('admin_add_category', views.admin_add_category),
    path('admin_list_category', views.admin_list_category),
    path('admin_list_customer', views.admin_list_customer),
    path('admin_edit_Product', views.admin_edit_Product),
    path('admin_edit_category/<str:cat_id>', views.admin_edit_category),
    path('admin_category_delete', views.admin_category_delete),
    path('admin_order_details/<str:order_id>', views.admin_order_details),
    path('admin_list_orders', views.admin_list_orders),
    path('admin_edit_banner', views.admin_edit_banner),
    path('admin_add_banner', views.admin_add_banner),
    path('admin_update_user_status', views.admin_update_user_status),
    path('admin_change_order_status', views.admin_change_order_status),
    path('admin_update_order_status', views.admin_update_order_status),
    path('admin_get_graph_data', views.admin_get_graph_data),
    path('admin_sales_report', views.admin_sales_report),
    path('admin_category_offers', views.admin_category_offers),
    path('admin_product_offers', views.admin_product_offers),
    path('admin_forget_password', views.forget_password),
    path('admin_remove_coupon', views.admin_remove_coupon),
    path('admin_add_coupon', views.admin_add_coupon),
    
    
    path('', views.root),
    path('user_home', views.user_home),
    path('user_sign_in', views.user_sign_in),
    path('user_sign_up', views.user_sign_up),
    path('welcome_new_user', views.welcome_new_user),
    path('user_sign_out', views.user_sign_out),
    path('user_product_detail/<str:product_id>', views.user_product_detail),
    path('user_add_to_cart', views.user_add_to_cart),
    path('user_delete_cart_item', views.user_delete_cart_item),
    path('user_view_cart', views.user_view_cart),
    path('user_cart_empty', views.user_view_cart),
    path('user_update_cart', views.user_update_cart),
    path('user_check_cart_or_shop', views.user_check_cart_or_shop),
    path('user_checkout', views.user_checkout),
    path('user_add_address', views.user_add_address),
    path('user_thankyou_for_order', views.user_thankyou_for_order),
    path('user_otp_sign_in', views.user_otp_sign_in),
    path('user_otp_sign_in_validation', views.user_otp_sign_in_validation),
    path('user_account', views.user_account),
    path('user_products', views.user_products),
    path('user_category_view/<str:name>', views.user_category_view),
    path('user_update_user/<str:user_id>', views.user_update_user),
    path('user_update_order_status', views.user_update_order_status),
    path('user_edit_address/<str:address_id>', views.user_edit_address),
    path('user_delete_address', views.user_delete_address),
    path('search_engine', views.search_engine),
    path('user_invoice_per_item/<str:id>', views.user_invoice_per_item),
    path('user_invoice', views.user_invoice),
    path('user_validate_coupon', views.user_validate_coupon),
    path('user_return_order/<str:order_id>', views.user_return_order),
    path('user_forget_password', views.forget_password),
    path('user_wallet', views.user_wallet),
    path('user_export_myorders_in_csv', views.user_export_myorders_in_csv),
    
    
   path('user_paypal_place_order', views.user_paypal_place_order, name='user_paypal_place_order'),
   path('user_razorpay_place_order', views.user_razorpay_place_order, name='razorpay_success'),
   path('user_pay_with_wallet', views.user_pay_with_wallet, name='user_pay_with_wallet'),
 
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)