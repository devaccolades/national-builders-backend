from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.http import FileResponse, Http404

from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from general import models as general_model
from general import serializer as general_serializer
from project import models as project_models
from project import serializer as project_serializer
from . import serializer as client_serialzer
from general.views import CompanyBranchDropdownListView

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
            instances = general_model.AwardsImages.objects.filter(is_deleted=False)
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
        
    def get_home_page_blogs(self):
        try:
            instances = general_model.Blogs.objects.filter(is_deleted=False)[:6]
            serializer = general_serializer.BlogsSeralizer(instances, many=True, context={'request': self.request})
            return serializer.data, None
        except Exception as e:
            return None, f"Failed to fetch Home Page videos Data: {str(e)}"
        
    def get_home_page_testimonials(self):
        try:
            instances = general_model.Testimonials.objects.filter(is_deleted=False)[:6]
            serializer = client_serialzer.TestimonialsSeralizer(instances, many=True, context={'request': self.request})
            return serializer.data, None
        except Exception as e:
            return None, f"Failed to fetch Home Page videos Data: {str(e)}"

    def get(self, request):
        project_counts_data, project_counts_error = self.get_project_counts()
        awards_data, awards_error = self.get_awards()
        home_page_videos_data, home_page_videos_error = self.get_home_page_videos()
        home_page_blogs_data, home_page_blogs_error = self.get_home_page_blogs()
        home_page_testimonials_data, home_page_testimonials_error = self.get_home_page_testimonials()

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

        if home_page_blogs_data is not None:
            response_data['blogs'] = home_page_blogs_data
        else:
            response_data['blogs_error'] = home_page_blogs_error

        if home_page_testimonials_data is not None:
            response_data['testimonials'] = home_page_testimonials_data
        else:
            response_data['testimonials_error'] = home_page_testimonials_error

        response={
        "StatusCode":6000 if all(data is not None for data in [project_counts_data, awards_data, home_page_videos_data,home_page_blogs_data]) else 6002,
        "detail" : "Success",
        "data": response_data,
        "message" : "feching datas !"
        }
        return Response(response, status=status.HTTP_200_OK)


class ProjectsAPIView(APIView):
    def get(self, request, slug=None):
        """
        Get project data by slug or return all projects.
        """
        response_data = {}
        try:
            if slug:
                instance = project_models.Project.objects.filter(slug=slug, is_deleted=False).first()
            else:
                instance = project_models.Project.objects.filter(is_deleted=False)

            if not instance:
                response_data = {
                "StatusCode": 6002,
                "detail": "success",
                "data":"",
                "message": "id not found"
                }
                return Response(response_data,status=status.HTTP_200_OK)
            serializer = client_serialzer.ProjectSerializer(instance, many=not slug, context={'request': self.request})
            if slug:
                image_instance = project_models.ProjectImages.objects.filter(project=instance.id, is_deleted=False)
                image_serializer = project_serializer.ProjectImageSerializer(image_instance, many=True, context={'request': self.request})
                floor_instance = project_models.FloorPlanImages.objects.filter(project=instance.id, is_deleted=False)
                floor_serializer = project_serializer.FloorPlanSerializer(floor_instance, many=True, context={'request': self.request})
                amenities_instance = instance.amenities.all()
                amenities_serializer = project_serializer.AmenitiesSerializer(amenities_instance, many=True, context={'request': self.request})
                specification_instance = project_models.ProjectSpecification.objects.filter(project=instance.id, is_deleted=False)
                specification_serializer = project_serializer.SpecificationsSerializer(specification_instance, many=True)
                distance_instance = project_models.ProjectDistance.objects.filter(project=instance.id, is_deleted=False)
                distance_serializer = project_serializer.DistanceSerializer(distance_instance, many=True)

                status_instance = project_models.CurrentStatus.objects.filter(project=instance, is_deleted=False).order_by('-year', '-month')
                status_serializer = project_serializer.CurrentStatusSerializer(status_instance, many=True, context={'request': request})            
                month_order = {month: index for index, (month, _) in enumerate(project_models.Month_CHOICES)}

                grouped_data = defaultdict(list)
                for item in status_serializer.data:
                    year = item['year']
                    status_data = {
                        'id': item['id'],
                        'image': item['image'],
                        'image_alt': item['image_alt'],
                        'month': item['month'].capitalize()
                    }
                    grouped_data[year].append(status_data)  

                status_array = [
                    {"year": year, "statuses": sorted(statuses, key=lambda x: -month_order[x['month'].lower()])}
                    for year, statuses in sorted(grouped_data.items(), reverse=True)
                ]
                response_data={
                    "StatusCode": 6000,
                    "detail": "success",
                    "data": serializer.data,
                    "images": image_serializer.data,
                    "floor_images": floor_serializer.data,
                    "amenities": amenities_serializer.data,
                    "specification": specification_serializer.data,
                    "distance": distance_serializer.data,
                    "status": status_array,
                    "message": "Project's Data fetched successfully"

                }
            else:
                response_data = {
                    "StatusCode": 6000,
                    "detail": "success",
                    "data": serializer.data,
                    "message": "Project's Data fetched successfully"
                }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data":"",
                "message": f'Something went wrong {e}'
            }
            return Response(response_data,status=status.HTTP_200_OK)
        
