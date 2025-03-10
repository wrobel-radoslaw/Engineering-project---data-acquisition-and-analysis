import os
import datetime as dt
import requests
from steam_web_api import Steam

# Weather API Data Analysis

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open('api_key.txt', 'r').read()
CITY = "Nawsie Brzosteckie"


#Converting Kelvin to Celsius & Fahrenheit
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius* (9/5) + 32
    return celsius, fahrenheit

url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
response = requests.get(url).json()

temp_kelvin = response['main']['temp']
temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
wind_speed = response['wind']['speed']
humidity = response['main']['humidity']
description = response['weather'][0]['description']
sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

print(f"Temperature in {CITY}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
print(f"Temperature in {CITY} feels like: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F")
print(f"Humidity in {CITY}: {humidity}%")
print(f"Wind Speed in {CITY}: {wind_speed}m/s")
print(f"General Weather in {CITY}: {description}")
print(f"Sun rises in {CITY} at: {sunrise_time} local time.")
print(f"Sun sets in {CITY} at: {sunset_time} local time.")


# os.environ["STEAM_API_KEY"] = "F99DAE5FCBC5B6A41CC50A5F5109DA58"

# KEY = os.environ.get("STEAM_API_KEY")

# if KEY is None:
#     raise ValueError("Please set the STEAM_API_KEY environment variable")

# steam = Steam(KEY)

# # arguments: steamid
# user = steam.users.get_user_details("76561198302458528")
# print(user)

# user_data = {
#     "Steam ID": user['player']['steamid'],
#     "Community Visibility State": user['player']['communityvisibilitystate'],
#     "Profile State": user['player']['profilestate'],
#     "Persona Name": user['player']['personaname'],
#     "Profile URL": user['player']['profileurl'],
#     "Avatar URL": user['player']['avatar'],
#     "Avatar Medium URL": user['player']['avatarmedium'],
#     "Avatar Full URL": user['player']['avatarfull'],
#     "Avatar Hash": user['player']['avatarhash'],
#     "Last Logoff": user['player']['lastlogoff'],
#     "Persona State": user['player']['personastate'],
#     "Primary Clan ID": user['player']['primaryclanid'],
#     "Time Created": user['player']['timecreated'],
#     "Persona State Flags": user['player']['personastateflags']
# }

# #Opening text file in write mode
# with open("user_details.txt", "w") as file:
#     #Information about the source
#     file.write("Source: Steam Web API documentation - https://developer.valvesoftware.com/wiki/Steam_Web_API\n\n")
    
#     #Saving data to a text file
#     for key, value in user_data.items():
#         file.write(f"{key}: {value}\n")

# print("User data has been saved in a text file. Check user_details.txt")