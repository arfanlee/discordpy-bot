import requests

def theweather(location):
    api = 'API_KEY'
    url = 'OPENWEATHER_API'

    answer = url + location + '&appid=' + api + '&units=metric'
    response = requests.get(answer)
    res = response.json()
    return res
