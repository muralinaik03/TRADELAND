from django.http import HttpResponse
from django.shortcuts import render,redirect
from pathlib import Path
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm,profile_register_form,add_property_form,add_property_details_form,add_image_form,add_feature_form
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from property.models import property, property_images, property_features, property_details,city,featured
from users.models import users,User,wishlist
from django.views.generic import CreateView,UpdateView,DeleteView

# class basev4(View):
#     def get(self,request):
#         cities = city.objects.all()
#         context={'search_cities':cities}
#         return render(request,'testing/basev4.html',context)
#     def post(self,request):
#         title = request.POST.get('search_title')
#         min_area = int(request.POST.get('search_min_area'))
#         max_area = int(request.POST.get('search_max_area'))
#         min_price = int(request.POST.get('search_min_price'))
#         max_price = int(request.POST.get('search_max_price'))
#         city_name = request.POST.get('city_search_dropdown')
#         if city_name == "All Cities":
#             results= property.objects.all().filter(title__icontains=title,area__gte=min_area,area__lte=max_price,price__gte=min_price,price__lte=max_price)
#         else:
#             city_obj=city.objects.all().filter(name=city_name)[0]
#             results= property.objects.all().filter(title__icontains=title,area__gte=min_area,area__lte=max_price,price__gte=min_price,price__lte=max_price,city=city_obj)
#         context = {'user_properties': results}
#         return render(request,'search.html',context)

class wishlist_view(LoginRequiredMixin,View):
    def get(self,request):
        properties = wishlist.objects.all().filter(user=request.user)
        context = {'user_properties': properties}
        return render(request,'wishlist.html',context)

class add_to_wishlist(LoginRequiredMixin,View):
    def get(self,request,pk):
        try :
            prop = property.objects.all().filter(id=pk)[0]
        except:
            context={'title':"No such property",'error':"The property that you wish to wishlist doesn't exist"}
            return render(request,'404.html',context)
        try:
            wishlisted = wishlist.objects.all().filter(user=request.user,prop=prop)[0]
            return render(request,'wishlisted_already.html',context={'prop':prop})
        except:
            return render(request,'wishlist_confirm_add.html',context={'prop':prop})
        
    def post(self,request,pk):
        prop = property.objects.all().filter(id=pk)[0]
        obj = wishlist(user=request.user, prop=prop)
        obj.save()
        return redirect('wishlist')

class remove_from_wishlist(LoginRequiredMixin,View):
    def get(self,request,pk):
        try :
            prop = property.objects.all().filter(id=pk)[0]
        except:
            context={'title':"No such property",'error':"The property that you wish remove from wishlist doesn't exist"}
            return render(request,'404.html',context)
        wishlisted = wishlist.objects.all().filter(user=request.user)
        check = False
        for row in wishlisted:
            if prop == row.prop:
                check=True
                row.delete()
                break
        return redirect('/wishlist')

class search_properties(View):
    def get(self,request):
        results= property.objects.all()
        context = {'user_properties': results}
        return render(request,'search.html',context)
    def post(self,request):
        title = request.POST.get('search_title')
        min_area = int(request.POST.get('search_min_area'))
        max_area = int(request.POST.get('search_max_area'))
        min_price = int(request.POST.get('search_min_price'))
        max_price = int(request.POST.get('search_max_price'))
        city_name = request.POST.get('city_search_dropdown')
        if city_name == "All Cities":
            results= property.objects.all().filter(title__icontains=title,area__gte=min_area,area__lte=max_price,price__gte=min_price,price__lte=max_price)
        else:
            city_obj=city.objects.all().filter(name=city_name)[0]
            results= property.objects.all().filter(title__icontains=title,area__gte=min_area,area__lte=max_price,price__gte=min_price,price__lte=max_price,city=city_obj)
        context = {'user_properties': results}
        return render(request,'search.html',context)

def basev3(request):
    return render(request, 'testing/basev3.html')

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

class edit_profile(LoginRequiredMixin,View):
    def post(self,request):
        form = RegisterForm(request.POST,instance=request.user)
        user_details = users.objects.all().filter(user=request.user)[0]
        pform = profile_register_form(request.POST,request.FILES,instance=user_details)
        if form.is_valid() and pform.is_valid():
            form.save()
            pform.save()
            return redirect('/home') # Make it my profile.
        return render(request, 'registration/sign_up.html',{'form':form,'pform':pform})
    def get(self,request):
        form = RegisterForm(instance = request.user)
        user_details = users.objects.all().filter(user=request.user)[0]
        pform = profile_register_form(instance=user_details)
        return render(request,'registration/sign_up.html',{'form':form,'pform':pform})


