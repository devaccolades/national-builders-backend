from django.urls import path
from .views import *
urlpatterns = [
    path('amenities/', AmenitiesAPIView.as_view(), name='amenities-crud-view'),
    path('amenities/<uuid:id>/', AmenitiesAPIView.as_view(), name='amenities-update-delete-view'),
    
    path('project-add/', ProjectApiView.as_view(), name='project-add'),
    path('project-get/', ProjectApiView.as_view(), name='project-list'),
    path('project-update/<slug:slug>/', ProjectApiView.as_view(), name='project-list'),
    path('project-get/<slug:slug>/', ProjectApiView.as_view(), name='project-add'),


    
]

