import os
import json
import requests

metrics = {}

def update_metrics(url, status_code):
    if url not in metrics:
        metrics[url] = dict()

    if 'status' not in metrics[url]:
        metrics[url]['status'] = dict()

    if status_code in metrics[url]['status']:
        metrics[url]['status'][status_code] += 1

    else:
        metrics[url]['status'].update({status_code: 1})


def get_ip_address():
    url = "https://api.ipify.org?format=json"
    response = requests.request("GET", url)

    if response.status_code is 200:
        ip_address = json.loads(response.content)

        update_metrics("https://api.ipify.org", response.status_code)
        return ip_address['ip'], ''

    update_metrics("https://api.ipify.org", response.status_code)
    return None, 'API returned status_code: {}'.format(response.status_code)


def get_info(ip_address):
    api_key = os.getenv("IP_FINDER_API")
    url = "http://api.ipstack.com/{}?access_key={}".format(ip_address, api_key)
    response = requests.request("GET", url)

    if response.status_code is 200:
        info = json.loads(response.content)
        if 'success' in info and not info['success']:
            update_metrics("http://api.ipstack.com", response.status_code)
            return None, info['error']['info']

        update_metrics("http://api.ipstack.com", response.status_code)
        return info, ''

    update_metrics("http://api.ipstack.com", response.status_code)
    return None, 'API returned {}'.format(response.status_code)


def get_max(object):
    max_object_count = 0
    max_object = ""
    for url in object:
        current_count = object.count(url)
        if current_count > max_object_count:
            max_object = url
            max_object_count = current_count

    return max_object


def get_weather_data(weather_info):
    weather = []
    for day in weather_info['data']['weather']:
        astronomy = day['astronomy'][0]

        temp = {
            "date": day['date'],
            "sunrise": astronomy['sunrise'],
            "sunset": astronomy['sunset'],
            "moon_phase": astronomy['moon_phase'],
            "max_temp": day['maxtempC'],
            "min_temp": day['mintempC'],
            "avg_temp": day['avgtempC'],
            "total_snow": day['totalSnow_cm'],
            "precipitations": 0,
            "humidity": 0,
            "visibility": 0,
            "feels_like": 0,
            "chance_of_rain": 0,
            "wind_speed": 0,
            "descriptions": {
                "url": [],
                "conditions": []
            }
        }

        for hour in day['hourly']:
            temp['precipitations'] += float(hour['precipMM'])
            temp['humidity'] += float(hour['humidity'])
            temp['visibility'] += float(hour['visibility'])
            temp['feels_like'] += float(hour['FeelsLikeC'])
            temp['chance_of_rain'] += float(hour['chanceofrain'])
            temp['wind_speed'] += float(hour['windspeedKmph'])
            temp['descriptions']['url'].append(hour['weatherIconUrl'][0]['value'])
            temp['descriptions']['conditions'].append(hour['weatherDesc'][0]['value'])

        length = len(day['hourly'])
        temp['precipitations'] = round(temp['precipitations'] / length, 2)
        temp['humidity'] = temp['humidity'] / length
        temp['visibility'] = temp['visibility'] / length
        temp['feels_like'] = temp['feels_like'] / length
        temp['chance_of_rain'] = temp['chance_of_rain'] / length
        temp['wind_speed'] = temp['wind_speed'] / length

        temp["descriptions"]['url'] = get_max(temp["descriptions"]['url'])
        temp["descriptions"]["conditions"] = get_max(temp["descriptions"]['conditions'])

        weather.append(temp)

    return weather
