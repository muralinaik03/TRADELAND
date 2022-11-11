from django.http import HttpResponse
from django.shortcuts import render,redirect
from pathlib import Path
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm,profile_register_form
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from property.models import property, property_images, property_features, property_details
from users.models import users

def basev3(request):
    return render(request,'testing/basev3.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        pform = profile_register_form(request.POST,request.FILES)
        if form.is_valid() and pform.is_valid():
            user = form.save()
            user.refresh_from_db()
            pform=profile_register_form(request.POST,request.FILES)
            pform.full_clean()
            profile = pform.save(commit=False)
            profile.user=user
            profile.save()
            login(request,user)
            return redirect('/home')
    else:
        form = RegisterForm()
        pform = profile_register_form()
    return render(request, 'registration/sign_up.html',{'form':form,'pform':pform})


def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request,'testing/basev2.html')

chat = premium =contact =my_properties = offers =basev3
class myproperties(View):
    def get(self,request):
        if request.user.is_authenticated:
            context = {'user_properties' : property.objects.all().filter(agent=request.user)}
            return render(request,'my_properties/show.html',context)
        else:
            return redirect('login')
    post =get

def view_property(request,pk):
    prop = property.objects.all().filter(id=pk)[0]
    images = property_images.objects.all().filter(property=prop)
    features = property_features.objects.all().filter(property=prop)
    details = property_details.objects.all().filter(property=prop)[0]
    agent_details = users.objects.all().filter(user=prop.agent)[0]
    user_details = users.objects.all().filter(user=request.user)[0]
    property_premium = agent_details.is_premium_agent
    premium_user = user_details.is_premium_client
    pview = premium_user or not property_premium
    context = {'prop' : prop, 'prop_images':images, 'prop_featues':features, 'prop_details':details, 'premium':pview,'agent_details':agent_details}
    return render(request, 'view_property/view_property.html',context)


