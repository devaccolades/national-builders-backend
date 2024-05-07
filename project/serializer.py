from rest_framework import serializers
from .models import *

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:  
        model = ProjectAmenities
        fields = ['id','logo','title']
    def get_logo(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Project
        fields = ['name', 'thumbnail', 'description', 'rera_number', 'qr_code', 'location', 'company_branch', 'type', 'status', 'units', 'bedrooms', 'area_from', 'area_to', 'iframe', 'meta_title', 'meta_description', 'slug']

    def clean_amenities(self):
        amenities = self.cleaned_data.get('amenities')
        if not amenities: 
            return []
        return amenities

        