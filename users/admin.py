from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

# Register your models here.
admin.site.register(users)
admin.site.register(gender_of_user)
admin.site.register(wishlist)