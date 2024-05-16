from django.urls import path
from .views import *
urlpatterns = [
    path('home-page/', DataAPIView.as_view(), name='data-api'),
    
    # path('testimonials/', TestimonialsAPIView.as_view(), name='testimonials-api'),
    
    # path('blogs/', BlogsAPIView.as_view(), name='blogs-api'),
    
    path('projects/', ProjectsAPIView.as_view(), name='projects-api'),
    path('projects/<slug:slug>/', ProjectsAPIView.as_view(), name='projects-api'),
    path('branch-dropdown/', BranchDropDownAPIView.as_view(), name='branch-dropdown-api'),


]