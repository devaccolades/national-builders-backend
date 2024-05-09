from rest_framework import serializers
from .models import *

class CompanyBranchSerializer(serializers.ModelSerializer):
    class Meta:  
        model = CompanyBranch
        fields = '__all__'
    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
        
class CompanyBranchDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBranch
        fields = ['id', 'location']

class KeyHandoverSeralizer(serializers.ModelSerializer):
    class Meta:
        model = KeyHandOver
        fields = ['id', 'image','name']