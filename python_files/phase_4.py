import requests
import os
import sqlite3

def retrieve_data():

    try:
        # Input Validation
    
        latitude = float(input("Please enter cities latitude: "))
        longitude = float(input("Please enter cities longitude: "))
        country = input("Please enter country name: ")
        country = country.title()
        city = input("Please enter city name: ")
        city = city.title()
        timezone = input("Please enter city's timezone: ")
        timezone = timezone.title()
        start_date = input("Please enter a start date: ")
        end_date = input("Please enter a end date: ")

        #API Request
  
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
	    "latitude": {latitude},
	    "longitude": {longitude},
	    "start_date": {start_date},
	    "end_date": {end_date},        
	    "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "precipitation_hours"]
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        daily = response.json()
        date = daily['daily']['time']
        max_temp = daily['daily']['temperature_2m_max']
        min_temp = daily['daily']['temperature_2m_min']
        mean_temp = daily['daily']['temperature_2m_mean']
        precipitation = daily['daily']['precipitation_hours']
        

        # Connect to database
        with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connect:

            connect.row_factory = sqlite3.Row

            cursor = connect.cursor()

            # To confirm the country does't exist already in the database before inserting
            cursor.execute("SELECT COUNT(*) FROM countries WHERE name = ?", (country,))
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute(f"""
                    INSERT INTO countries (name, timezone) VALUES ('{country}', '{timezone}');                
                """)

            # To confirm city name does not exist in the database before inserting query
            cursor.execute("SELECT COUNT(*) FROM cities WHERE name = ?", (city,))
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute(f"""
                    INSERT INTO cities (name, longitude, latitude, country_id) VALUES ('{city}', {latitude}, {longitude}, 
                    (SELECT id FROM countries WHERE name = '{country}'))
                """)
            # To insert into daily_weather_entires
            for date_value, max_temp_value, min_temp_value, mean_temp_value, precipitation_value in zip(date, max_temp, min_temp, mean_temp, precipitation):
                # Check if the date already exists for the given city
                cursor.execute("""
                    SELECT COUNT(*) FROM daily_weather_entries 
                    WHERE date = ? AND city_id = (SELECT id FROM cities WHERE name = ?)
                """, (date_value, city))

                count = cursor.fetchone()[0]

                if count == 0:
                    # if date does not exist, insert the record
                    cursor.execute("""
                        INSERT INTO daily_weather_entries(date, max_temp, min_temp, mean_temp, precipitation, city_id)
                        VALUES (?, ?, ?, ?, ?, (SELECT id FROM cities WHERE name = ?))
                    """, (date_value, max_temp_value, min_temp_value, mean_temp_value, precipitation_value, city))
                    
                else:
                    print(f"Record for date {date_value} already exists for {city} city")
            print(f"Successfully added {city} city and it's weather records from {start_date} to {end_date} to the database")        
            connect.commit()
           
    except Exception as e:
        print(f"An error occurred: {e}")



# Change the CWD to the path where this script is located

if __name__ == "__main__":
    PATH_TO_THIS_FILE = os.path.dirname(__file__)
    os.chdir(PATH_TO_THIS_FILE)

    print("CURRENT WORKING DIRECTORY: ", os.getcwd())

    retrieve_data()

    