"""
sned Brochure details for user side
"""
class BrochureDownloadView(APIView):
    def get(self, request, pk, format=None):
        try:
            project = project_models.Project.objects.get(pk=pk)
            if project.brochure:
                response = FileResponse(project.brochure, as_attachment=True, filename=project.brochure.name)
                return response
            else:
                return Response({"detail": "Brochure not found"}, status=404)
        except project_models.Project.DoesNotExist:
            raise Http404

class BranchDropDownAPIView(CompanyBranchDropdownListView):
    pass

class RentalsAPIView(APIView):
    def get(self, request):
        try:
            instance = project_models.Rentals.objects.filter(is_deleted=False,is_hide=False)
            serializer = project_serializer.RentalsSerializer(instance, many=True, context={'request': self.request})
            response_data = {
                    "StatusCode": 6000,
                    "detail": "success",
                    "data": serializer.data,
                    "message": "Rental's Data fetched successfully"
                }

        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data":"",
                "message": f'Something went wrong {e}'
            }
        return Response(response_data, status=status.HTTP_200_OK)
    


class RentalsEnquiryAPIView(APIView):
     def post(self, request):
        try:
            serializer = client_serialzer.RentalEnquirySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                context = {
                    'name': f"{serializer.validated_data['first_name']} {serializer.validated_data['last_name']}",
                    'email': serializer.validated_data['email'],
                    'phone': serializer.validated_data['phone'],
                    'message': serializer.validated_data['message'],
                    'rentals': serializer.validated_data['rentals']
                }

                template = get_template('rental_enquiry.html').render(context)
                e=settings.EMAIL_HOST_USER
                send_mail(
                    'Enquiry Data',
                    None, 
                    settings.EMAIL_HOST_USER,
                    ['smm@nationalbuilders.in'],
                    fail_silently=False,
                    html_message = template,
                    )
                response_data = {
                    "StatusCode": 6001,
                    "detail": "success",
                    "data": serializer.data,
                    "message": "Rental Enquiry successfully"
                }
            else:
                response_data = {
                    "StatusCode": 6002,
                    "detail": "validation error",
                    "data": serializer.errors,
                    "message": "Invalid data"
                }
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data":"",
                "message": f'Something went wrong {e}'
            }
        return Response(response_data, status=status.HTTP_200_OK)
     

class EnquiryAPIView(APIView):
     def post(self, request):
        try:
            serializer = client_serialzer.EnquirySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                context = {
                    'name': f"{serializer.validated_data['first_name']} {serializer.validated_data['last_name']}",
                    'email': serializer.validated_data['email'],
                    'phone': serializer.validated_data['phone'],
                    'message': serializer.validated_data['message'],
                    'project': serializer.validated_data['project'] if request.data.get('project') else None
                }
                template = get_template('enquiry.html').render(context)
                e=settings.EMAIL_HOST_USER
                send_mail(
                    'Enquiry Data',
                    None, 
                    settings.EMAIL_HOST_USER,
                    ['smm@nationalbuilders.in'],
                    fail_silently=False,
                    html_message = template,
                    )
                response_data = {
                    "StatusCode": 6001,
                    "detail": "success",
                    "data": serializer.data,
                    "message": "Enquiry successfully"
                }
            else:
                response_data = {
                    "StatusCode": 6002,
                    "detail": "validation error",
                    "data": serializer.errors,
                    "message": "Invalid data"
                }
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data":"",
                "message": f'Something went wrong {e}'
            }
        return Response(response_data, status=status.HTTP_200_OK)
     
        

class TestimonialsAPIView(APIView):
    def get(self, request):
        media_type = request.GET.get('media_type') 
        try:
            if media_type == 'image':
                start_limit = int(request.query_params.get('start_limit', 0))
                end_limit = int(request.query_params.get('end_limit', 3))
                instances = general_model.Testimonials.objects.filter(is_deleted=False, media_type='image')[start_limit:end_limit]
            elif media_type == 'video': 
                instances = general_model.Testimonials.objects.filter(is_deleted=False, media_type='video')
            else:
                return Response({"StatusCode": 6001, "detail": "Invalid media type"}, status=status.HTTP_400_BAD_REQUEST)
            
            total_count = general_model.Testimonials.objects.filter(is_deleted=False, media_type=media_type).count()
            serializer = client_serialzer.TestimonialsSeralizer(instances, many=True, context={'request': self.request})
            
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "total_count": total_count if media_type == 'image' else len(serializer.data),  # Return total count for images
                "message": "Testimonials Data fetched successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data": "",
                "message": f"Failed to fetch Testimonials Data: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_200_OK)



