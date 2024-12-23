from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from home import views as home_views

urlpatterns = [
    path('categories/',views.home_view,name = "smart-phone"),
    path('categories/<int:cid>/products',views.view_products_by_category,name = "products"), 
    path('products/<int:pid>/reviews/', views.reviews, name='product_reviews'),
    path('products/<int:pid>/details/', views.details, name='product_details'),
    # path('categories/<int:cid>/products.search_result, name='search_result')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)