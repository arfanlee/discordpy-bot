import requests
import json

def theweather(location):
    api = '0aab15441d83eb3e03c3805d4cc199d2'
    url = 'OPENWEATHER_API'

    answer = url + location + '&appid=' + api + '&units=metric'
    response = requests.get(answer)
    res = response.json()
    return res
