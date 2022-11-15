from property.models import city

def all_cities(request):
    allcities = city.objects.all()
    context = {'search_cities':allcities}
    return context