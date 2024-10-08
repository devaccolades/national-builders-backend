from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectAmenities)
admin.site.register(ProjectSpecification)
admin.site.register(ProjectImages)
admin.site.register(FloorPlanImages)
admin.site.register(ProjectDistance)
admin.site.register(Rentals)
admin.site.register(Enquiry)
admin.site.register(RentalEnquiry)

@admin.register(CurrentStatus)
class CurrentStatusAdmin(admin.ModelAdmin):
    list_display = ('project', 'year', 'month')
    list_filter = ('project', 'year', 'month', 'is_deleted')
    search_fields = ('project__name', 'year', 'month')
