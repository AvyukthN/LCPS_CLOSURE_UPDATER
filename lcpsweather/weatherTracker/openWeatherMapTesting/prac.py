import requests

"""
x = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Ashburn&appid=1b22987782bbf4121610cdb4b60b3faa')

weatherjson = x.json()
print(weatherjson)

wind = weatherjson['wind']
coords = weatherjson['coord']
looks = weatherjson['weather'][0]
numbers = weatherjson['main']

main = looks['main']
desc = looks['description']

temp = numbers['temp']
feels_like = numbers['feels_like']
mint = numbers['temp_min']
minm = numbers['temp_max']
pressure = numbers['pressure']
humidity = numbers['humidity']

windspeed = wind['speed']
winddirection = wind['deg']
windgust = wind['gust']

print("Looks: " + main)
print("Description: " + desc)
print("Temperature: " + str(temp))
print("Feels Like: " + str(feels_like))
print("Minimum Temperature: " + str(mint))
print("Minimum Temperature: " + str(mint))
print("Pressure: " + str(pressure))
print("Humidity: " + str(humidity))
print("Wind Speed: " + str(windspeed) + " mph")
print("Wind Direction: " + str(winddirection) + " degrees")
print("Wind Gust Force: " + str(windgust))"""

key = '1b22987782bbf4121610cdb4b60b3faa'

x = requests.get('https://tile.openweathermap.org/map/{}/{}/{}/{}.png?appid={}'.format('precipitation_new', 3, 10, 10, key))

string = bytes(x.text, 'jpg')

with open("img.png", "wb") as f:
    f.write(x)


"""weatherjson = x.json()

for diction in weatherjson:
    print(diction)

hourly = weatherjson['hourly']
print(hourly[1])"""