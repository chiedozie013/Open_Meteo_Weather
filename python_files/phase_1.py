# Author: <Your name here>
'''
James, Chiedozie
'''

# Student ID: <Your Student ID>
'''
d3458961
'''

import sqlite3


# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory
'''

def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        # Configures the database to return sqlite3 Rows when queried.
        connection.row_factory = sqlite3.Row

        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Commits changes to the database.
        connection.commit()

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")
        
        
    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities(connection):
    # TODO: Implement this function
    try:
        # Configures the database to return sqlite3 Rows when queried.
        connection.row_factory = sqlite3.Row

        # Define the query
        query = "SELECT * from [cities]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Commits changes to the database.
        connection.commit()

        # Iterate over the results and display the results.
        for row in results:
            #row_list = list(row)
            #print(row_list)
            print(f"City Id: {row['id']} ----- City Name: {row['name']} ----- City longitude: {row['longitude']} ----- City latitude: {row['longitude']} ----- Country_id: {row['country_id']}")

       

    except sqlite3.OperationalError as ex:
        print(ex)
    pass

'''
Good
'''
def average_annual_temperature(connection, city_id, year):
    # TODO: Implement this function
    try:
        # Configures the database to return sqlite3 Rows when queried.
        connection.row_factory = sqlite3.Row

        # Define the query
        query = f"SELECT ROUND(avg(mean_temp), 2) AS avg_mean_temp FROM daily_weather_entries WHERE city_id = {city_id} and date BETWEEN '{year}-01-01' and '{year}-12-31'"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Commits changes to the database.
        connection.commit()

        # Iterate over the results and display the results.
        for row in results:
            print(f"Average Annual Temperature for city with ID {city_id} in year {year} is {row[0]}")

        

    except sqlite3.OperationalError as ex:
        print(ex)
    pass

def average_seven_day_precipitation(connection, city_id, start_date):
    # TODO: Implement this function
    try:
        # Configures the database to return sqlite3 Rows when queried.
        connection.row_factory = sqlite3.Row

        # Define the query
        query = f"SELECT ROUND(AVG(precipitation), 2) AS average_precipitation FROM daily_weather_entries WHERE city_id = {city_id} and date BETWEEN '{start_date}' AND DATE('{start_date}', '+6 days')"
        
        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Commits changes to the database.
        connection.commit()

        # Iterate over the results and display the results.
        for row in results:
            print(f"Average Seven Day Precipitation for city with ID {city_id} from {start_date} is {row[0]}")

            
    except sqlite3.OperationalError as ex:
        print(ex)

    pass

'''
Very good
'''
def average_mean_temp_by_city(connection, city_id, date_from, date_to):
    # TODO: Implement this function
    try:
        # Configures the database to return sqlite3 Rows when queried.
        connection.row_factory = sqlite3.Row

        # Define the query
        
        query = f"SELECT ROUND(AVG(mean_temp), 2) AS average_mean_temp FROM daily_weather_entries WHERE city_id = {city_id} and date BETWEEN '{date_from}' AND ('{date_to}')"
        
        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Commits changes to the database.
        connection.commit()

        # Iterate over the results and display the results.
        for row in results:
            print(f"The average mean temperature from {date_from} to {date_to} for city with ID {city_id} is {row[0]}")

            
    except sqlite3.OperationalError as ex:
        print(ex)

    pass

def average_annual_precipitation_by_country(connection, year):
    # TODO: Implement this function
    try:
        # Configures the database to return sqlite3 Rows when queried.
        connection.row_factory = sqlite3.Row

        # Define the query
        
        query = f"""
            
            SELECT countries.name, 
            ROUND(avg(daily_weather_entries.precipitation), 2) AS average_precipitation
            FROM daily_weather_entries
            JOIN cities ON daily_weather_entries.city_id = cities.id
            JOIN countries ON cities.country_id = countries.id            
            WHERE daily_weather_entries.date BETWEEN '{year}-01-01' AND '{year}-12-31'
            GROUP BY countries.name
                     
        """
        
        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Commits changes to the database.
        connection.commit()

        # Iterate over the results and display the results.
        for row in results:
            print(f"The average precipitation of {row[0]} in the year {year} is {row[1]}")

            
    except sqlite3.OperationalError as ex:
        print(ex)
    pass

'''
Excellent

You have gone beyond the basic requirements for this aspect.

'''

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    with sqlite3.connect("db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        print("Output for select_all_countries function")
        select_all_countries(connection)
        print()
        print("Output for select_all_cities function")
        select_all_cities(connection)
        print()
        print("Output for average annual temperature of a given city ID and year")
        city_id = int(input("Please enter a city_id: "))
        year = int(input("Please enter a year from 2000 to 2022: ")) 
        average_annual_temperature(connection, city_id, year)
        print()
        print("Output for average seven day precipitation of a given city ID and start date")
        city_id = int(input("Please enter a city ID: "))
        start_date = input("Please enter a start date in this format(yyyy-mm-dd): ")        
        average_seven_day_precipitation(connection, city_id, start_date)
        print()
        print("Output for average mean temperature of a given city ID from a start date to an end date")
        city_id = int(input("Please enter the city_id: "))
        date_from = input("Please enter a start date in this format(yyyy-mm-dd): ")
        date_to = input("Please enter an end date in this format(yyyy-mm-dd): ")
        average_mean_temp_by_city(connection, city_id, date_from, date_to)
        print()
        print("Output for average precitipation of a given country and year")
        year = input("Please enter a year from 2000 to 2022: ")
        average_annual_precipitation_by_country(connection, year)
        