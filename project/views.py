from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import ProjectAmenities
from .serializer import *
# Create your views here.

class AmenitiesAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = AmenitiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Amenities Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_200_OK)
           
    def get(self, request):
        instance = ProjectAmenities.objects.filter(is_deleted=False)
        serializer = AmenitiesSerializer(instance, many=True, context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()        
        serializer = AmenitiesSerializer(instance, data=data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data
            }
        else:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "data": serializer.errors
            }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def delete(self, request, id):
        instance = self.get_object(id)
        instance.is_deleted = True 
        instance.save()
        response_data={
                "StatusCode":6000,
                "detail" : "error",
                "data" : "",
                "message": f"{instance.title} Amenities Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            return ProjectAmenities.objects.filter(pk=pk,is_deleted=False).first()
        except ProjectAmenities.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)



class ProjectApiView(APIView):
      # permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Project Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_200_OK)
    def get(self, request,slug=None):
        if slug:
            instance = self.get_object(slug)
            if instance is not None:
                serializer = ProjectSerializer(instance, context={'request': request})
                response_data={
                    "StatusCode":6000,
                    "detail" : "Success",
                    "data": serializer.data
                    }
                return Response(response_data,status=status.HTTP_200_OK)
            else:
                response_data={
                    "StatusCode":6002,
                    "detail" : "error",
                    "message": 'Slug Not Found'
                    }
                return Response(response_data,status=status.HTTP_200_OK)
        else:
            instance = Project.objects.filter(is_deleted=False)
            serializer = ProjectSerializer(instance, many=True, context={'request': request})
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data
                }
            return Response(response_data,status=status.HTTP_200_OK)
        
    def patch(self, request, slug):
        instance = self.get_object(slug)
        data = request.data.copy()
        if 'qr_code' not in data or data['qr_code'] == "":
            data['qr_code'] = instance.qr_code
        if 'thumbnail' not in data or data['thumbnail'] == "":
            data['thumbnail'] = instance.thumbnail
        serializer = ProjectSerializer(instance, data=data,partial=True,context={'request': request})

        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": f'{instance.name} is Updated !'
            }
        else:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "data": serializer.errors
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, slug):
        try:
            return Project.objects.filter(slug=slug,is_deleted=False).first()
        except Project.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "slug Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)