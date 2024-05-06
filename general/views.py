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