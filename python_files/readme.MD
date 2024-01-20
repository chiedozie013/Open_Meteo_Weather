# ICA on Software for Digital Innovation (CIS4044-N)

## Author: James, Chiedozie James
## Student ID: d3458961



# Phase 1 - Python for SQLite3 Database Queries
In this phase, i wrote queries to the 6 functions provided.

1. For the first function, i passed in the connected database to the function and wrote a query to select all countries from the countries table.

2. The second function, i passed in the connected database to the function and wrote a query to select all cities from the cities table.

3. The third function quaries average annual temperature of a particular city. passing in the connected database to the function and demanding the user enters a city id they want to quary and the year of choice. after the city id and year is inputed it processes the query with that information and produced the average annual precipitation in 2 decimal places

4.  the fouth function queries the the avarage seven day precipitation of a paticular user inputted city ID and start date. The average of the seven day precipitation is outputed in 2 decimal places. The function takes in 3 parameters, connection to the database, city ID and start date.

5.  The fifth function takes in connection to the database, queries average mean temperature from the datapase of a particular user given city ID, start date and end date. this query retrives the average in 2 decimal places.

6.  The sixth function takes in connection to the database, queries the average annual precipitation for all countires in the database for any user given year. The user is promted to enter a year of chioce and the anual recitation for that year is calculated and outputted in 2 decimal places.

# Phase 2. Basic Graphs using Matplotlib.
in this phase, i wrote functions to plot various graphs using retrieved data gotten from queries into a database. Below are discriptions of plots

1.  The first function in the phase 2 takes in query, creates the connection to the database, sets te row_factory attrinute to the database, creates a cursor and executes the passed in query.

2.  The second function in this phase plots a bar chart to show 7 day precipitation for a specific city. It takes in 3 arguments, query for the database, user inputted city name and start date, then plots a bar chart with the retrieved information, precipitation against date for the seven days starting from the given start date.

3.  The third function in this phase plots a bar chart showing the average annual tenperature for all cities in the database for a user given year. The function takes in 2 arguments, query and user inputted year and plots a bar chart with year against cities.

4.  The fourth function in this phase plots a bar chart showing the average annual precipitation for all years in the database for a user given country name. The function takes in 2 arguments, query to the database and country name given by the user and plots a bar chart for average preciitation against year.

5.  The fifth function in this phase, group_bar_chart is a grouped bar chart showing the min, max and mean temperature as well as precipitation of a a particular user given day for all cities in the database. This function takes in 2 arguments, query to the database and date given by the user with the python input function.

6.  The multi_line function is a line chart that plots the daily maximum and minimum temperatures for a given month for a specific user given city. This function takes in 3 arguments, query to the database, city name and date comprising of just year and month.

7.  The scatter_plot function is a scatter plot chart for average temperature against average precipitation for all city. The function takes in 2 arguments, query to the database and year. this scatter plot chart is temperature and rainfall.

# Phase 3. User Interface.
This phase provides the user with an interface to enable the user to perform all data queries for all phases. The user is provided with statements and each function to perform is attributed a number, the user is required to choose any number from the list displayed and that function or queried is carried out and the output displayed on the console or the plot is displayed. 
This interface uses a while true statement and it loops over and over until the user enters quit to terminate the loop

This interface also enables the user to delete some user specified data or all data stored in the Sqlite3 database.. 
the user decides if 
a.  to delete a city and its record from the cities and daily entry tables
b.  delete an entire country and all it city records  
c.  delete the entire recod in the database.
the user interface also enables the user to invoke and perform the retrieve_data function from phase 4 which retrieves and updates a database.

# Phase 4. Data Retrieval and Storage.
This phase retrieves data from the Open Meteo API and stores the data extracted from the JSON response in a SQlite3 database.
It prompts the user to provide parameters such as lattitude, longtude, country name, zone time, start date and end date to perform the retrieval from the database. Data retrieved from the API is then inserted into the database. First the function checks if the country name already exists in the database if it exist it skips else it inserts into the country table. Then it confirms if the city name exists in the database, if it exists it skips else its inserts city details into the cities table and alos an if statement to check if the date to be inserted exits and it it does it skips and displays an error that date exists else it inserts all details into the daily weather entries table.

# Testing.
I further wrote a code to test the retrieve_data function. and it tests ok.