def index(request):
    fe = featured.objects.all()
    return render(request, 'index.html',{'fe':fe})

def about(request):
    return render(request,'about.html')

chat = premium =contact =my_properties = offers =basev3
class myproperties(LoginRequiredMixin,View):
    def get(self,request):
        context = {'user_properties' : property.objects.all().filter(agent=request.user)}
        return render(request,'my_properties/show.html',context)
    post = get

def view_property(request,pk):
    try:
        prop = property.objects.all().filter(id=pk)[0]
        images = property_images.objects.all().filter(property=prop)
        features = property_features.objects.all().filter(property=prop)
        print(features)
        details = property_details.objects.all().filter(property=prop)[0]
        agent_details = users.objects.all().filter(user=prop.agent)[0]
        property_premium = agent_details.is_premium_agent
        try:
            user_details = users.objects.all().filter(user=request.user)[0]
            premium_user = user_details.is_premium_client
        except:
            premium_user = False
        pview = premium_user or not property_premium
        context = {'prop' : prop, 'prop_images':images, 'prop_features':features, 'prop_details':details, 'premium':pview,'agent_details':agent_details}
        return render(request, 'view_property/v2.html',context)
    except:
        return render(request,'404.html',{'title':'Property Not Found!','error':"<h2> Property Not Found </h2> <p> The property you are looking doesn't exist. Go back to <a href=\"/home\">home</a></p>"})

class add_property(LoginRequiredMixin,View):
    def get(self,request):
        prop_form = add_property_form()
        prop_details_form = add_property_details_form()
        context = {'prop_form':prop_form,'prop_details_form':prop_details_form}
        return render(request,'property/add_property.html',context)
    def post(self,request):
        form = add_property_form(request.POST,request.FILES)
        details = add_property_details_form(request.POST)
        if form.is_valid() and details.is_valid():
            obj = form.save(commit=False)
            det = details.save(commit=False)
            obj.agent = request.user
            obj.status = True
            obj.save()
            obj.refresh_from_db()
            det.property = obj
            det.save()
            return redirect('/home')#Change to success page later.
        else:
            context = {'prop_form':form,'prop_details_from':details}
            return render(request,'property/add_property.html',context)

class update_property(LoginRequiredMixin,View):
    def get(self,request,pk):
        try:
            p = property.objects.all().filter(id=pk)[0]
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'obj':'Property'}
            return render(request,'404.html',context)
        try:
            pd = property_details.objects.all().filter(property=p)[0]
        except:
            context={'error':"Uh oh! there is some error. Go back to <a href=\"/home\">home</a>.",'obj':'Brain'}
            return render(request,'404.html',context)
        if p.agent != request.user:
            return render(request,'404.html',{'error':"The action you are trying is forbidden to you. Go to <a href=\"/home\">home</a>.",'title':'Forbidden'})
        pf = add_property_form(instance=p)
        pdf = add_property_details_form(instance=pd)
        context = {'prop_form':pf,'prop_details_form':pdf}
        return render(request,'property/add_property.html',context)

    def post(self,request,pk):
        # I hate my life why isnt this working :(((((((((
        p = property.objects.all().filter(id=pk)[0]
        pd = property_details.objects.all().filter(property=p)[0]
        form = add_property_form(request.POST,request.FILES,instance=p)
        details = add_property_details_form(request.POST,instance=pd)
        if form.is_valid() and details.is_valid():
            form.save()
            details.save()
            return redirect('/home')#Change to success page later.
        else:
            context = {'prop_form':form,'prop_details_from':details}
            return render(request,'property/add_property.html',context)

class premium(LoginRequiredMixin,View):
    def get(self,request):
        user_details = users.objects.all().filter(user=request.user)[0]
        is_premium_client = user_details.is_premium_client
        context = {'havepremium':is_premium_client}
        return render(request,'premium.html',context)


