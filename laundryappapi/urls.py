from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet, 
    get_all_users, 
    get_user, 
    register_user, 
    delete_user, 
    update_user, 
    add_order, 
    update_order_status, 
    delete_order, 
    create_laundry_store, 
    delete_laundry_store, 
    update_laundry_store, 
    get_all_laundry_stores, 
    get_laundry_store
)

# Registering OrderViewSet with DefaultRouter
router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Users
    path('users/', include([
        path('get_all/', get_all_users, name='get_all_users'),
        path('get/<uuid:pk>/', get_user, name='get_user'),
        path('register/', register_user, name='register_user'),
        path('delete/<uuid:pk>/', delete_user, name='delete_user'),
        path('update/<uuid:pk>/', update_user, name='update_user'),
    ])),

    # Orders
    path('orders/', include([
        path('add/', add_order, name='add_order'),
        path('update/<uuid:pk>/', update_order_status, name='update_order_status'),
        path('delete/<uuid:pk>/', delete_order, name='delete_order'),
    ])),

    # Laundry Stores
    path('laundrystores/', include([
        path('get_all/', get_all_laundry_stores, name='get_all_laundry_stores'),
        path('get/<uuid:pk>/', get_laundry_store, name='get_laundry_store'),
        path('create/', create_laundry_store, name='create_laundry_store'),
        path('update/<uuid:pk>/', update_laundry_store, name='update_laundry_store'),
        path('delete/<uuid:pk>/', delete_laundry_store, name='delete_laundry_store'),
    ])),
]
