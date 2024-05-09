from django.db import models
import uuid

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