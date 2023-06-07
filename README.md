# Climate analysis 

## Before You Begin
To start the SQLAlchemy challenge, I followed the instructions provided. Here are the steps I followed:

1. Created a new repository called "sqlalchemy-challenge" specifically for this project.
2. Cloned the repository to my computer.
3. Inside the local Git repository, created a directory named "SurfsUp" corresponding to the challenge.
4. Added the Jupyter notebook (climate_starter.ipynb) and app.py to the "SurfsUp" directory. These files contain the main scripts for analysis.
5. Added the "Resources" folder to the "SurfsUp" directory. This folder contains the data files required for the challenge.
6. Pushed the changes to GitHub or GitLab for version control and collaboration.

## Part 1: Analyze and Explore the Climate Data
In this part, I used Python and SQLAlchemy to perform a basic climate analysis and data exploration of the climate database. The steps followed are as follows:

1. Used the SQLAlchemy create_engine() function to connect to the SQLite database.
2. Used the SQLAlchemy automap_base() function to reflect the tables into classes and saved references to the classes named Station and Measurement.
3. Linked Python to the database by creating a SQLAlchemy session.
4. Conducted a precipitation analysis and a station analysis.

## Precipitation Analysis
For the precipitation analysis, I completed the following steps:

1. Found the most recent date in the dataset.
2. Used the most recent date to query the previous 12 months of precipitation data.
3. Selected only the "date" and "prcp" values.
4. Loaded the query results into a Pandas DataFrame and set the column names explicitly.
5. Sorted the DataFrame values by "date".
6. Plotted the results using the DataFrame plot method.
7. Printed the summary statistics for the precipitation data using Pandas.

## Station Analysis
For the station analysis, I completed the following steps:

1. Designed a query to calculate the total number of stations in the dataset.
2. Designed a query to find the most-active stations by listing the stations and observation counts in descending order.
3. Identified the station ID with the greatest number of observations.
4. Designed a query to calculate the lowest, highest, and average temperatures for the most-active station.
5. Designed a query to retrieve the previous 12 months of temperature observation (TOBS) data for the most-active station.
6. Plotted the results as a histogram with bins=12.

## Part 2: Design Your Climate App
After completing the initial analysis, I designed a Flask API based on the queries developed. Here are the routes I created using Flask:

* / - This route starts at the homepage and lists all the available routes.
* /api/v1.0/precipitation - This route converts the query results from the precipitation analysis (last 12 months of data) into a dictionary using date as the key and precipitation as the value. It returns the JSON representation of the dictionary.
* /api/v1.0/stations - This route returns a JSON list of stations from the dataset.
* /api/v1.0/tobs - This route queries the dates and temperature observations of the most active station for the previous year of data. It returns a JSON list of temperature observations for the previous year.
* /api/v1.0/<start> and /api/v1.0/<start>/<end> - These routes return a JSON list of the minimum, average, and maximum temperatures for a specified start or start-end range. For a specified start, it calculates TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date. For a specified start and end date, it calculates the same values for the dates within the specified range.
  
I used Flask and the jsonify function to create the routes and convert the API data to valid JSON responses.

Remember to close the session at the end of the notebook to ensure proper cleanup.
