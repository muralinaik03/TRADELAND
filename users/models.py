from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from tradeland.settings import BASE_DIR
from property.models import property
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(BASE_DIR,'media/property', filename)

def validate_phone(value):
    if len(value) !=10 or not value.isnumeric():
        raise ValidationError('Phone number only contains 0-9 and 10 digits must be present.')
    else:
        return value

class gender_of_user(models.Model):
    gender = models.CharField(max_length=10)
    def __str__(self):
        return self.gender

def gender_default(*args, **kwargs):
    return gender_of_user.objects.all().filter(id=1)

# Create your models here.
class users(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    gender = models.ForeignKey(gender_of_user,default=User.objects.all().filter(id=1),on_delete=gender_default,null=True)
    description = models.TextField(blank=True)
    profile_picture = models.ImageField(null=True,blank=True,upload_to=get_file_path)
    mobile_number = models.CharField(max_length=10,default='0000000000',null=False,validators=[validate_phone])
    is_premium_agent = models.BooleanField(default=False)
    is_premium_client = models.BooleanField(default=False)
    rating = models.FloatField(null=True,default=0)

    def __str__(self):
        return self.user.username

class wishlist(models.Model):
    prop =  models.ForeignKey(property,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.prop.title + " "+self.user.username
    
    class Meta:
        verbose_name_plural = "wishlist"

