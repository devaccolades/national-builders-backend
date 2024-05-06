from django.urls import path
from .views import *
urlpatterns = [
    path('amenities/', AmenitiesAPIView.as_view(), name='amenities-crud-view'),
    path('amenities/<uuid:id>/', AmenitiesAPIView.as_view(), name='amenities-update-delete-view'),
    
]