class BlogsAPIView(APIView):
    def get (self,request,slug=None):
        try:
            if slug:
                instances = general_model.Blogs.objects.filter(slug=slug,is_deleted=False).first()
                serializer = general_serializer.BlogsSeralizer(instances,context={'request': self.request})
                suggestion_instance = general_model.Blogs.objects.filter(is_deleted=False).exclude(id=instances.id).order_by('-date_added')[:3]
                suggestion_serializer = general_serializer.BlogsSeralizer(suggestion_instance,many=True,context={'request': self.request})
            else:
                start_limit = int(request.query_params.get('start_limit',0))
                end_limit = int(request.query_params.get('end_limit',7))
                instances = general_model.Blogs.objects.filter(is_deleted=False)[start_limit:end_limit]
                serializer = general_serializer.BlogsSeralizer(instances, many=True,context={'request': self.request})
                total_count = general_model.Blogs.objects.filter(is_deleted=False).count()
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "total_count": "" if slug else total_count,
                "suggestions" : suggestion_serializer.data if slug else "",
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


class NewsAndEventsAPIView(APIView):
    def get (self,request,slug=None):
        try:
            if slug:
                instances = general_model.NewAndEvents.objects.filter(slug=slug,is_deleted=False).first()
                serializer = general_serializer.NewsAndEventsSeralizer(instances,context={'request': self.request})
                suggestion_instance = general_model.NewAndEvents.objects.filter(is_deleted=False).exclude(id=instances.id).order_by('-date_added')[:3]
                suggestion_serializer = general_serializer.NewsAndEventsSeralizer(suggestion_instance,many=True,context={'request': self.request})
            else:
                start_limit = int(request.query_params.get('start_limit',0))
                end_limit = int(request.query_params.get('end_limit',7))
                instances = general_model.NewAndEvents.objects.filter(is_deleted=False)[start_limit:end_limit]
                serializer = general_serializer.NewsAndEventsSeralizer(instances, many=True,context={'request': self.request})
                total_count = general_model.NewAndEvents.objects.filter(is_deleted=False).count()
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "total_count": "" if slug else total_count,
                "suggestions" : suggestion_serializer.data if slug else "",
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


class KeyHandOverAPIView(APIView):
    def get(self, request):
        try:
            show_method = request.query_params.get('show_method', 'false').lower() == 'true'
            
            if show_method:
                instance = general_model.KeyHandOver.objects.filter(is_deleted=False)
                serializer = general_serializer.KeyHandoverSeralizer(instance,many=True, context={'request': self.request})
            else:
                start_limit = int(request.query_params.get('start_limit', 0))
                end_limit = int(request.query_params.get('end_limit', 7))
                instance = general_model.KeyHandOver.objects.filter(is_deleted=False)[start_limit:end_limit]
                serializer = general_serializer.KeyHandoverSeralizer(instance, many=True, context={'request': self.request})
                total_count = general_model.KeyHandOver.objects.filter(is_deleted=False).count()
            
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "total_count": "" if show_method else total_count,
                "message": "Key Hand Over Data fetched successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "data": "",
                "message": f"Failed to fetch Key Hand Over Data: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_200_OK)


class BranchAPIView(APIView):
    def get(self, request):
        try:
            instance = general_model.CompanyBranch.objects.filter(is_deleted=False,show_user_side=True)[:2]
            serializer = general_serializer.CompanyBranchSerializer(instance, many=True, context={'request': self.request})
            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message": "Key Hand Over Data fetched successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "data": "",
                "message": f"Failed to fetch Key Hand Over Data: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_200_OK)



class SeoAPIView(APIView):
    def get(self, request):
        try:
            path = str(request.query_params.get('path', '/'))
            instance = general_model.SEO.objects.filter(path=path,is_deleted=False).first()
            serializer = general_serializer.SeoSeralizer(instance)
            response_data = {
                "StatusCode": 6000,
                "detail": "success",
                "data":serializer.data,
                "message": "Data retrieved successfully"
                }
        except Exception as e:
            response_data = {
                "StatusCode": 6002,
                "detail": "error",
                "data":"",
                "message": f'Something went wrong {e}'
                }
        return Response(response_data, status=status.HTTP_200_OK)
     