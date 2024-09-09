from django.db import models
from general.models import BaseModel,CompanyBranch
# Create your models here.

PROJECT_TYPE_CHOICES = (
    ('apartment', 'apartment'),
    ('villas', 'villas'),
    ('commercial', 'commercial'),
    ('rental', 'rental'),
    ('residential','residential'),
    ('residential cum commercial', 'residential cum commercial'),
    ('other','other')
)

PROJECT_STATUS_CHOICES = (
    ('new launch', 'new launch'),
    ('on going', 'on going'),
    ('ready to occupy', 'ready to occupy'),
    ('nearing completion', 'nearing completion'),
    ('under construction', 'under construction'),
    ('sold out', 'sold out'),
)

PROJECT_DISTANCE_CHOICES = (
    ('km', 'km'),
    ('meter', 'meter'),
)

Month_CHOICES = (
    ('january', 'January'),
    ('february', 'February'),
    ('march', 'March'),
    ('april', 'April'),
    ('may', 'May'),
    ('june', 'June'),
    ('july', 'July'),
    ('august', 'August'),
    ('september', 'September'),
    ('october', 'October'),
    ('november', 'November'),
    ('december', 'December'),
)



class ProjectAmenities(BaseModel):
    logo = models.FileField(upload_to='projects/image', null=True, blank=True)
    image_alt = models.CharField(max_length=125, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'ProjectAmenities'
        verbose_name = ('Project Amenitie')
        verbose_name_plural = ('Project Amenities')
        ordering = ('date_added',)
 

class Project(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(upload_to='projects/image', null=True, blank=True)
    thumbnail_alt = models.CharField(max_length=125, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rera_number=models.CharField(max_length=500,blank=True,null=True)
    logo = models.ImageField(upload_to='projects/image',blank=True,null=True)
    qr_code=models.ImageField(upload_to='projects/image',blank=True,null=True)
    qr_code_alt = models.CharField(max_length=125, null=True, blank=True)
    brochure = models.FileField(upload_to='projects/brochure',blank=True,null=True)
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
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

class ProjectImages(BaseModel):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='projects/image', null=True, blank=True)
    image_alt = models.CharField(max_length=125, null=True, blank=True)
    order = models.IntegerField(blank=True,null=True,default=1)
    class Meta:
        db_table = 'ProjectImages'
        verbose_name = ('Project Image')
        verbose_name_plural = ('Project Images')
        ordering = ('date_added',)

class FloorPlanImages(BaseModel):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='projects/image', null=True, blank=True)
    image_alt = models.CharField(max_length=125, null=True, blank=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    order = models.IntegerField(blank=True,null=True,default=1)
    class Meta:
        db_table = 'FloorlanImages'
        verbose_name = ('Floor Plan Image')
        verbose_name_plural = ('Floor Plan Images')
        ordering = ('date_added',)

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
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    location_name = models.CharField(max_length=255,null=True,blank=True)
    distance = models.CharField(max_length=150,null=True,blank=True)
    measurement_unit = models.CharField(choices=PROJECT_DISTANCE_CHOICES, max_length=255)

    class Meta:
        db_table = 'ProjectDistance'
        verbose_name = ('Project Distance')
        verbose_name_plural = ('Project Distance')
        ordering = ('date_added',)


class Rentals(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='rentals/image', null=True, blank=True)
    image_alt = models.CharField(max_length=125, null=True, blank=True)
    company_branch = models.ForeignKey(CompanyBranch, on_delete=models.SET_NULL, null=True)
    type = models.CharField(choices=PROJECT_TYPE_CHOICES, max_length=255)
    area = models.CharField(max_length=255,blank=True,null=True)
    price = models.CharField(max_length=255,blank=True,null=True)
    is_hide = models.BooleanField(default=False)

    class Meta:
        db_table='Rentals'
        verbose_name = ('Rentals')
        verbose_name_plural = ('Rentals')
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.name)
    
class CurrentStatus(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    year = models.BigIntegerField(null=True, blank=True)
    month = models.CharField(choices=Month_CHOICES, max_length=100) 
    image = models.ImageField(upload_to='projects/images/')
    image_alt = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        db_table = 'projects.project_current_status'
        verbose_name = 'Current Status'
        verbose_name_plural = 'Current Statuses'
        ordering = ('-date_added',)

    def __str__(self):
        return f"{self.month} {self.year}"

class Enquiry(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    enquiry_date=models.DateTimeField(auto_now_add=True)
    first_name=models.CharField(max_length=200,blank=True,null=True)
    last_name=models.CharField(max_length=200,blank=True,null=True)
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
    
class RentalEnquiry(models.Model):
    rentals=models.ForeignKey(Rentals,on_delete=models.CASCADE,null=True,blank=True)
    enquiry_date=models.DateTimeField(auto_now_add=True)
    first_name=models.CharField(max_length=200,blank=True,null=True)
    last_name=models.CharField(max_length=200,blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    phone=models.BigIntegerField(blank=True,null=True)
    message=models.TextField(blank=True,null=True)
    is_read=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='RentalEnquiry'
        verbose_name = ('Rental Enquiry')
        verbose_name_plural = ('Rental Enquirys')
        ordering = ('-enquiry_date',)

    
    def __str__(self):
        return str(self.enquiry_date)

