from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.views import APIView
import requests, json


class WeatherApiView(APIView):

    def get(self, request, *args, **kwargs):
        city = kwargs.get('city', None)
        period = kwargs.get('period', None)
        BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
        API_KEY = "b961143ab8e3f05bbf2551186b15f4d3"

        URL = BASE_URL + "q=" + city + "&units=metric&cnt=" + period + "&lang=en" + "&appid=" + API_KEY

        response = requests.get(URL)
        # checking the status code of the request
        if response.status_code == 200:
            # getting data in the json format
            data = response.json()
            # getting the main dict block
            list_weather = data['list']
            temperature_data = {}
            for i in range(len(list_weather)):
                median = (list_weather[i]['main']['temp_min'] + list_weather[i]['main']['temp_max']) / 2
                temperature_data[i + 1] = {"temperature": list_weather[i]['main']['temp'],
                                           "min_temperature": list_weather[i]['main']['temp_min'],
                                           "max_temperature": list_weather[i]['main']['temp_max'],
                                           "median_temperature": median,
                                           "humidity": list_weather[i]['main']['humidity'],
                                           }
            return HttpResponse(json.dumps(temperature_data), content_type="application/json")

        else:
            # showing the error message
            return HttpResponseNotFound('<h1>City ' + city + ' doesnt exist</h1>')
