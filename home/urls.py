from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from home import views as home_views

urlpatterns = [
    path('categories/',views.home_view,name = "smart-phone"),
    path('categories/<int:cid>/products',views.view_products_by_category,name = "products"), 
    path('searchproducts/',views.category_search,name = "search_products"),
    path('products/<int:pid>/reviews/', views.reviews, name='product_reviews'),
    path('products/<int:pid>/details/', views.details, name='product_details'),
    path('products/<int:product_id>/add-to-cart/', home_views.add_to_cart, name='add_to_cart'),
    path('cart/', home_views.cart_view, name = 'viewcart'),
    path('remove-from-cart/<int:product_id>', home_views.remove_from_cart, name = 'removefromcart'),
    path('checkout/',home_views.checkout, name = 'checkout'),
    path('orders/',home_views.number_of_orders,name = 'number_of_orders'),
    path('orders/<int:oid>/',home_views.view_orders,name = 'orders')
    # path('categories/<int:cid>/products.search_result, name='search_result')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)