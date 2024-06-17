from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, add_order, update_order_status, delete_order

# Router for viewset
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),  # Includes all CRUD operations for the OrderViewSet
    path('add_order/', add_order, name='add_order'),  # Endpoint for adding orders
    path('orders/<int:pk>/update_status/', update_order_status, name='update_order_status'),  # Endpoint for updating order status
    path('orders/<int:pk>/delete/', delete_order, name='delete_order'),  # Endpoint for deleting orders
]