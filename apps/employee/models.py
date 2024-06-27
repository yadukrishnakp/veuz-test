from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from veuz_core.models import AbstractDateTimeFieldBaseModel

# Create your models here.
class EmployeeDetails(AbstractDateTimeFieldBaseModel):
    slug          = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    name          = models.CharField(max_length=256,null=True, blank=True)
    email         = models.CharField(max_length=256,null=True, blank=True)
    phonenumber   = models.CharField(max_length=256,null=True, blank=True)
    
    class Meta: 
        verbose_name          = "EmployeeDetails"
        verbose_name_plural   = "EmployeeDetailss"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if EmployeeDetails.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(EmployeeDetails, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class EmployeeSettings(AbstractDateTimeFieldBaseModel):
    FIELD_TYPES = [
        ('String', 'String'),
        ('Number', 'Number'),
    ]        
    field_type        = models.CharField(max_length=100,choices=FIELD_TYPES, blank=True, null=True)
    slug             = models.SlugField(_('Slug'), max_length=100, editable=False, null=True, blank=True)
    name             = models.CharField(max_length=256,null=True, blank=True)
    value            = models.CharField(max_length=256,null=True, blank=True)
    employee_details = models.ForeignKey(EmployeeDetails, related_name="employee_details", on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta: 
        verbose_name          = "EmployeeSettings"
        verbose_name_plural   = "EmployeeSettings"
        
    def save(self, *args, **kwargs):
        if not self.slug or self.name:
            self.slug = slugify(str(self.name))
            if EmployeeSettings.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.name)) + '-' + str(randint(1, 9999999))
        super(EmployeeSettings, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name