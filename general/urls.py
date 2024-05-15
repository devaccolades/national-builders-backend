from django.urls import path
from .views import *
urlpatterns = [
    path('branch/', BranchAPIView.as_view(), name='branch-crud-view'),
    path('branch/<uuid:id>/', BranchAPIView.as_view(), name='branch-update-delete-view'),
    
    path('branch-selection/<uuid:id>/', BranchSelectionAPIView.as_view(), name='branch-userside-selection'),
    path('company-branches-dropdown/', CompanyBranchDropdownListView.as_view(), name='company-branch-dropdown-list'),
    
    path('key-handover/', KeyHandOverAPIView.as_view(), name='key-handdover-get-add'),
    path('key-handover/<uuid:id>/', KeyHandOverAPIView.as_view(), name='key-handdover-update-delete'),
    
    path('Testimonials/', TestimonialsAPIView.as_view(), name='Testimonials-get-add'),
    path('Testimonials/<uuid:id>/', TestimonialsAPIView.as_view(), name='Testimonials-update-delete'),
    
    path('blogs/', BlogsAPIView.as_view(), name='blogs-get-add'),
    path('blogs/<uuid:id>/', BlogsAPIView.as_view(), name='blogs-update-delet'),
   
    path('news-and-events/', NewsAndEventsAPIView.as_view(), name='news-and-events-get-add'),
    path('news-and-events/<uuid:id>/', NewsAndEventsAPIView.as_view(), name='news-and-events-update-delete'),
    
    path('seo/', SeoAPIView.as_view(), name='seo-get-post'),
    path('seo/<uuid:id>/', SeoAPIView.as_view(), name='seo-update-delete'),
    
    path('project-count-homepage/', ProjectCoutsAPIView.as_view(), name='projectcouts-get'),
    path('project-count-homepage/<int:id>/', ProjectCoutsAPIView.as_view(), name='projectcouts-update'),
   
    path('awards/', AwardsAPIView.as_view(), name='awards-get'),
    path('awards/<uuid:id>/', AwardsAPIView.as_view(), name='awards-get'),
    
    path('home-page-videos/', HomePageVideoAPIView.as_view(), name='awards-get'),
    path('home-page-videos/<int:id>/', HomePageVideoAPIView.as_view(), name='awards-update'),



]

