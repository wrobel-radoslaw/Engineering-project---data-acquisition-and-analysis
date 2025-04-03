insert = (
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
                    row[10],  # Sunset (HH:MM:SS)
                )

                insert_query = """
                INSERT INTO weatherdata (
                    city, country, longitude, latitude, temperature_celsius,
                    temperature_fahrenheit, humidity, wind_speed, description,
                    sunrise_time, sunset_time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                print("insert query", insert_query)
                
                try:
                    print(cursor.mogrify(insert_query, insert).decode("utf-8"))  # Debugging query                    cursor.execute(insert_query, insert)
                    cursor.execute(insert_query, insert)
                    conn.commit()
                except Exception as e:
                    print("Error inserting data:", e)