from rest_framework import serializers
from .models import *
class CompanyBranchSerializer(serializers.ModelSerializer):
    class Meta:  
        model = CompanyBranch
        fields = ['id', 'location','image','image_alt','iframe','address','email','phone_number','show_user_side']

class CompanyBranchSaveSerializer(serializers.ModelSerializer):
    class Meta:  
        model = CompanyBranch
        fields = ['id', 'location','image','image_alt','iframe','address','email','phone_number']
        

class CompanyBranchDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBranch
        fields = ['id', 'location']

class KeyHandoverSeralizer(serializers.ModelSerializer):
    class Meta:
        model = KeyHandOver
        fields = ['id', 'image','name','image_alt']

class TestimonialsSaveSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = ['id','image','name','project','description','image_alt']

class TestimonialsSeralizer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    class Meta:
        model = Testimonials
        fields = ['id', 'image','name','project','description','image_alt']

    def get_project(self, obj):
        from project.serializer import ProjectListSerializer 
        serializer = ProjectListSerializer(obj.project)
        return serializer.data
    
class BlogsSeralizer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()
    class Meta:
        model = Blogs
        fields = ['id','image','title','body','image_alt','meta_tag','meta_description','slug','date_added']

    def get_date_added(self, obj):  
        return obj.date_added.strftime("%B %d, %Y") if obj.date_added else None

class NewsAndEventsSeralizer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()
    class Meta:
        model = NewAndEvents
        fields = ['id','image','title','body','youtube_link','image_alt','meta_tag','meta_description','slug','date_added']

    def get_date_added(self, obj):  
        return obj.date_added.strftime("%B %d, %Y") if obj.date_added else None

class SeoSeralizer(serializers.ModelSerializer):
    class Meta:
        model = SEO
        fields = ['id','page','path','meta_title','meta_description']

class ProjectCountsSeralizer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCounts
        fields = ['id','launched','projectcompleted','readytooccupy','ongoing']

class AwardsImagesSeralizer(serializers.ModelSerializer):
    class Meta:
        model = AwardsImages
        fields = ['id','images','order','image_alt']


class HomePageVideoImagesSeralizer(serializers.ModelSerializer):
    class Meta:
        model = HomePageVideos
        fields = ['id','desktop_video','mobile_video']
