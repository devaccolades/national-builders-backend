from rest_framework import serializers
from .models import ProjectAmenities

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:  
        model = ProjectAmenities
        fields = ['id','logo','title']
    def get_logo(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    
        