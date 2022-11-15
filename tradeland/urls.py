"""tradeland URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.index,name="home"),
    path('', views.index, name="index"),
    path('addproperty',views.add_property.as_view(),name="addproperty"),
    path('updateproperty/<int:pk>',views.update_property.as_view(),name="update_property"),
    path('addimage/<int:pk>',views.add_image.as_view(),name="add_image"),
    path('addfeature/<int:pk>',views.add_feature.as_view(),name="add_feature"),
    path('deleteimage/<int:pk>',views.delete_image.as_view(),name="delete_image"),
    path('deletefeature/<int:pk>',views.delete_feature.as_view(),name="delete_feature"),
    path('deleteproperty/<int:pk>',views.delete_property.as_view(),name="delete_property"),
    path('myproperties',views.myproperties.as_view(),name="myproperties"),
    path('properties/<int:pk>',views.view_property,name="viewproperty"),
    path('wishlist',views.wishlist_view.as_view(),name="wishlist"),
    path('addtowishlist/<int:pk>',views.add_to_wishlist.as_view(),name="add_to_wishlist"),
    path('removefromwishlist/<int:pk>',views.remove_from_wishlist.as_view(),name="remove_from_wishlist"),
    path('myprofile',views.wishlist_view.as_view(),name="myprofile"),
    path('editprofile',views.edit_profile.as_view(),name="editprofile"),
    path('chat',views.chat,name="chat"),
    path('premium',views.premium.as_view(),name="premium"),
    path('about',views.about,name="about"),
    path('', include('django.contrib.auth.urls')),
    path('sign-up',views.sign_up,name="signup"),
    path('searchproperties',views.search_properties.as_view(),name="searchproperties"),
    # testing
    # path('testing/basev4',views.basev4.as_view(),name="testingbasev3"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)