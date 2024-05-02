from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9b5aed08029255f403e4bf3f0e1cca5a'
    cities = City.objects.all()
    weather_data = []

    if request.method == 'POST': 
        form = CityForm(request.POST) 
        if form.is_valid(): 
            form.save() 

    form = CityForm() 
    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city': city.name,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form} 
    return render(request, 'my_weather/index.html', context)
