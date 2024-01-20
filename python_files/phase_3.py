import os
import sqlite3
import phase_1
import phase_2
import phase_4


def deleteCity(connection):
    city_name = input("Enter the city name to delete: ")
    city_name = city_name.title()
    confirm = input(f"Confirm you want to delete {city_name} from the database (Yes/No): ")
    if  confirm.title() == "Yes":
        try:
            cursor = connection.cursor()

            # Check if the city exists before attempting to delete
            cursor.execute("SELECT COUNT(*) FROM cities WHERE name = ?", (city_name,))
            count = cursor.fetchone()[0]

            if count > 0:
                # City exists, so delete related records in daily_weather_entries
                cursor.executescript(f"""
                    DELETE FROM daily_weather_entries WHERE city_id = (SELECT id FROM cities WHERE name = '{city_name}');
                    DELETE FROM cities WHERE name = '{city_name}';
                """)
                
                print(f"City {city_name} and its entries deleted successfully.")
            else:
                print(f"City {city_name} not found in the database.")

            connection.commit()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Bye")

def deleteCountry(connection):    
    country_name = input("Enter the country name to delete: ")
    country_name = country_name.title()
    confirm = input(f"Confirm you want to delete {country_name} from the database (Yes/No): ")
    if  confirm.title() == "Yes":
        try:
                cursor = connection.cursor()

                # Check if the country exists before attempting to delete
                cursor.execute("SELECT id FROM countries WHERE name = ?", (country_name,))
                country_id = cursor.fetchone()

                if country_id:             

                    
                    # Delete related daily_weather_entries
                    cursor.execute("DELETE FROM daily_weather_entries WHERE city_id IN (SELECT id FROM cities WHERE country_id = ?)", country_id)

                    # Delete related cities
                    cursor.execute("DELETE FROM cities WHERE country_id = ?", country_id)

                    # Finally, delete the country
                    cursor.execute("DELETE FROM countries WHERE id = ?", country_id)                
                    
                    print(f"Country {country_name} and its related cities and entries deleted successfully.")
                else:
                    print(f"Country {country_name} not found in the database.")

                connection.commit()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Bye")


def delete_entire_record(connection):
    confirm = input(f"Confirm you want to drop the database (Yes/No): ")
    if  confirm.title() == "Yes":
        try:
            cursor = connection.cursor()

                # Disable foreign key constraints temporarily for easier deletion
            cursor.execute("PRAGMA foreign_keys = OFF;")

                # Get a list of all tables in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                cursor.execute(f"DELETE FROM {table_name};")
                print(f"All data deleted from table: {table_name}")

                # Re-enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = ON;")

            print("All data deleted from the database.")

            connection.commit()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Bye")


