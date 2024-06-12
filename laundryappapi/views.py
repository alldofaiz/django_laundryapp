from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Laundry
from .serializers import LaundrySerializer

class LaundryViewSet(viewsets.ModelViewSet):
    queryset = Laundry.objects.all()
    serializer_class = LaundrySerializer

@api_view(['POST'])
def add_laundry(request):
    if request.method == 'POST':
        serializer = LaundrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_laundry_status(request, pk):
    try:
        laundry = Laundry.objects.get(pk=pk)
    except Laundry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = request.data
        serializer = LaundrySerializer(laundry, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_laundry(request, pk):
    try:
        laundry = Laundry.objects.get(pk=pk)
    except Laundry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        laundry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
