from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.home_view,name = "smart-phone"),
    path('product/<int:pid>/reviews/', views.reviews, name='product_reviews'),
    path('product/<int:pid>/details/', views.details, name='product_details')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)