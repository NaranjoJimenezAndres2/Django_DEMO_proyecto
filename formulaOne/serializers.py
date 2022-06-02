from rest_framework import serializers
from .models import Comparacion


class ComparacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comparacion
        fields = ('id', 'title', 'content', 'created_at')
        
        
        
