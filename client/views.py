from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from general import models as general_model
from general import serializer as general_serializer
from project import models as project_models
from project import serializer as project_serializer
from . import serializer as client_serialzer

class DataAPIView(APIView):
    def get_project_counts(self):
        try:
            instances = general_model.ProjectCounts.objects.all()
            serializer = general_serializer.ProjectCountsSeralizer(instances, many=True)
            return serializer.data, None
        except Exception as e:
            return None, f"Failed to fetch Project Count Data: {str(e)}"

    def get_awards(self):
        try:
            instances = general_model.AwardsImages.objects.all()
            serializer = general_serializer.AwardsImagesSeralizer(instances, many=True, context={'request': self.request})
            return serializer.data, None
        except Exception as e:
            return None, f"Failed to fetch Awards Data: {str(e)}"

    def get_home_page_videos(self):
        try:
            instances = general_model.HomePageVideos.objects.all()
            serializer = general_serializer.HomePageVideoImagesSeralizer(instances, many=True, context={'request': self.request})
            return serializer.data, None
        except Exception as e:
            return None, f"Failed to fetch Home Page videos Data: {str(e)}"

    def get(self, request):
        project_counts_data, project_counts_error = self.get_project_counts()
        awards_data, awards_error = self.get_awards()
        home_page_videos_data, home_page_videos_error = self.get_home_page_videos()

        response_data = {}

        if project_counts_data is not None:
            response_data['project_counts'] = project_counts_data
        else:
            response_data['project_counts_error'] = project_counts_error

        if awards_data is not None:
            response_data['awards'] = awards_data
        else:
            response_data['awards_error'] = awards_error

        if home_page_videos_data is not None:
            response_data['home_page_videos'] = home_page_videos_data
        else:
            response_data['home_page_videos_error'] = home_page_videos_error

        response={
        "StatusCode":6000 if all(data is not None for data in [project_counts_data, awards_data, home_page_videos_data]) else 6002,
        "detail" : "Success",
        "data": response_data,
        "message" : "feching datas !"
        }
        return Response(response, status=status.HTTP_200_OK)

class TestimonialsAPIView(APIView):
    def get (self,request):
        try:
            instances = general_model.Testimonials.objects.all()
            serializer = client_serialzer.TestimonialsSeralizer(instances, many=True,context={'request': self.request})
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message": "Testimonials Data fetched successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data" : "",
                "message": f"Failed to fetch Testimonials Data: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_200_OK)


class BlogsAPIView(APIView):
    def get (self,request):
        try:
            instances = general_model.Blogs.objects.all()
            serializer = general_serializer.BlogsSeralizer(instances, many=True,context={'request': self.request})
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message": "Blogs Data fetched successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data" : "",
                "message": f"Failed to fetch Blogs Data: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_200_OK)


class ProjectsAPIView(APIView):
    def get (self,request):
        try:
            instances = project_models.Project.objects.all()
            serializer = project_serializer.ProjectSerializer(instances, many=True,context={'request': self.request})
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message": "Project's Data fetched successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data" : "",
                "message": f"Failed to fetch Project's Data: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_200_OK)
