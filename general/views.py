from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import CompanyBranch
from .serializer import *

# Create your views here.

class BranchAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = CompanyBranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data
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
        instance = CompanyBranch.objects.filter(is_deleted=False)
        serializer = CompanyBranchSerializer(instance, many=True, context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def put(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()        
        if 'image' not in data or data['image'] == "":
            data['image'] = instance.image
        serializer = CompanyBranchSerializer(instance, data=data)
        
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
                "message": "Branch Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_object(self, pk):
        try:
            return CompanyBranch.objects.filter(pk=pk,is_deleted=False).first()
        except CompanyBranch.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)

# This function determines which branches are displayed on the user's frontend
class BranchSelectionAPIView(APIView):
    permission_classes = (IsAdminUser,)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        if instance is None:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)

        serializer = CompanyBranchSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def get_object(self, pk):
        try:
            return CompanyBranch.objects.get(pk=pk, is_deleted=False)
        except CompanyBranch.DoesNotExist:
            return None


class CompanyBranchDropdownListView(APIView):
    def get(self,request):
        instance = CompanyBranch.objects.filter(is_deleted=False)
        serializer = CompanyBranchDropDownSerializer(instance, many=True)
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    

class KeyHandOverAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = KeyHandoverSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data
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
        instance = KeyHandOver.objects.filter(is_deleted=False)
        serializer = KeyHandoverSeralizer(instance, many=True, context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()        
        if 'image' not in data or data['image'] == "":
            data['image'] = instance.image
        serializer = KeyHandoverSeralizer(instance, data=data)
        
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
                "message": "Key handover Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return KeyHandOver.objects.filter(id=id,is_deleted=False).first()
        except KeyHandOver.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class TestimonialsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = TestimonialsSaveSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "New Testimonieal Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors,
            "message" : ""

            }
            return Response(response_data, status=status.HTTP_200_OK)
           
    def get(self, request):
        instance = Testimonials.objects.filter(is_deleted=False)
        serializer = TestimonialsSeralizer(instance, many=True, context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()        
        if 'image' not in data or data['image'] == "":
            data['image'] = instance.image
        serializer = TestimonialsSaveSeralizer(instance, data=data)
        
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
                "message": "Key handover Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return Testimonials.objects.filter(id=id,is_deleted=False).first()
        except Testimonials.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class BlogsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = BlogsSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "New Blogs Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors,
            "message" : ""

            }
            return Response(response_data, status=status.HTTP_200_OK)
           
    def get(self, request):
        instance = Blogs.objects.filter(is_deleted=False)
        serializer = BlogsSeralizer(instance, many=True, context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()        
        if 'image' not in data or data['image'] == "":
            data['image'] = instance.image
        serializer = BlogsSeralizer(instance, data=data)
        
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message" : "Blog Updated !"
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
                "message": "Blog Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return Blogs.objects.filter(id=id,is_deleted=False).first()
        except Blogs.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
class NewsAndEventsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = NewsAndEventsSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "New News Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors,
            "message" : ""

            }
            return Response(response_data, status=status.HTTP_200_OK)
           
    def get(self, request):
        instance = NewAndEvents.objects.filter(is_deleted=False)
        serializer = NewsAndEventsSeralizer(instance, many=True, context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()        
        if 'image' not in data or data['image'] == "":
            data['image'] = instance.image
        serializer = NewsAndEventsSeralizer(instance, data=data)
        
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message" : "News & Events Updated !"
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
                "message": "News & Events Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return NewAndEvents.objects.filter(id=id,is_deleted=False).first()
        except NewAndEvents.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class SeoAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = SeoSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Seo Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors,
            "message" : "error"

            }
            return Response(response_data, status=status.HTTP_200_OK)
           
    def get(self, request):
        instance = SEO.objects.filter(is_deleted=False)
        serializer = SeoSeralizer(instance, many=True)
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = SeoSeralizer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message" : "Seo Updated !"
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
                "message": "Seo Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return SEO.objects.filter(id=id,is_deleted=False).first()
        except SEO.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
class ProjectCoutsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = ProjectCountsSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Project Cuont added Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors,
            "message" : "error"

            }
            return Response(response_data, status=status.HTTP_200_OK)
    def get(self, request):
        instance = ProjectCounts.objects.all()
        serializer = ProjectCountsSeralizer(instance, many=True)
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = ProjectCountsSeralizer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message" : "Project Count's Updated !"
            }
        else:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "data": serializer.errors
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return ProjectCounts.objects.filter(id=id).first()
        except ProjectCounts.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class AwardsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = AwardsImagesSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Image Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors,
            "message" : "error"

            }
            return Response(response_data, status=status.HTTP_200_OK)
    def get(self, request):
        instance = AwardsImages.objects.filter(is_deleted=False)
        serializer = AwardsImagesSeralizer(instance, many=True,context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = AwardsImagesSeralizer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message" : "Image Updated !"
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
                "message": "image Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return AwardsImages.objects.filter(id=id).first()
        except AwardsImages.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class HomePageVideoAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = HomePageVideoImagesSeralizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Video Added !"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors,
            "message" : "error"

            }
            return Response(response_data, status=status.HTTP_200_OK)
    def get(self, request):
        instance = HomePageVideos.objects.all()
        serializer = HomePageVideoImagesSeralizer(instance, many=True,context={'request': request})
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        # data = request.data.copy()        
        # if 'desktop_video' not in data or data['desktop_video'] == "":
        #     data['desktop_video'] = instance.desktop_video
        # if 'desktop_video' not in data or data['desktop_video'] == "":
        #     data['desktop_video'] = instance.desktop_video
        serializer = HomePageVideoImagesSeralizer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message" : "Video Updated !"
            }
        else:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "data": serializer.errors
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return HomePageVideos.objects.filter(id=id).first()
        except HomePageVideos.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)