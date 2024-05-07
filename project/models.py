from django.db import models
from general.models import BaseModel,CompanyBranch
# Create your models here.

PROJECT_TYPE_CHOICES = (
    ('apartment', 'apartment'),
    ('villas', 'villas'),
    ('commercial', 'commercial'),
    ('rental', 'rental'),
    ('other','other')
)

PROJECT_STATUS_CHOICES = (
    ('new launch', 'new launch'),
    ('ready to occupy', 'ready to occupy'),
    ('under construction', 'under construction'),
    ('sold out', 'sold out'),
)




class ProjectAmenities(BaseModel):
    logo = models.FileField(upload_to='projects/image', null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'ProjectAmenities'
        verbose_name = ('Project Amenitie')
        verbose_name_plural = ('Project Amenities')
        ordering = ('date_added',)


class Project(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(upload_to='projects/image', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rera_number=models.CharField(max_length=500,blank=True,null=True)
    qr_code=models.ImageField(upload_to='projects/image',blank=True,null=True)
    location=models.CharField(max_length=500,blank=True,null=True) 
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.SET_NULL, null=True)
    type = models.CharField(choices=PROJECT_TYPE_CHOICES, max_length=255)
    status = models.CharField(choices=PROJECT_STATUS_CHOICES, max_length=255)
    units = models.CharField(max_length=255,blank=True,null=True)
    bedrooms = models.CharField(max_length=255,blank=True,null=True)
    area_from = models.CharField(max_length=255,blank=True,null=True)
    area_to = models.CharField(max_length=255,blank=True,null=True)
    amenities = models.ManyToManyField(ProjectAmenities)
    iframe = models.TextField(null=True, blank=True)
    meta_title=models.TextField(blank=True,null=True)
    meta_description=models.TextField(blank=True,null=True)
    slug = models.SlugField(default="", unique=True)

    class Meta:
        db_table = 'Projects'
        verbose_name = ('project')
        verbose_name_plural = ('projects')
        ordering = ('date_added',)

    def __str__(self):
        return self.name

class ProjectImages(BaseModel):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    images = models.ImageField(upload_to='projects/image', null=True, blank=True)
    order = models.IntegerField(blank=True,null=True,default=1)
    class Meta:
        db_table = 'ProjectImages'
        verbose_name = ('Project Image')
        verbose_name_plural = ('Project Images')
        ordering = ('order',)

class FloorPlanImages(BaseModel):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    images = models.ImageField(upload_to='projects/image', null=True, blank=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    order = models.IntegerField(blank=True,null=True,default=1)
    class Meta:
        db_table = 'FloorlanImages'
        verbose_name = ('Project Image')
        verbose_name_plural = ('Project Images')
        ordering = ('order',)

class ProjectSpecification(BaseModel):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ProjectSpecification'
        verbose_name = ('Project Specification')
        verbose_name_plural = ('Project Specifications')
        ordering = ('date_added',)

class ProjectDistance(BaseModel):
    location_name = models.CharField(max_length=255,null=True,blank=True)
    distance = models.CharField(max_length=150,null=True,blank=True)


class Enquiry(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    enquiry_date=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=200,blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    phone=models.BigIntegerField(blank=True,null=True)
    message=models.TextField(blank=True,null=True)
    is_read=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Enquiry'
        verbose_name = ('Enquiry')
        verbose_name_plural = ('Enquiry')
        ordering = ('-enquiry_date',)

    
    def __str__(self):
        return str(self.enquiry_date)

