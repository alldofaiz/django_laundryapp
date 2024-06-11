# laundry/serializers.py
from rest_framework import serializers
from .models import Laundry

class LaundrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laundry
        fields = '__all__'
