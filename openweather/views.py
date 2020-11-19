from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
import requests, json


def index(request):
    return render(request, 'index.html')


def weather_request(request):
    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
    API_KEY = "b961143ab8e3f05bbf2551186b15f4d3"

    city = request.POST.get('city')
    period = request.POST.get('period')

    URL = BASE_URL + "q=" + city + "&units=metric&cnt=" + period + "&lang=en" + "&appid=" + API_KEY

    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        list_weather = data['list']
        tem_min = []
        tem_max = []
        temp = []
        humidity = []
        tem_median = []
        for i in range(len(list_weather)):
            temp.append(list_weather[i]['main']['temp'])
            tem_min.append(list_weather[i]['main']['temp_min'])
            tem_max.append(list_weather[i]['main']['temp_max'])
            humidity.append(list_weather[i]['main']['humidity'])
            median = (list_weather[i]['main']['temp_min'] + list_weather[i]['main']['temp_max']) / 2
            tem_median.append(median)
        context = {
            'temp': temp,
            'tem_min': tem_min,
            'tem_max': tem_max,
            'tem_median': tem_median,
            'humidity': humidity,
        }
    else:
        # showing the error message
        print("Error in the HTTP request")

    return render(request, 'index.html', context=context)
