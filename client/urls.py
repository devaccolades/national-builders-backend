from django.urls import path
from .views import *
urlpatterns = [
    path('home-page/', DataAPIView.as_view(), name='data-api'),
    
    path('projects/', ProjectsAPIView.as_view(), name='projects-api'),
    path('projects/<slug:slug>/', ProjectsAPIView.as_view(), name='projects-api'),
    
    path('branch-dropdown/', BranchDropDownAPIView.as_view(), name='branch-dropdown-api'),
    
    path('rentals/', RentalsAPIView.as_view(), name='rentals-api'),
    
    path('rental-enquiry/', RentalsEnquiryAPIView.as_view(), name='rentals-enquiry-api'),
    path('enquiry/', EnquiryAPIView.as_view(), name='enquiry-api'),

    path('testimonials/', TestimonialsAPIView.as_view(), name='testimonials-api'),
    
    path('blogs/', BlogsAPIView.as_view(), name='blogs-api'),
    path('blogs/<slug:slug>/', BlogsAPIView.as_view(), name='blogs-api'),
    
    path('news-and-events/', NewsAndEventsAPIView.as_view(), name='news-blogs-api'),
    path('news-and-events/<slug:slug>/', NewsAndEventsAPIView.as_view(), name='news-blogs-api'),
    
    path('key-hand-over/', KeyHandOverAPIView.as_view(), name='key-hand-over-api'),
    
    path('branch/', BranchAPIView.as_view(), name='branch-api'),
    
    path('seo/', SeoAPIView.as_view(), name='seo-api'),


]