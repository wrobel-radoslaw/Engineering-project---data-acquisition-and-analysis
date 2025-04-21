from tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import psycopg2.extras
from psycopg2.extras import execute_batch
import csv
import os
import glob
import datetime as dt
import requests
import string
from PIL import ImageTk, Image
from steam_web_api import Steam

while True:
    print("\n")
    print(f"Welcome! Enter the number of the function you would like to use: ")
    print(f"1. Gathering Weather Data")
    print(f"2. Gathering Steam Profile Data")
    print(f"3. PostgreSQL Database with saving weather data from CSV files. Here you can also draw graphs based on certain data")
    print("\n")

    SelectFunction = input("Enter what function do you want to use: \n")

    def save_weather_data_to_csv(city, country, longitude, latitude, temp_celsius, temp_fahrenheit, humidity, wind_speed, description, sunrise_time, sunset_time):
        # Create directory if it doesn't exist
        if not os.path.exists("CSVWeatherData"):
            os.makedirs("CSVWeatherData")

        # Create a unique filename based on the current date and time
        filename = dt.datetime.now().strftime("CSVWeatherData/weather_data_%Y%m%d_%H%M%S.csv")

        # Data to be written to the CSV file
        data = [
            {"City": city, "Country": country, "Longitude": longitude, "Latitude": latitude, "Temperature (C)": temp_celsius,
            "Temperature (F)": temp_fahrenheit, "Humidity (%)": humidity, "Wind Speed (m/s)": wind_speed, "Description": description,
            "Sunrise": sunrise_time.strftime('%H:%M:%S'), "Sunset": sunset_time.strftime('%H:%M:%S')}
        ]

        # Write data to CSV file
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ["City", "Country", "Longitude", "Latitude", "Temperature (C)", "Temperature (F)", "Humidity (%)", "Wind Speed (m/s)", "Description", "Sunrise", "Sunset"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def save_steam_profile_data_to_csv(user_data):
        # Create directory if it doesn't exist
        if not os.path.exists("Steam Profile Data"):
            os.makedirs("Steam Profile Data")

        # Create a unique filename based on the current date and time, including the Steam ID
        filename = dt.datetime.now().strftime(f"Steam Profile Data/steam_profile_data_{user_data['Steam ID']}_%Y%m%d_%H%M%S.csv")

        # Making sure user's Steam ID is saved correct
        user_data["Steam ID"] = str(user_data["Steam ID"])
        user_data["Primary Clan ID"] = str(user_data["Primary Clan ID"])

        # Write data to CSV file
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in user_data.items():
                writer.writerow([key, value])
                writer.writerow([])  # Add an empty line between entries

    if SelectFunction in ["1", "Gathering", "Weather", "Weather Data", "Gathering Weather Data", "Gathering Weather", "Gathering Weather Data"]:
        # Reading API key from text file
        with open("api_key.txt", "r") as file:
            api_key = file.read().strip()

        # Creating the main window of the application
        root = Tk()
        root.title("Weather App")
        root.geometry("450x700")
        root['background'] = "#DDEEFF"  # New background color

        # Logo
        new = ImageTk.PhotoImage(Image.open('logo.png'))
        panel = Label(root, image=new)
        panel.place(x=0, y=520)

        # Date and time
        dt_now = dt.datetime.now()
        date_day = Label(root, text=dt_now.strftime('%A'), bg='#DDEEFF', font=("bold", 15))  # Day of the week
        date_day.place(x=5, y=130)  # Adjusted position
        date = Label(root, text=dt_now.strftime('%d %B %Y'), bg='#DDEEFF', font=("bold", 15))  # Date
        date.place(x=5, y=160)  # Adjusted position
        hour = Label(root, text=dt_now.strftime('%I : %M %p'), bg='#DDEEFF', font=("bold", 15))  # Time
        hour.place(x=5, y=190)  # Adjusted position

        # Switching between sun or moon icon depending on the time of day
        if 8 <= int(dt_now.strftime('%H')) <= 17:
            img = ImageTk.PhotoImage(Image.open('sun.png'))
        else:
            img = ImageTk.PhotoImage(Image.open('moon.png'))
        panel = Label(root, image=img)
        panel.place(x=300, y=75)  # Adjusted position

        # Searching for your city and weather conditions
        city_name_var = StringVar()
        city_entry = Entry(root, textvariable=city_name_var, width=45)
        city_entry.grid(row=1, column=0, ipady=10, stick=W+E+N+S)

        def kelvin_to_celsius_fahrenheit(kelvin):
            celsius = kelvin - 273.15
            fahrenheit = celsius * (9 / 5) + 32
            return celsius, fahrenheit

        def get_weather():
            try:
                # Getting weather data from API
                api_request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_entry.get()}&appid={api_key}")
                response = api_request.json()

                temp_kelvin = response['main']['temp']
                temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
                wind_speed = response['wind']['speed']
                humidity = response['main']['humidity']
                description = response['weather'][0]['description']
                local_offset = dt.timedelta(seconds=response['timezone'])

                # Using UTC to convert sunrise and sunset times
                sunrise_time = (dt.datetime.fromtimestamp(response['sys']['sunrise'], dt.timezone(local_offset))
                                .replace(tzinfo=None))
                sunset_time = (dt.datetime.fromtimestamp(response['sys']['sunset'], dt.timezone(local_offset))
                            .replace(tzinfo=None))

                # City coordinates
                longitude = response['coord']['lon']
                latitude = response['coord']['lat']

                # Country and city
                country = response['sys']['country']
                city = response['name']

                # Updating labels
                label_temp.configure(text=f"{temp_celsius:.2f}°C / {temp_fahrenheit:.2f}°F")
                label_humidity.configure(text=f"Humidity: {humidity}%")
                label_wind_speed.configure(text=f"Wind Speed: {wind_speed} m/s")
                label_description.configure(text=f"Weather: {description.capitalize()}")
                label_sunrise.configure(text=f"Sunrise: {sunrise_time.strftime('%H:%M:%S')}")
                label_sunset.configure(text=f"Sunset: {sunset_time.strftime('%H:%M:%S')}")
                label_lon.configure(text=f"{longitude}")
                label_lat.configure(text=f"{latitude}")
                label_country.configure(text=f"Country: {country}")
                label_city.configure(text=f"City: {city}")

                # Save data to CSV file
                save_weather_data_to_csv(city, country, longitude, latitude, temp_celsius, temp_fahrenheit, humidity, wind_speed, description, sunrise_time, sunset_time)
            except Exception as e:
                label_temp.configure(text="Error!")
                print("Error retrieving data:", e)

        # Search button
        city_nameButton = Button(root, text="Search", command=get_weather)
        city_nameButton.grid(row=1, column=1, padx=5, stick=W+E+N+S)

        # Labels for weather data
        label_city = Label(root, text="City: ...", bg='#DDEEFF', font=("bold", 15))
        label_city.place(x=5, y=45)
        label_country = Label(root, text="Country: ...", bg='#DDEEFF', font=("bold", 15))
        label_country.place(x=5, y=70)
        label_lon = Label(root, text="Longitude: ...", bg='#DDEEFF', font=("Helvetica", 15))
        label_lon.place(x=5, y=95)
        label_lat = Label(root, text="Latitude: ...", bg='#DDEEFF', font=("Helvetica", 15))
        label_lat.place(x=140, y=95)
        label_temp = Label(root, text="Temperature: ...", bg='#DDEEFF', font=("Helvetica", 32), fg='black')
        label_temp.place(x=10, y=235)
        label_humidity = Label(root, text="Humidity: ...", bg='#DDEEFF', font=("bold", 15))
        label_humidity.place(x=10, y=310)
        label_wind_speed = Label(root, text="Wind Speed: ...", bg='#DDEEFF', font=("bold", 15))
        label_wind_speed.place(x=10, y=340)
        label_description = Label(root, text="Weather: ...", bg='#DDEEFF', font=("bold", 15))
        label_description.place(x=10, y=370)
        label_sunrise = Label(root, text="Sunrise: ...", bg='#DDEEFF', font=("bold", 15))
        label_sunrise.place(x=10, y=400)
        label_sunset = Label(root, text="Sunset: ...", bg='#DDEEFF', font=("bold", 15))
        label_sunset.place(x=10, y=430)

        # Run the application
        root.mainloop()

    elif SelectFunction in ["2", "Steam", "Steam Data", "Gathering Steam", "Profile", "Steam Profile", "Steam Profile Data", "Gathering Steam Profile Data", "Gathering Steam Profile"]:
        os.environ["STEAM_API_KEY"] = "F99DAE5FCBC5B6A41CC50A5F5109DA58"

        KEY = os.environ.get("STEAM_API_KEY")

        if KEY is None:
            raise ValueError("Please set the STEAM_API_KEY environment variable")

        steam = Steam(KEY)

        print("Please give your Steam profile ID:")
        ProfileID = input("Steam ID: ")

        # Check if the `ProfileID` contains only numbers
        if (ProfileID.isdigit() and len(ProfileID) == 17):
            user = steam.users.get_user_details(ProfileID)
            print(user)
        else:
            print("Invalid input. Please check if your Steam ID contains only numbers and it's 17 digits long.")

            user_data = {
                "Steam ID": str(user['player']['steamid']),
                "Community Visibility State": user['player']['communityvisibilitystate'],
                "Profile State": user['player']['profilestate'],
                "Persona Name": user['player']['personaname'],
                "Profile URL": user['player']['profileurl'],
                "Avatar URL": user['player']['avatar'],
                "Avatar Medium URL": user['player']['avatarmedium'],
                "Avatar Full URL": user['player']['avatarfull'],
                "Avatar Hash": user['player']['avatarhash'],
                "Last Logoff": user['player'].get('lastlogoff', 'N/A'),  # Use .get() to avoid KeyError
                "Persona State": user['player']['personastate'],
                "Primary Clan ID": str(user['player']['primaryclanid']),
                "Time Created": user['player']['timecreated'],
                "Persona State Flags": user['player']['personastateflags']
            }
            
            # Saving Steam Profile ID to database
            if not os.path.exists("Steam Profile Database"):
                os.makedirs("Steam Profile Database")
            with open("Steam Profile Database/steam_ids.txt", "a") as SteamID_Database:
                SteamID_Database.write(personaname + " " + ProfileID + "\n")
            
            SavingData = input("Do you want to save all the data to a CSV file? Type Yes/No \n").strip().lower()
            if SavingData in ["yes", "y", "ye"]:
                # Save Steam profile data to CSV file
                save_steam_profile_data_to_csv(user_data)

                # Opening text file in write mode
                with open("user_details.txt", "w") as file:
                    # Information about the source
                    file.write("Source: Steam Web API documentation - https://developer.valvesoftware.com/wiki/Steam_Web_API\n\n")
                    
                    # Saving data to a text file
                    for key, value in user_data.items():
                        file.write(f"{key}: {value}\n")

                print("User data has been saved in a text file. Check steam_profile_data in your Steam Profile Data catalog.")

    elif SelectFunction in ["3", "PostgreSQL", "Database", "PostgreSQL Database", "PostgreSQL Database with saving weather data from CSV files"]:

        
        # PostgreSQL connection details
        hostname = 'localhost'
        database = 'engineeringproject'
        username = 'postgres'
        pwd = 'admin'
        port_id = 5432

        # Path to the folder containing CSV files
        csv_folder = r"C:\Users\radek\Documents\GitHub\Engineering-project---data-acquisition-and-analysis\CSVWeatherData"

        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                host=hostname,
                database=database,
                user=username,
                password=pwd,
                port=port_id
            )
            cursor = conn.cursor()

            print("*** Connected to the PostgreSQL database. ***")
            print("Hello! You're automaticly connected to the PostgreSQL database.")
            print("1. Create a graph based on the data from the database")
            print("2. Save data from CSV files to the database\n")

            SelectFunction = input("Enter what function do you want to use: ")
            
            if SelectFunction in ["1", "Create", "Create a graph", "Create graph", "Graph"]:
                figure = plt.figure()
                axes = figure.add_subplot(1, 1, 1)
                plt.show()

            elif SelectFunction in ["2", "Save", "Save data", "Save data to database", "Save data to PostgreSQL"]:
                # Recreate the weatherdata table
                delete_table_query = "DROP TABLE IF EXISTS weatherdata;"
                cursor.execute(delete_table_query)

                # Create the weatherdata table if it does not exist
                create_table_query = '''
                CREATE TABLE IF NOT EXISTS weatherdata (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(50) NOT NULL,
                    country VARCHAR(50) NOT NULL,
                    longitude DOUBLE PRECISION NOT NULL,
                    latitude DOUBLE PRECISION NOT NULL,
                    temperature_celsius DOUBLE PRECISION NOT NULL,
                    temperature_fahrenheit DOUBLE PRECISION NOT NULL,
                    humidity INTEGER NOT NULL,
                    wind_speed DOUBLE PRECISION NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    sunrise_time TIME NOT NULL,
                    sunset_time TIME NOT NULL
                );
                '''
                cursor.execute(create_table_query)
                conn.commit()

                # Retrieve all CSV files from the specified folder
                csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))

                # Iterate through each CSV file
                for file in csv_files:
                    print(f"Processing file: {os.path.basename(file)}")

                    with open(file, 'r', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        headers = next(reader)  # Skip the header row

                        # Prepare data for batch insertion
                        data = []
                        for row in reader:
                            try:
                                data.append((
                                    row[0],  # City
                                    row[1],  # Country
                                    float(row[2]),  # Longitude
                                    float(row[3]),  # Latitude
                                    float(row[4]),  # Temperature (C)
                                    float(row[5]),  # Temperature (F)
                                    int(row[6]),  # Humidity (%)
                                    float(row[7]),  # Wind Speed (m/s)
                                    row[8],  # Description
                                    row[9],  # Sunrise (HH:MM:SS)
                                    row[10]  # Sunset (HH:MM:SS)
                                ))
                            except Exception as e:
                                print(f"Error processing row: {row}. Details: {e}")

                        # Insert data into the table using execute_batch for efficiency
                        insert_query = '''
                        INSERT INTO weatherdata (
                            city, country, longitude, latitude, temperature_celsius,
                            temperature_fahrenheit, humidity, wind_speed, description,
                            sunrise_time, sunset_time
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        '''
                        try:
                            execute_batch(cursor, insert_query, data)
                            conn.commit()
                            print(f"Inserted {len(data)} records from file {os.path.basename(file)}")
                        except Exception as e:
                            print(f"Error inserting data from file {os.path.basename(file)}. Details: {e}")
                            conn.rollback()

        except Exception as error:
            print(f"Error while working with the database: {error}")
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
            print("*** PostgreSQL connection has been closed. ***\n")

    else:

        print("Wrong input!")