class delete_property(LoginRequiredMixin,View):
    def get(self,request,pk):
        try:
            p = property.objects.all().filter(id=pk)[0]
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'title':'Property'}
            return render(request,'404.html',context)
        if p.agent != request.user:
            return render(request,'404.html',{'error':"The action you are trying is forbidden to you. Go to <a href=\"/home\">home</a>.",'title':'Forbidden'})
        context = {'item':'property ' + p.title }
        return render(request,'confirmdelete.html',context)
    
    def post(self,request,pk):
        p = property.objects.all().filter(id=pk)[0]
        p.delete()
        return redirect('/home')

class add_image(LoginRequiredMixin,View):
    def get(self,request,pk):
        try:
            p = property.objects.all().filter(id=pk)[0]
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'title':'Property'}
            return render(request,'404.html',context)
        if p.agent != request.user:
            return render(request,'404.html',{'error':"The action you are trying is forbidden to you. Go to <a href=\"/home\">home</a>.",'title':'Forbidden'})
        # context = {'item':'property ' + p.title }
        form = add_image_form()
        context={'form':form,'prop':p}
        return render(request,'property/add_image.html',context)
    
    def post(self,request,pk):
        p = property.objects.all().filter(id=pk)[0]
        form = add_image_form(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.property=p
            image.save()
            return redirect('/properties/'+str(p.id))
        else:
            context={'form':form,'prop':p}
            return render(request,'property/add_image.html',context)

class delete_image(LoginRequiredMixin,View):
    def get(self,request,pk):
        try:
            p = property.objects.all().filter(id=pk)[0]
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'title':'Property'}
            return render(request,'404.html',context)
        try:
            i = property_images.objects.all().filter(property=p)
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'title':'Property'}
            return render(request,'404.html',context)
        if p.agent != request.user:
            return render(request,'404.html',{'error':"The action you are trying is forbidden to you. Go to <a href=\"/home\">home</a>.",'title':'Forbidden'})
        # context = {'item':'property ' + p.title }
        context={'prop':p,'images':i}
        return render(request,'property/delete_image.html',context)
    
    def post(self,request,pk):
        p = property.objects.all().filter(id=pk)[0]
        i = property_images.objects.all().filter(property=p)
        for img in i:
            if request.POST.get(str(p.id) +"_"+str(img.id),False) or request.POST.get(str(p.id) +"_"+str(img.id),False)=='True':
                img.delete()
        return redirect('/properties/'+str(p.id))

class delete_feature(LoginRequiredMixin,View):
    def get(self,request,pk):
        try:
            p = property.objects.all().filter(id=pk)[0]
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'title':'Property'}
            return render(request,'404.html',context)
        try:
            d = property_features.objects.all().filter(property=p)
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'title':'Property'}
            return render(request,'404.html',context)
        if p.agent != request.user:
            return render(request,'404.html',{'error':"The action you are trying is forbidden to you. Go to <a href=\"/home\">home</a>.",'title':'Forbidden'})
        # context = {'item':'property ' + p.title }
        context={'prop':p,'d':d}
        return render(request,'property/delete_feature.html',context)
    
    def post(self,request,pk):
        p = property.objects.all().filter(id=pk)[0]
        d = property_features.objects.all().filter(property=p)
        for f in d:
            if request.POST.get(str(p.id) +"_"+str(f.id),False) or request.POST.get(str(p.id) +"_"+str(f.id),False)=='True':
                f.delete()
        return redirect('/properties/'+str(p.id))

class add_feature(LoginRequiredMixin,View):
    def get(self,request,pk):
        try:
            p = property.objects.all().filter(id=pk)[0]
        except:
            context={'error':"The property you are asking isn't present. Go back to <a href=\"/home\">home</a>.",'title':'Property'}
            return render(request,'404.html',context)
        if p.agent != request.user:
            return render(request,'404.html',{'error':"The action you are trying is forbidden to you. Go to <a href=\"/home\">home</a>.",'title':'Forbidden'})
        # context = {'item':'property ' + p.title }
        form = add_feature_form()
        context={'form':form,'prop':p}
        return render(request,'property/add_feature.html',context)
    
    def post(self,request,pk):
        p = property.objects.all().filter(id=pk)[0]
        form = add_feature_form(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.property=p
            f.save()
            return redirect('/properties/'+str(p.id))
        else:
            context={'form':form,'prop':p}
            return render(request,'property/add_feature.html',context)



