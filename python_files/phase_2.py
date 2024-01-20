
import os
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

def query_database(query):
    with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connect:

        connect.row_factory = sqlite3.Row

        cursor = connect.cursor()        
        results = cursor.execute(query)
        

        connect.commit()

        return results

def plot_7_day_precipitation(query, city_name, start_date):
    results = query_database(query)

    data = {
            "precipitation": [],            
            "date": []
        }

    for row in results:
        data["precipitation"].append(row['precipitation'])           
        data["date"].append(row['date'])
    
    
    plt.bar(data['date'], data['precipitation'], color='blue')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.title(f'7 Day Precipitation for {city_name} from {start_date}')    
    plt.tick_params(axis = 'x', labelrotation = 55)

    plt.show()

def avg_annual_temp(query, year):
    results = query_database(query)

    data = {
            "city_name": [],
            "avg_max_temp": [],                  
            
        }

    for row in results:
        data['city_name'].append(row['city_name'])
        data['avg_max_temp'].append(row['avg_max_temp'])
         
    plt.bar(data['city_name'], data['avg_max_temp'], color='blue')
    plt.xlabel('City Name')
    plt.ylabel('Avg Maximum Temperature')
    plt.title(f'Annual Average Max Temperature for all Cities in {year}')
    plt.tick_params(axis = 'x', labelrotation = 75)
    plt.show()

def average_yearly_precipitation(query, country_name):
    results = query_database(query)

    data = {
            "avg_precipitation": [],            
            "year": []
        }

    for row in results:
        data["avg_precipitation"].append(row['avg_precipitation'])           
        data["year"].append(row['year'])
    
    
    plt.bar(data['year'], data['avg_precipitation'], color='blue')
    plt.xlabel('Year')
    plt.ylabel('Avg_Precipitation (mm)')
    plt.title(f'Yearly Average Precipitation for {country_name} from year 2000 - 2022')    
    plt.tick_params(axis = 'x', labelrotation = 75)

    plt.show()


def group_bar_chat(query, date):
    results = query_database(query)

    data = {
            "name": [],            
            "min_temp": [],
            "max_temp": [],
            "mean_temp": [],
            "precipitation": []
        }

    for row in results:
        data["name"].append(row['name'])           
        data["min_temp"].append(row['min_temp'])
        data["max_temp"].append(row['max_temp'])
        data["mean_temp"].append(row['mean_temp'])
        data["precipitation"].append(row['precipitation'])
    
    bar_width = 0.20
    index = np.arange(len(data['name']))
    
    plt.bar(index, data['min_temp'], width = bar_width, label = 'Min_Temp', color='blue')
    plt.bar(index + bar_width, data['max_temp'], width = bar_width, color='red', label = 'Max_Temp')
    plt.bar(index + (bar_width * 2), data['mean_temp'], width = bar_width, color='green', label = 'Mean_Temp')
    plt.bar(index + (bar_width * 3), data['precipitation'], width = bar_width, color='orange', label = 'Precipitation')
    plt.xlabel('Cities')
    plt.ylabel('Avg_Precipitation (mm)')
    plt.title(f'Min, Max , Mean Temperature and Precipitation values for {date}')    
    plt.xticks(index + bar_width / 2, data["name"])
    plt.tick_params(axis = 'x', labelrotation = 55)
    plt.legend()
    plt.grid(True)
    plt.show()


def multi_line(query, city_name, date):
    results = query_database(query)

    data = {
            "date": [],
            "min_temp": [],            
            "max_temp": []            
        }

    for row in results:
        data['date'].append(row['date'])
        data["min_temp"].append(row['min_temp'])           
        data["max_temp"].append(row['max_temp'])
    
    
    plt.plot(data["date"], data['max_temp'], color = 'blue', label = 'Max_Temp')
    plt.plot(data["date"], data['min_temp'], color = 'red', label = 'Min_Temp')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    plt.title(f'Daily Minimum and Maximum Temperature for {city_name} for {date}')
    plt.grid()    
    plt.tick_params(axis = 'x', labelrotation = 80)
    plt.legend()

    plt.show()

def scatter_plot(query, year):
    results = query_database(query)

    data = {
            "city_name": [],
            "temperature": [],            
            "precipitation": []            
        }
   
    
    for row in results:
        data["city_name"].append(row['city_name']) 
        data["temperature"].append(row['temperature'])           
        data["precipitation"].append(row['precipitation'])

    x = data['precipitation']
    y = data['temperature']
    
    


    plt.scatter(x, y, color = 'red', marker = 'o')
   

    plt.xlabel('Rainfall')
    plt.ylabel('Temperature')
    
    plt.title(f'Scatter Plot of Average Temperature and Average Precipitation for all cities in year {year}')
    # Adding city names as annotations
    for city, temp, precip in zip(data["city_name"], data["temperature"], data["precipitation"]):
        plt.annotate(f'{city}', (precip, temp), textcoords="offset points", xytext=(0, 5), ha='center')
    
    # Add dotted lines
    for xi, yi in zip(x, y):
        plt.plot([xi, xi], [0, yi], color='gray', linestyle='--', linewidth=0.8)
        plt.plot([0, xi], [yi, yi], color='gray', linestyle='--', linewidth=0.8)

    plt.show()

if __name__ == "__main__":
    PATH_TO_THIS_FILE = os.path.dirname(__file__)
    os.chdir(PATH_TO_THIS_FILE)

    print("CURRENT WORKING DIRECTORY: ", os.getcwd())
    
    print("Bar Chart to show the 7-day precipitation for a specific town/city")
    city_name = input("Please enter a city name: ")
    city_name = city_name.title()
    start_date = input("Please enter a start date(yyyy-mm-dd): ")
    query = f"""
            SELECT date, precipitation FROM [daily_weather_entries]
            JOIN cities On daily_weather_entries.city_id = cities.id 
            WHERE cities.name = '{city_name}' and date BETWEEN '{start_date}' AND DATE('{start_date}', '+6 days')
        """
    plot_7_day_precipitation(query, city_name, start_date)
    print()
    print("Bar Chart to show aanual average maximum temperature for all cities in a particular year")
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
    avg_annual_temp(query, year)
    print()
    print("Bar Chart to show the average yearly precipitation by country")
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

    average_yearly_precipitation(query, country_name)
    print()
    print("Group Bar Charts to displaying the min/max/mean temperatures and precipitation values of a particular day for all cities")
    date = input("Please enter a date (yyyy-mm-dd): ")
    query = f"""
        SELECT cities.name, min_temp, max_temp, mean_temp, precipitation
        FROM daily_weather_entries
        JOIN cities ON daily_weather_entries.city_id == cities.id
        WHERE date = '{date}'
        GROUP BY city_id
    """
    group_bar_chat(query, date)
    print()
    print("Multi Line chart to show the daily minimum and maximum temperature fora given month for a specific month ")
    city_name = input("Please enter a city name: ")    
    city_name = city_name.title()
    date = input("Please enter the year and month (yyyy-mm): ")
    query = f"""
            SELECT date, min_temp, max_temp
            FROM daily_weather_entries
            JOIN cities On daily_weather_entries.city_id = cities.id
            WHERE cities.name = '{city_name}' AND strftime('%Y-%m', date) = '{date}' 
        """
    multi_line(query, city_name, date)
    print()
    print("Scatter plot chat of temperatures against rainfall for a city in a given month ")
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
    scatter_plot(query, year)

