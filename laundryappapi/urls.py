# laundryappapi/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LaundryViewSet

router = DefaultRouter()
router.register(r'laundry', LaundryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
