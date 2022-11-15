from django.db import models

# Create your models here.
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime
from tradeland.settings import BASE_DIR
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(BASE_DIR,'media/property', filename)

class city(models.Model):
    name = models.CharField(max_length=100,default="Varanasi")
    state = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name

# North, East, West, South, North-East, North-West, South-East, South-West
class facing(models.Model):
    facing = models.CharField(max_length=11)

    # To correct plural showin in admin.
    class Meta:
        verbose_name_plural = "facing"

    def __str__(self):
        return self.facing

# Main road or alley road or none
class overlooking(models.Model):
    overlooking = models.CharField(max_length=10)
    
    class Meta:
        verbose_name_plural = "overlooking"

    def __str__(self):
        return self.overlooking

# Mediate, Immediate, Adverse, Constructive
class possession(models.Model):
    possession = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "possession"
    
    def __str__(self):
        return self.possession

# Cash, Transfer/Credit
class transaction_type(models.Model):
    transaction_type = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "transaction_types"
    
    def __str__(self):
        return self.transaction_type

# Owner, Co-owner
class property_ownership(models.Model):
    property_ownership = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "property_ownership"
    
    def __str__(self):
        return self.property_ownership

# class pincode(models.Model):
#     pincode = models.CharField(max_length=6)
#     city = models.ForeignKey(city, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.pincode

class property(models.Model):
    title = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    agent = models.ForeignKey(User,related_name='agent',on_delete=models.CASCADE)
    street_address = models.CharField(max_length=250,default='')
    landmark = models.CharField(max_length=150,blank=True)
    area = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()
    city = models.ForeignKey(city,on_delete=models.CASCADE)
    # pincode = models.ForeignKey(pincode, on_delete=models.SET_NULL,null=True)
    main_picture = models.ImageField(upload_to=get_file_path)

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return self.title

class property_details(models.Model):
    property = models.OneToOneField(property,related_name='property',on_delete=models.CASCADE)
    length = models.PositiveIntegerField()
    breadth = models.PositiveIntegerField()
    floors_allowed = models.PositiveIntegerField()
    facing = models.ForeignKey(facing,on_delete=models.CASCADE)
    overlooking = models.ForeignKey(overlooking,on_delete=models.CASCADE)
    possession = models.ForeignKey(possession,on_delete=models.CASCADE)
    boundary_wall = models.BooleanField(default=False)
    transaction_type = models.ForeignKey(transaction_type,on_delete=models.CASCADE)
    property_ownership = models.ForeignKey(property_ownership,on_delete=models.CASCADE)
    width_of_facing_road = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    yt_video = models.URLField(max_length=500,default='https://player.vimeo.com/video/73221098',blank=True)
    map = models.URLField(max_length=500,default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3608.2455290309986!2d82.98937350000001!3d25.2623247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x398e3320e885927b%3A0x78ac04d1bac708f0!2sIIT%20(BHU)%20Varanasi!5e0!3m2!1sen!2sin!4v1668192349845!5m2!1sen!2sin',blank=True)

    class Meta:
        verbose_name_plural = "property_details"

    def __str__(self):
        return self.property.title

class property_images(models.Model):
    property = models.ForeignKey(property,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=get_file_path)

    class Meta:
        verbose_name_plural = "property_images"

    def __str__(self):
        return self.property.title + " "+ self.title

class property_features(models.Model):
    property = models.ForeignKey(property,on_delete=models.CASCADE)
    feature = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "property_features"

    def __str__(self):
        return self.feature


class featured(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=30)
    prop = models.ForeignKey(property,on_delete=models.CASCADE)
    city_state = models.CharField(max_length=25)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.text + self.title