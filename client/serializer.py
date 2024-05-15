from rest_framework import serializers

from project import serializer as project_serializer
from general import serializer as general_serializer

class TestimonialsSeralizer(serializers.ModelSerializer):
    project = project_serializer.ProjectDropDownListSerializer()
    class Meta:
        model = general_serializer.Testimonials
        fields = ['id', 'image','name','project','description']

    def get_project(self, obj):
        from project.serializer import ProjectListSerializer 
        serializer = ProjectListSerializer(obj.project)
        return serializer.data
    
    # 