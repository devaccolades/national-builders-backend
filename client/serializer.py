from rest_framework import serializers

from project import models as project_models
from general import models as general_models

class TestimonialsSeralizer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    class Meta:
        model = general_models.Testimonials
        fields = ['id', 'image','name','project','description','image_alt']

    def get_project(self, obj):
        return obj.project.name

class CompanyBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = general_models.CompanyBranch
        fields = ['id','location'] 

class ProjectSerializer(serializers.ModelSerializer):
    company_branch = CompanyBranchSerializer()
    class Meta:  
        model = project_models.Project
        fields = ['id','name', 'thumbnail', 'thumbnail_alt','description', 'rera_number', 'qr_code','qr_code_alt', 'location', 'company_branch', 'type', 'status', 'units', 'bedrooms', 'area_from', 'area_to', 'iframe', 'meta_title', 'meta_description', 'slug','logo']

    def clean_amenities(self):
        amenities = self.cleaned_data.get('amenities')
        if not amenities: 
            return []
        return amenities
    

class RentalEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.RentalEnquiry
        fields = ['first_name','last_name', 'email', 'rentals', 'phone', 'message']


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Enquiry
        fields = ['first_name','last_name', 'email', 'phone', 'message','project']
