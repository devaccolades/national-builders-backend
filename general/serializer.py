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

class TestimoniealsSaveSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Testimonieals
        fields = ['id','image','name','project','description']

class TestimoniealsSeralizer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    class Meta:
        model = Testimonieals
        fields = ['id', 'image','name','project','description']

    def get_project(self, obj):
        from project.serializer import ProjectListSerializer 
        serializer = ProjectListSerializer(obj.project)
        return serializer.data
    
class BlogsSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ['id','image','title','body','image_alt','meta_tag','meta_description','slug']

class NewsAndEventsSeralizer(serializers.ModelSerializer):
    class Meta:
        model = NewAndEvents
        fields = ['id','image','title','body','youtube_link','image_alt','meta_tag','meta_description','slug']