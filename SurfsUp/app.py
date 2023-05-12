# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of your dictionary."""
    # Calculate the date 1 year ago from the last data point in the database
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d')
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query the precipitation data for the last 12 months
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    prcp_dict = {}
    for result in prcp_results:
        prcp_dict[result[0]] = result[1]

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query all stations
    station_results = session.query(Station.station).all()

    # Convert the query results to a list
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year."""
    # Calculate the date 1 year ago from the last data point in the database
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d')
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query the most active station
    most_active_station = session.query(Measurement.station).\
                          group_by(Measurement.station).\
                          order_by(func.count(Measurement.station).desc()).\
                          first()

    # Query the temperature data for the last 12 months for the most active station
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
                   filter(Measurement.station == most_active_station[0]).\
                   filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a list
    tobs_list = []
    for result in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = result.date
        tobs_dict["tobs"] = result.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_summary(start, end=None):
    """Return a JSON list of the minimum temperature, the average temperature,
    and the maximum temperature for a specified start or start-end range."""
    if end:
        # Calculate TMIN, TAVG, and TMAX for the dates between start and end
        temperature_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                              filter(Measurement.date >= start).\
                              filter(Measurement.date <= end).all()
    else:
        # Calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
        temperature_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                              filter(Measurement.date >= start).all()

    # Convert the query results to a list
    temperature_list = []
    for result in temperature_results:
        temperature_dict = {}
        temperature_dict["TMIN"] = result[0]
        temperature_dict["TAVG"] = result[1]
        temperature_dict["TMAX"] = result[2]
        temperature_list.append(temperature_dict)

    return jsonify(temperature_list)

if __name__ == '__main__':
    app.run()