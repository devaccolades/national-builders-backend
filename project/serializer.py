from rest_framework import serializers
from .models import *
from general.serializer import CompanyBranchDropDownSerializer
from django.shortcuts import get_object_or_404

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
    
class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Project
        fields = ['id','name', 'thumbnail', 'description', 'rera_number', 'qr_code', 'location', 'company_branch', 'type', 'status', 'units', 'bedrooms', 'area_from', 'area_to', 'iframe', 'meta_title', 'meta_description', 'slug','amenities']

class ProjectDropDownListSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Project
        fields = ['id','name']

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImages
        fields = ['id','project','images']

class ProjectImageSaveSerializer(serializers.Serializer):
    project = serializers.CharField() 
    images = serializers.ListField(child=serializers.ImageField())

    def create(self, validated_data):
        project_id = validated_data['project']
        images = validated_data['images']
        project_instance = get_object_or_404(Project, id=project_id)
        for image in images:
            ProjectImages.objects.create(project=project_instance, images=image)
        
        return validated_data
        

class FloorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlanImages
        fields = ['id','project','images','title']

class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSpecification
        fields = ['id','project','title','description']

class DistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDistance
        fields = ['id','project','location_name','distance','measurement_unit']

class RentalsSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rentals
        fields = ['name','image','company_branch','type','area','price']

class RentalsSerializer(serializers.ModelSerializer):
    company_branch = CompanyBranchDropDownSerializer()
    class Meta:
        model = Rentals
        fields = ['id','name','image','company_branch','type','area','price','is_hide']


class EnquirySerializer(serializers.ModelSerializer):
    project = ProjectDropDownListSerializer()
    enquiry_date = serializers.SerializerMethodField()

    class Meta:
        model = Enquiry
        fields = ['id', 'name', 'email', 'project', 'phone', 'message', 'is_read', 'enquiry_date',]

    def get_enquiry_date(self, obj):  
        return obj.enquiry_date.strftime("%Y-%m-%d %H:%M") 
    

class EnquiryDownloadSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    enquiry_date = serializers.SerializerMethodField()

    class Meta:
        model = Enquiry
        fields = ['name', 'email','phone','message', 'project','enquiry_date' ]

    def get_enquiry_date(self, obj):  
        return obj.enquiry_date.strftime("%Y-%m-%d %H:%M") 
    
    def get_project(self, obj):  
        return obj.project.name