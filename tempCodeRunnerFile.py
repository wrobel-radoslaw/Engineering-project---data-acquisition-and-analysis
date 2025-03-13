    if not os.path.exists("Steam Profile Database"):
        os.makedirs("Steam Profile Database")
    with open("Steam Profile Database/steam_ids.txt", "a") as SteamID_Database:
        SteamID_Database.write(ProfileID + "\n")