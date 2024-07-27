from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import ProjectAmenities
from .serializer import *
import csv
from django.http import HttpResponse


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
    permission_classes = (IsAdminUser,)
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
                serializer = ProjectListSerializer(instance, context={'request': request})
                response_data={
                    "StatusCode":6000,
                    "detail" : "Success",
                    "data": serializer.data,
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
            serializer = ProjectListSerializer(instance, many=True, context={'request': request})
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
        if 'logo' not in data or data['logo'] == "":
            data['logo'] = instance.logo if instance.logo else None
            
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
    
    def delete(self, request, id):
        instance = self.get_object_id(id)
        instance.is_deleted = True 
        instance.save()
        response_data={
                "StatusCode":6000,
                "detail" : "error",
                "data" : "",
                "message": "Project Deleted !"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object_id(self, id):
        try:
            return Project.objects.filter(id=id,is_deleted=False).first()
        except Project.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "slug Not Found"
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
        

class ProjectCountAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self,request):
        instace_count  = Project.objects.filter(is_deleted=False).count()
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": instace_count,
            "message" : "success!"
            }
        return Response(response_data, status=status.HTTP_200_OK)


class ProjectImagesApiView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = ProjectImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Images added successfully!"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def get(self, request, projectId):
        try:
            instance = ProjectImages.objects.filter(project=projectId, is_deleted=False)
            serializer = ProjectImageSerializer(instance, many=True, context={'request': request})
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message" : "Success"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ProjectImages.DoesNotExist:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "message": "Project id Not Found",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()
        if 'images' not in data or data['images'] == "":
            data['images'] = instance.images
        serializer = ProjectImageSerializer(instance, data=data,partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Image is Updated !'
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
                "message": "Image Deleted Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_object(self, id):
        try:
            return ProjectImages.objects.filter(id=id,is_deleted=False).first()
        except ProjectImages.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
class FloorPlanImagesApiView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = FloorPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Images added successfully!"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_200_OK)
    def get(self, request, projectId):
        try:
            instance = FloorPlanImages.objects.filter(project=projectId, is_deleted=False)
            serializer = FloorPlanSerializer(instance, many=True, context={'request': request})
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message" : "Success"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ProjectImages.DoesNotExist:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "message": "Project id Not Found",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()
        if 'images' not in data or data['images'] == "":
            data['images'] = instance.images
        serializer = FloorPlanSerializer(instance, data=data,partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Image is Updated !'
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
                "message": "Image Deleted Deleted"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return FloorPlanImages.objects.filter(id=id,is_deleted=False).first()
        except FloorPlanImages.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class ProjectAmenitiesAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request, projectId):
        try:
            project = Project.objects.filter(id=projectId).first()
            amenities_ids = project.amenities.filter(is_deleted=False).values_list('id', flat=True)
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": amenities_ids,
                "message" : "Success"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ProjectImages.DoesNotExist:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "message": "Project id Not Found",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request, projectId):
        try:
            
            project = Project.objects.filter(id=projectId).first()
            amenities_ids = []
            for key,value in request.data.items():
                amenities_ids.append(value)
            amenities_to_add = ProjectAmenities.objects.filter(id__in=amenities_ids)
            project.amenities.clear() 
            project.amenities.add(*amenities_to_add)
            amenities = project.amenities.filter(is_deleted=False).values_list('id',flat=True)

            print()
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": list(amenities),
                "message" : "Success"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ProjectImages.DoesNotExist:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "message": "Project id Not Found",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class SpecificationsApiView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = SpecificationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Specifications added successfully!"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def get(self, request, projectId):
        try:
            instance = ProjectSpecification.objects.filter(project=projectId, is_deleted=False)
            serializer = SpecificationsSerializer(instance, many=True)
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message" : "Success"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ProjectImages.DoesNotExist:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "message": "Project id Not Found",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = SpecificationsSerializer(instance, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Specification is Updated !'
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
                "message": "Specification Deleted !"
            }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def get_object(self, id):
        try:
            return ProjectSpecification.objects.filter(id=id,is_deleted=False).first()
        except ProjectSpecification.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)

    

