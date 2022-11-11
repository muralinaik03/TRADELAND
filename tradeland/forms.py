from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from users.models import users

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

