from rest_framework import serializers
from .models import *
from general.serializer import CompanyBranchDropDownSerializer
from django.shortcuts import get_object_or_404

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:  
        model = ProjectAmenities
        fields = ['id','logo','title','image_alt']
    def get_logo(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Project
        fields = ['name', 'thumbnail','thumbnail_alt', 'description', 'rera_number', 'qr_code','qr_code_alt', 'location', 'company_branch', 'type', 'status', 'units', 'bedrooms', 'area_from', 'area_to', 'iframe', 'meta_title', 'meta_description', 'slug','logo','brochure']

    def clean_amenities(self):
        amenities = self.cleaned_data.get('amenities')
        if not amenities: 
            return []
        return amenities
    
class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Project
        fields = ['id','name', 'thumbnail','thumbnail_alt', 'description', 'rera_number', 'qr_code','qr_code_alt', 'location', 'company_branch', 'type', 'status', 'units', 'bedrooms', 'area_from', 'area_to', 'iframe', 'meta_title', 'meta_description', 'slug','amenities','logo','brochure']

class ProjectDropDownListSerializer(serializers.ModelSerializer):
    class Meta:  
        model = Project
        fields = ['id','name']

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImages
        fields = ['id','project','images','image_alt']
        

class FloorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlanImages
        fields = ['id','project','images','title','image_alt']

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
        fields = ['name','image','company_branch','type','area','price','image_alt']

class RentalsSerializer(serializers.ModelSerializer):
    company_branch = CompanyBranchDropDownSerializer()
    class Meta:
        model = Rentals
        fields = ['id','name','image','company_branch','type','area','price','is_hide','image_alt']


class EnquirySerializer(serializers.ModelSerializer):
    project = ProjectDropDownListSerializer()
    enquiry_date = serializers.SerializerMethodField()

    class Meta:
        model = Enquiry
        fields = ['id', 'first_name','last_name', 'email', 'project', 'phone', 'message', 'is_read', 'enquiry_date',]

    def get_enquiry_date(self, obj):  
        return obj.enquiry_date.strftime("%Y-%m-%d %H:%M") 
    

class EnquiryDownloadSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    enquiry_date = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Enquiry
        fields = ['name', 'email','phone','message', 'project','enquiry_date' ]

    def get_enquiry_date(self, obj):  
        return obj.enquiry_date.strftime("%Y-%m-%d %H:%M") 
    
    def get_project(self, obj):  
        if obj.project:
            return obj.project.name
        else:
            return ''
    def get_name(self, obj):
        name = ''
        if obj.first_name:
            name += obj.first_name
        if obj.last_name:
            if name: 
                name += ' '
            name += obj.last_name
        return name


    
class RentalEnquirySerializer(serializers.ModelSerializer):
    rentals = ProjectDropDownListSerializer()
    enquiry_date = serializers.SerializerMethodField()

    class Meta:
        model = RentalEnquiry
        fields = ['id', 'first_name','last_name', 'email', 'rentals', 'phone', 'message', 'is_read', 'enquiry_date',]

    def get_enquiry_date(self, obj):  
        return obj.enquiry_date.strftime("%Y-%m-%d %H:%M") 
    

class RentalEnquiryDownloadSerializer(serializers.ModelSerializer):
    rentals = serializers.SerializerMethodField()
    enquiry_date = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Enquiry
        fields = ['name', 'email','phone','message', 'rentals','enquiry_date' ]

    def get_enquiry_date(self, obj):  
        return obj.enquiry_date.strftime("%Y-%m-%d %H:%M") 
    
    def get_rentals(self, obj):  
        if obj.rentals:
            return obj.rentals.name
        else:
            return ''
    def get_name(self, obj):
        name = ''
        if obj.first_name:
            name += obj.first_name
        if obj.last_name:
            if name: 
                name += ' '
            name += obj.last_name
        return name


class CurrentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentStatus
        fields = ['id','project', 'year', 'month', 'image', 'image_alt']