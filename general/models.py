from django.db import models
import uuid
from ckeditor.fields import RichTextField
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class CompanyBranch(BaseModel):
    location = models.CharField(max_length=150)
    image = models.ImageField(upload_to='companybranch/image', null=True, blank=True)
    iframe = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=255,null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True)
    show_user_side = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'companybranch'
        verbose_name = ('Company Branch')
        verbose_name_plural = ('Company Branchs')
        ordering = ('date_added',)

    def __str__(self):
        return self.location
    

class KeyHandOver(BaseModel):
    name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='keyhandover/image', null=True, blank=True)

    class Meta:
            db_table = 'keyhandover'
            verbose_name = ('Key HandOver')
            verbose_name_plural = ('Key HandOver')
            ordering = ('-date_added',)

    def __str__(self):
        return self.name
        
    
class Testimonieals(BaseModel):
    name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='testimonieals/image', null=True, blank=True)
    project=models.ForeignKey('project.Project',on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'testimonieals'
        verbose_name = ('Testimonieal')
        verbose_name_plural = ('Testimoniealss')
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

class Blogs(BaseModel):
    image=models.ImageField(upload_to='blogs/image',blank=True,null=True)
    title = models.CharField(max_length=300, blank=True, default='',null=True)
    body = RichTextField(blank=True)
    image_alt = models.CharField(max_length=125, null=True, blank=True)
    meta_tag=models.CharField(max_length=300, blank=True, default='',null=True)
    meta_description=models.CharField(max_length=300, blank=True, default='',null=True)
    slug = models.SlugField(default="", unique=True)

    class Meta:
        db_table = 'Blogs'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.title)
    
class NewAndEvents(BaseModel):
    image=models.ImageField(upload_to='blogs/image',blank=True,null=True)
    title = models.CharField(max_length=300, blank=True, default='',null=True)
    body = RichTextField(blank=True)
    image_alt = models.CharField(max_length=125, null=True, blank=True)
    youtube_link = models.CharField(max_length=255, blank=True, null=True)
    meta_tag=models.CharField(max_length=300, blank=True, default='',null=True)
    meta_description=models.CharField(max_length=300, blank=True, default='',null=True)
    slug = models.SlugField(default="", unique=True)

    class Meta:
        db_table = 'newandevents'
        verbose_name = 'New And Event'
        verbose_name_plural = 'New And Events'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.title)
    

class SEO(BaseModel):
    page=models.CharField(max_length=200,blank=True,null=True)
    path=models.CharField(max_length=200,blank=True,null=True)
    meta_title=models.TextField(blank=True,null=True)
    meta_description=models.TextField(blank=True,null=True)
    class Meta:
        db_table='seo'
        verbose_name = ('SEO')
        verbose_name_plural = ('SEO')
        ordering = ('date_added',)
