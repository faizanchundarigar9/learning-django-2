from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('view/',views.view_wishlist,name = 'view_wishlist'),
    path('remove/<int:wishlist_item_id>/',views.remove_product_from_wishlist,name = 'remove_from_wishlist'),
    path('add/',views.add_to_wishlist,name = 'add_to_wishlist')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)