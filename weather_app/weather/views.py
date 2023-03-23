import requests
from django.shortcuts import render
from django.urls import path
from datetime import datetime

"""def weather_view(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        if city:
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=d06bb9bbce9501b66bfa5677e0f2c865&units=metric'.format(city)
            timeout=10
            response = requests.get(url,timeout=timeout)
            data = response.json()
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            weather_description = data['weather'][0]['description']
            return render(request, 'weather.html', {'city': city, 'temperature': temperature,
                                                    'humidity': humidity, 'wind_speed': wind_speed,
                                                    'weather_description': weather_description})
    return render(request, 'weather.html')"""

def mys(time):
        format_data = "%Y-%m-%d %H:%M:%S"  
        x = datetime.strptime(time, format_data)
        return x.hour

def fillterr(e):
    if mys(e['dt_txt'])==15:
        return True
    else:
        return False
    
def getDateOnly(time):
    format_data = "%Y-%m-%d %H:%M:%S"  
    x = datetime.strptime(time, format_data)
    return x.date()
def weather_view(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        if city:
            try:
                url_lat = 'https://api.openweathermap.org/geo/1.0/direct?q='+city+'&limit=1&appid=d06bb9bbce9501b66bfa5677e0f2c865'
                response_lat = requests.get(url_lat, timeout=5)
                response_lat.raise_for_status()  # raise exception if response status code is not 200
                data_lat = response_lat.json()
                if(len(data_lat)>0):
                  data_lat=data_lat[0]
                else:
                   message="Something went wrong"
                   return render(request, 'weather.html', {'error': message})
                try:
                   url='http://api.openweathermap.org/data/2.5/forecast?lat='+str(data_lat['lat'])+'&lon='+str(data_lat['lon'])+'&appid=d06bb9bbce9501b66bfa5677e0f2c865&units=metric'
      
                   response = requests.get(url, timeout=5)
                   response.raise_for_status()  # raise exception if response status code is not 200
                   data = response.json()
                   allweather=data['list']
                   newArr=filter(fillterr, allweather)

                   return render(request, 'weather.html', {'aaall':newArr,'city':city})
                except:                                      #   'city': city, 'temperature': temperature,
                  message="Something went wrong"
                  return render(request, 'weather.html', {'error': message})
            except requests.exceptions.Timeout:
                message = "The request to the OpenWeatherMap API timed out. Please try again later."
                return render(request, 'weather.html', {'error': message})
            except requests.exceptions.HTTPError:
                message = "The request to the OpenWeatherMap API returned an error. Please check your input and try again."
                return render(request, 'weather.html', {'error': message})
            except requests.exceptions.FileNotFoundError:
                message = "No City found"
                return render(request, 'weather.html', {'error': message})
            except:
                message="Something went wrong"
                return render(request, 'weather.html', {'error': message})
    return render(request, 'weather.html')   
