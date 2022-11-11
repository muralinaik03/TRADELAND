from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    profile_picture = models.ImageField(null=True,blank=True,upload_to="users/images/")
    mobile_number = models.CharField(max_length=10,default='0000000000',null=False,validators=[validate_phone])
    no_of_properties_sold = models.PositiveIntegerField(default=0)
    no_of_properties_bought = models.PositiveIntegerField(default=0)
    is_premium_agent = models.BooleanField(default=False)
    is_premium_client = models.BooleanField(default=False)
    rating = models.FloatField(null=True,default=0)

    def __str__(self):
        return self.user.username

