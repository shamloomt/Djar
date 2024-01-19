from django.urls import path
from adminpanel.views import GetAll_Product, GetAll_Categories, get_product_with_cat #,GetAll_Cart, post_addToCart
from .import views
from django.utils.encoding import uri_to_iri

urlpatterns = [

    ## PRODUCT AND CATEGORY ##
    path('get-all-product/', GetAll_Product.as_view()),
    path('get-all-cat/', GetAll_Categories.as_view()),
    path('get-prwcat/<int:catID>/', get_product_with_cat.as_view()),
    path('get-product/<int:pk>/', views.get_productSingle),
    path('update-product/<int:pk>/', views.update_product),

    ## CART ##
    path('Cart-view/<int:pk>/',views.Cart_View), #user ID
    path('Cart-add/',views.Cart_Add),
    path('Cart-update/<int:pk>/',views.Cart_Update), #cart ID
    path('Cart-delete/<int:pk>/',views.Cart_Delete),
    path('Cart-merge-orders/<int:uid>/<int:oid>/',views.Cart_Merge_Order), #user_id #order_id
    
    ## ORDERS ##
    path('user-Orders-view/<int:pk>/',views.User_Orders_View), #user_id
    path('Order-view/<int:pk>/',views.Order_View), #order_id
    path('Order-dtails-View/<int:pk>/', views.Order_dtails_View), #order_id
    path('Order-add/',views.Order_Add),
    path('Order-update/<int:pk>/',views.Order_Update), #order_id
    # path('Order-delete/<int:pk>/',views.Order_Delete),

    ## BASE INFO ##
    path('Base_info/<str:pk>/',views.Base_info),

    ## SEARCH ##
    #path('Search/<pk>/', views.Search),
    path(uri_to_iri('Search/<pk>'), views.Search),

    ## PRODUCT FAVORITE ##
    path('fav-view/<int:pk>/',views.PrFav_Get),
    path('fav-add/',views.PrFav_Add),
    path('fav-delete/<int:pk_u>/<int:pk_p>/',views.PrFav_Delete),

    ## DiSCOUNTS ##
    path('discount_get/<str:dis_code>/<int:pk>/',views.Discount_Get),

    # path('send/', views.send),

]