class DistanceApiView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = DistanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Near By added successfully!"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data={
            "StatusCode":6002,
            "detail" : "error",
            "data": serializer.errors
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

    def get(self, request, projectId):
        try:
            instance = ProjectDistance.objects.filter(project=projectId, is_deleted=False)
            serializer = DistanceSerializer(instance, many=True)
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message" : "Success"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ProjectImages.DoesNotExist:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "message": "Project id Not Found",
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = DistanceSerializer(instance, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Near By is Updated !'
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
                "message": "Near By Deleted !"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return ProjectDistance.objects.filter(id=id,is_deleted=False).first()
        except ProjectDistance.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        

class RentalsAPIView(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):
        serializer = RentalsSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data={
            "StatusCode":6001,
            "detail" : "Success",
            "data": serializer.data,
            "message" : "Rentals added !"
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
        instance = Rentals.objects.filter(is_deleted=False)
        serializer = RentalsSerializer(instance, many=True,context={'request': request})
        response_data = {
            "StatusCode": 6000,
            "detail": "Success",
            "data": serializer.data,
            "message" : "Success"
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        instance = self.get_object(id)
        data = request.data.copy()
        if 'image' not in data or data['image'] == "":
            data['image'] = instance.image
        serializer = RentalsSerializer(instance, data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Rentals Updated !'
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
                "message": "Rentals Deleted !"
            }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def get_object(self, id):
        try:
            return Rentals.objects.filter(id=id,is_deleted=False).first()
        except Rentals.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
class RentalsUpdateAPIView(APIView):
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = RentalsSaveSerializer(instance, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Rentals Updated !'
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
            return Rentals.objects.filter(id=id,is_deleted=False).first()
        except Rentals.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
class ProjectDropDownList(APIView):
    # permission_classes = (IsAdminUser,)
    def get(self,request):
        instance = Project.objects.filter(is_deleted=False)
        serializer = ProjectDropDownListSerializer(instance, many=True)
        response_data={
            "StatusCode":6000,
            "detail" : "Success",
            "data": serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)

class EnquiryAPIView(APIView):
    permission_classes = (IsAdminUser,)
    
    def get(self, request):
        instance = Enquiry.objects.filter(is_deleted=False)
        serializer = EnquirySerializer(instance, many=True)
        response_data = {
            "StatusCode": 6000,
            "detail": "Success",
            "data": serializer.data,
            "message" : "Success"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = EnquirySerializer(instance, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Enqury Read !'
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
            return Enquiry.objects.filter(id=id,is_deleted=False).first()
        except Enquiry.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        
class EnquiryDownloadAPIView(APIView):
    # permission_classes = (IsAdminUser,)
    def get(self, request):
        try:
            instance = Enquiry.objects.filter(is_deleted=False)
            serializer = EnquiryDownloadSerializer(instance,many=True)
            response = HttpResponse(
            content_type='text/csv',
            )
            response['Content-Disposition'] = 'attachment; filename="EnquiryData.csv"'

            writer = csv.writer(response)
            writer.writerow(['Name', 'Email', 'Phone', 'Message','Project Name','Enquiry_date'])
            for enquiry in serializer.data:
                name = enquiry.get('name', '')
                email = enquiry.get('email', '')
                phone = enquiry.get('phone', '')
                message = enquiry.get('message', '')
                project_name = enquiry.get('project', '')
                enquiry_date = enquiry.get('enquiry_date', '')

                writer.writerow([name, email, phone, message, project_name, enquiry_date])

            return response
        except Exception as e:
            print(e)
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                 "message": "Something went wrong"
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RentalEnquiryAPIView(APIView):
    permission_classes = (IsAdminUser,)
    
    def get(self, request):
        instance = RentalEnquiry.objects.filter(is_deleted=False)
        serializer = RentalEnquirySerializer(instance, many=True)
        response_data = {
            "StatusCode": 6000,
            "detail": "Success",
            "data": serializer.data,
            "message" : "Success"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        instance = self.get_object(id)
        serializer = RentalEnquirySerializer(instance, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data={
                "StatusCode":6000,
                "detail" : "Success",
                "data": serializer.data,
                "message": 'Rentals Enqury Read !'
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
            return RentalEnquiry.objects.filter(id=id,is_deleted=False).first()
        except RentalEnquiry.DoesNotExist:
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                "message": "id Not Found"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        


class RentalsEnquiryDownloadAPIView(APIView):
    # permission_classes = (IsAdminUser,)
    def get(self, request):
        try:
            instance = RentalEnquiry.objects.filter(is_deleted=False)
            serializer = RentalEnquiryDownloadSerializer(instance,many=True)
            response = HttpResponse(
            content_type='text/csv',
            )
            response['Content-Disposition'] = 'attachment; filename="RentalsEnquiryData.csv"'

            writer = csv.writer(response)
            writer.writerow(['Name', 'Email', 'Phone', 'Message','Rentals Name','Enquiry_date'])
            for enquiry in serializer.data:
                name = enquiry.get('name', '')
                email = enquiry.get('email', '')
                phone = enquiry.get('phone', '')
                message = enquiry.get('message', '')
                rentals_name = enquiry.get('rentals', '')
                enquiry_date = enquiry.get('enquiry_date', '')

                writer.writerow([name, email, phone, message, rentals_name, enquiry_date])

            return response
        except Exception as e:
            print(e)
            response_data={
                "StatusCode":6002,
                "detail" : "error",
                 "message": "Something went wrong"
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
