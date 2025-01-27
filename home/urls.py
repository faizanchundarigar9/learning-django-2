from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from home import views as home_views
from home.views import(
    CategoryOperations, 
    ProductByCategory, 
    ProductDetail, 
    CartView, 
    ViewOrders, 
    ViewOrderDetails,
    ProductViewSet)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"products",ProductViewSet,basename = "products")

urlpatterns = [
    path('',include(router.urls),name = "products"),
    path('categories/',views.home_view,name = "smart-phone"),
    path('categories/<int:cid>/products',views.view_products_by_category,name = "products"), 
    path('searchproducts/',views.category_search,name = "search_products"),
    path('products/<int:pid>/details/', views.details, name='product_details'),
    path('products/<int:product_id>/add-to-cart/', home_views.add_to_cart, name='add_to_cart'),
    path('quantitycounter/<int:cpid>/',home_views.quantity_counter, name = "quantity_counter"),
    path('cart/', home_views.cart_view, name = 'viewcart'),
    path('remove-from-cart/<int:product_id>', home_views.remove_from_cart, name = 'removefromcart'),
    path('checkout/',home_views.checkout, name = 'checkout'),
    path('orders/',home_views.number_of_orders,name = 'number_of_orders'),
    path('orders/<int:oid>/',home_views.view_orders,name = 'orders'),
    path('wishlist/',include('wishlist.urls'),name = 'view_wishlist'),
    path('wishlist/<int:pid>/',include('wishlist.urls'),name = 'add_to_wishlist'),
    path('profile/',views.view_profile,name = "view_profile"),
    path('api/category/',CategoryOperations.as_view(),name="categoryapi"),
    path('api/categories/<int:cid>/products/',ProductByCategory.as_view(),name="product by category api"),
    path('api/products/<int:pid>/details/', ProductDetail.as_view(), name='product details by api'),
    path('api/cart/', CartView.as_view(), name = 'view cart by api'),
    path('api/orders/<int:oid>/',ViewOrders.as_view(),name = 'orders by api'),
    path('api/orders/<int:oid>/details/',ViewOrderDetails.as_view(),name = 'order details by api')


    # path('categories/<int:cid>/products.search_result, name='search_result')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)