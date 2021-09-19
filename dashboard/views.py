from dashboard.forms import CityForm
from dashboard.models import City
from django.shortcuts import render
from django.http import HttpResponse
from dashboard.data import get_weather_data
from django.template.response import TemplateResponse
# Create your views here.
def home(request):
    form = CityForm()   # Empty form initialize
   
    if request.method == 'POST': 
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            city_name = form.cleaned_data.get('city_name')     # work only when form data is saved
            weather_data = get_weather_data(city_name)
   
    elif request.method == 'GET':  
        try:                               
            city_name = City.objects.latest('date_added').city_name   # return previously searched data
            weather_data = get_weather_data(city_name)
        except Exception as e:
            weather_data = None
        
    
    

    dic = {'form': form, 'weather_data': weather_data}
    return render(request, 'home.html',context = dic)

def history(request):
    cities = City.objects.all().order_by('-date_added')[ :3] 
    weather_data_list = []
    for city in cities: 
        city_name = city.city_name
        weather_data_list.append(get_weather_data(city_name))
  
    context= { 'weather_data_list': weather_data_list}
    return render(request,'history.html',context)