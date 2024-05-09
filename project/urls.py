from django.urls import path
from .views import *
urlpatterns = [
    path('amenities/', AmenitiesAPIView.as_view(), name='amenities-crud-view'),
    path('amenities/<uuid:id>/', AmenitiesAPIView.as_view(), name='amenities-update-delete-view'),
    
    path('project-add/', ProjectApiView.as_view(), name='project-add'),
    path('project-get/', ProjectApiView.as_view(), name='project-list'),
    path('project-update/<slug:slug>/', ProjectApiView.as_view(), name='project-list'),
    path('project-get/<slug:slug>/', ProjectApiView.as_view(), name='project-get-single-view'),
    path('project-delete/<uuid:id>/', ProjectApiView.as_view(), name='project-add'),
    
    path('project-images-add/', ProjectImagesApiView.as_view(), name='project-image-add'),
    path('project-images-get/<uuid:projectId>/', ProjectImagesApiView.as_view(), name='project-image-get'),
    path('project-images-update/<uuid:id>/', ProjectImagesApiView.as_view(), name='project-image-update'),
    path('project-images-delete/<uuid:id>/', ProjectImagesApiView.as_view(), name='project-image-get'),

    path('floor-plan-images-add/', FloorPlanImagesApiView.as_view(), name='floor-plan-image-add'),
    path('floor-plan-images-get/<uuid:projectId>/', FloorPlanImagesApiView.as_view(), name='floor-plan-image-get'),
    path('floor-plan-images-update/<uuid:id>/', FloorPlanImagesApiView.as_view(), name='floor-plan-image-update'),
    path('floor-plan-images-delete/<uuid:id>/', FloorPlanImagesApiView.as_view(), name='floor-plan-image-update'),
    
    path('project-amenities-add/<uuid:projectId>/', ProjectAmenitiesAPIView.as_view(), name='project-related-amenities-add'),
    path('project-amenities-get/<uuid:projectId>/', ProjectAmenitiesAPIView.as_view(), name='project-related-amenities-get'),
    
    path('specifications-add/', SpecificationsApiView.as_view(), name='specifications-add'),
    path('specifications-get/<uuid:projectId>/', SpecificationsApiView.as_view(), name='specifications-get'),
    path('specifications-update/<uuid:id>/', SpecificationsApiView.as_view(), name='specifications-update'),
    path('specifications-delete/<uuid:id>/', SpecificationsApiView.as_view(), name='specifications-delete'),
    
    path('project-distance-add/', DistanceApiView.as_view(), name='project-distance-delete'),
    path('project-distance-get/<uuid:projectId>/', DistanceApiView.as_view(), name='project-distance-get'),
    path('project-distance-edit/<uuid:id>/', DistanceApiView.as_view(), name='project-distance-edit'),
    path('project-distance-delet/<uuid:id>/', DistanceApiView.as_view(), name='project-distance-delete'),
    
    path('rental/', RentalsAPIView.as_view(), name='rental-add-get'),
    path('rental/<uuid:id>/', RentalsAPIView.as_view(), name='rental-update-delete'),

    

    

]

