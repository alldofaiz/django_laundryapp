from rest_framework import viewsets
from .models import Laundry
from .serializers import LaundrySerializer

class LaundryViewSet(viewsets.ModelViewSet):
    queryset = Laundry.objects.all()
    serializer_class = LaundrySerializer
