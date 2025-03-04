import os
from steam_web_api import Steam
from decouple import config

os.environ["STEAM_API_KEY"] = "F99DAE5FCBC5B6A41CC50A5F5109DA58"

KEY = os.environ.get("STEAM_API_KEY")

if KEY is None:
    raise ValueError("Please set the STEAM_API_KEY environment variable")

steam = Steam(KEY)

# arguments: steamid
user = steam.users.get_user_details("76561198302458528")
print(user)

user_data = {
    "Steam ID": user['player']['steamid'],
    "Community Visibility State": user['player']['communityvisibilitystate'],
    "Profile State": user['player']['profilestate'],
    "Persona Name": user['player']['personaname'],
    "Profile URL": user['player']['profileurl'],
    "Avatar URL": user['player']['avatar'],
    "Avatar Medium URL": user['player']['avatarmedium'],
    "Avatar Full URL": user['player']['avatarfull'],
    "Avatar Hash": user['player']['avatarhash'],
    "Last Logoff": user['player']['lastlogoff'],
    "Persona State": user['player']['personastate'],
    "Primary Clan ID": user['player']['primaryclanid'],
    "Time Created": user['player']['timecreated'],
    "Persona State Flags": user['player']['personastateflags']
}

#Opening text file in write mode
with open("user_details.txt", "w") as file:
    # Dodajemy informację o źródle
    file.write("Source: Steam Web API documentation - https://developer.valvesoftware.com/wiki/Steam_Web_API\n\n")
    
    #Saving data to a text file
    for key, value in user_data.items():
        file.write(f"{key}: {value}\n")

print("User data has been saved in a text file. Check user_details.txt")