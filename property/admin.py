# Register your models here.
from django.contrib import admin
from .models import city,facing,overlooking,possession,transaction_type,property_ownership,property_details,property_features,property_images,property,featured

# Register your models here.
admin.site.register(city)
admin.site.register(facing)
admin.site.register(overlooking)
admin.site.register(possession)
admin.site.register(transaction_type)
admin.site.register(property_ownership)
admin.site.register(property_details)
admin.site.register(property)
admin.site.register(property_features)
admin.site.register(property_images)
admin.site.register(featured)