def userInterface(connection):
    while True:
        print()
        print("Please choose desired query number from the list of numbers below")
        print()
        print("Phase 1")
        print("1. Prints all countries")
        print("2. Prints all cities")
        print("3. Prints average annual temperature of a given city ID and year")
        print("4. Prints average seven day precipitation of a given city ID and start date")
        print("5. Prints average mean temperature of a given city ID from a start date to an end date")
        print("6. Prints average annual precipitation of a given country and year")
        print("Phase 2")
        print("7. Generate bar chart to show the 7-day precipitation for a specific town/city")
        print("8. Generates bar chart for all cities in a particular year")
        print("9. Generate bar chat that shows the average yearly precipitation by country")
        print("10. Generates grouped bar chats for displaying the min, max, mean temperature and precipitation")
        print("11. Generates multi-line charts to show the daily minimum and maximum temperature for a given month for a specific city")
        print("12. Generates a scatter plot of temperatures over rainfall for a particular city and month")
        print("13. Deletes records from SQLite3 database")        
        print("14. To retrieve data from the API and insert data into the SQLite3 database " )
        print("quit to exit")
        print()

        user_input = input("What query would you like to perform:  ")

        if user_input == "1":
            phase_1.select_all_countries(connection)
        elif user_input == "2":
            phase_1.select_all_cities(connection)
        elif user_input == "3":
            city_id = int(input("Please enter a city_id: "))
            year = int(input("Please enter a year from 2000 to 2022: "))
            phase_1.average_annual_temperature(connection, city_id, year)
        elif user_input == "4":
            city_id = int(input("Please enter a city ID: "))
            date = input("Please enter start date in this format(yyyy-mm-dd): ")
            phase_1.average_seven_day_precipitation(connection, city_id, date)
        elif user_input == "5":
            city_id = input("Plase enter a city ID: ")
            date_from = input("Please enter a start date in this format(yyyy-mm-dd): ")
            date_to = input("Please enter an end date in this format(yyyy-mm-dd): ")
            phase_1.average_mean_temp_by_city(connection, city_id, date_from, date_to)
        elif user_input == "6":
            year = input("Please enter a year from 2000 to 2022: ")
            phase_1.average_annual_precipitation_by_country(connection, year)
        elif user_input == "7":
            city_name = input("Please enter a city name: ")
            city_name = city_name.title()
            start_date = input("Please enter a start date(yyyy-mm-dd): ")
            query = f"""
                    SELECT date, precipitation FROM [daily_weather_entries]
                    JOIN cities On daily_weather_entries.city_id = cities.id 
                    WHERE cities.name = '{city_name}' and date BETWEEN '{start_date}' AND DATE('{start_date}', '+6 days')
                """
            phase_2.plot_7_day_precipitation(query, city_name, start_date)

        elif user_input == "8":
           year = input("Please enter desired year: ")
           query = f""" 
                    SELECT
                    cities.name AS city_name,   
                    ROUND(AVG(daily_weather_entries.max_temp), 2) AS avg_max_temp
                    FROM cities
                    JOIN daily_weather_entries ON cities.id = daily_weather_entries.city_id
                    WHERE strftime('%Y', daily_weather_entries.date) = '{year}'
                    GROUP BY cities.name
                    ORDER BY city_name
                """
           phase_2.avg_annual_temp(query, year)
        elif user_input == "9":
            country_name = input("Please enter a country name: ")
            country_name = country_name.title()
            query = f"""
                SELECT
                strftime('%Y', daily_weather_entries.date) AS year,
                ROUND(AVG(daily_weather_entries.precipitation), 2) AS avg_precipitation
                FROM daily_weather_entries
                JOIN cities ON daily_weather_entries.city_id = cities.id
                JOIN countries ON cities.country_id = countries.id
                WHERE countries.name = '{country_name}' AND daily_weather_entries.date BETWEEN '2000-01-01' AND '2022-12-31'
                GROUP BY year
                ORDER BY year;
            """
            phase_2.average_yearly_precipitation(query, country_name)

        elif user_input == "10":
            date = input("Please enter a date (yyyy-mm-dd): ")
            query = f"""
                SELECT cities.name, min_temp, max_temp, mean_temp, precipitation
                FROM daily_weather_entries
                JOIN cities ON daily_weather_entries.city_id == cities.id
                WHERE date = '{date}'
                GROUP BY city_id
            """
            phase_2.group_bar_chat(query, date)

        elif user_input == "11":
            city_name = input("Please enter a city name: ")
            city_name = city_name.title()
            date = input("Please enter the year and month (yyyy-mm): ")
            query = f"""
                SELECT date, min_temp, max_temp
                FROM daily_weather_entries
                JOIN cities On daily_weather_entries.city_id = cities.id
                WHERE cities.name = '{city_name}' AND strftime('%Y-%m', date) = '{date}' 
            """
            phase_2.multi_line(query, city_name, date)

        elif user_input == "12":
            year = input("Please enter chosen year(yyyy): ")
            query = f"""
                    SELECT 
                    cities.name AS city_name,
                    round(avg(daily_weather_entries.mean_temp), 2) AS temperature, 
                    round(avg(daily_weather_entries.precipitation), 2) AS precipitation
                    FROM daily_weather_entries
                    JOIN cities ON daily_weather_entries.city_id = cities.id
                    WHERE strftime('%Y', daily_weather_entries.date) = '{year}'
                    GROUP BY
                    cities.name
                """
            phase_2.scatter_plot(query, year)

        elif user_input == "13":
            print("1: Delete a city record: ")
            print("2: Delete a country record: ")
            print("3: Delete the entire record in the database")
            select = input("Which delete operation would you want to perform? ")
            

            if select == "1":                               
                deleteCity(connection)                                     
            if select == "2":
                deleteCountry(connection)
            if select == "3":
                delete_entire_record(connection)
        
        elif user_input == "14":
            phase_4.retrieve_data()


        elif user_input.lower() == "quit":
            break
        else:
            print("Wrong input.. Please enter a valid choice number")


if __name__ == "__main__":
    PATH_TO_THIS_FILE = os.path.dirname(__file__)
    os.chdir(PATH_TO_THIS_FILE)

    print("CURRENT WORKING DIRECTORY: ", os.getcwd())

    with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        userInterface(connection)
        