# laundryappapi/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LaundryViewSet, add_laundry, update_laundry_status, delete_laundry

router = DefaultRouter()
router.register(r'laundry', LaundryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/laundry/', add_laundry, name='add_laundry'),
    path('api/laundry/<int:pk>/', update_laundry_status, name='update_laundry_status'),
    path('api/laundry/<int:pk>/', delete_laundry, name='delete_laundry'),
]
