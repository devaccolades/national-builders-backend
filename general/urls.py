from django.urls import path
from .views import *
urlpatterns = [
    path('branch/', BranchAPIView.as_view(), name='branch-crud-view'),
    path('branch/<uuid:id>/', BranchAPIView.as_view(), name='branch-update-delete-view'),
    
    path('branch-selection/<uuid:id>/', BranchSelectionAPIView.as_view(), name='branch-userside-selection'),
    path('company-branches-dropdown/', CompanyBranchDropdownListView.as_view(), name='company-branch-dropdown-list'),

]

