from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from users.models import users
from property.models import property,property_details,property_features,property_images


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in [ 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class profile_register_form(ModelForm):
    class Meta:
        model = users
        fields = ['gender','mobile_number','description','profile_picture']

class add_property_form(ModelForm):
    class Meta:
        model = property
        fields = ['title','area','street_address', 'landmark','price','city','main_picture']

class add_property_details_form(ModelForm):
    class Meta:
        model = property_details
        fields = ['length','breadth','floors_allowed','facing','overlooking','possession','boundary_wall','transaction_type','property_ownership','width_of_facing_road','description','yt_video','map']

