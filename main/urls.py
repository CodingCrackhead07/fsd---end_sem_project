from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('your_listings/', views.your_listings, name='your_listings'),
    path('car_details/<int:car_id>/', views.car_details, name='car_details'),  # This is the car_details URL
    path('add_car/', views.add_car, name='add_car'),
    path('delete_car/<int:id>/', views.delete_car, name='delete_car'),
    path('add_to_wishlist/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.your_wishlist, name='your_wishlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
