from distutils.log import debug
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,inspect, func

from datetime import datetime,timedelta
app = Flask(__name__)

# # Create engine using the hawaii.sqlite database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base() # Declare a Base using `automap_base()`
Base.prepare(engine, reflect=True) # Use the Base class to reflect the database tables
Measurement = Base.classes.measurement # Assign the measurement class to a variable called `measurement`
Stations = Base.classes.station # Assign the measurement class to a variable called `Stationsb`
session = Session(engine) #Create session link from Python to the DB
# home route
@app.route('/')

def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Local API </h2> </center>"
        f"<center><h3>Select from one of the available routes:</h3> </center>"
        f"<center> /api/v1.0/precipitation</center>"
        f"<center> /api/v1.0/stations</center>"
        f"<center> /api/v1.0/tobs</center>"
        f"<center> /api/v1.0/start/end</center>"
     
        )

@app.route("/api/v1.0/precipitation")
def precip():
    #returne the previous year's precipitation as json
# /api/v1.0/precipitation
    previous_year_date =dt.date(2017,8,23)- dt.timedelta(days=365)

    #query sqllite database to get the data and precipitation 

    results=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year_date).all()
    session.close() 

    #dictionary with date for key and precipitation (prcp values)
    precipitation = {date:prcp for date, prcp in results}
    #convert to json
    return jsonify(precipitation)
# /api/v1.0/stations
@app.route("/api/v1.0/stations")

#retrieve the names of the stations
def stations():
    results = session.query(Stations.station).all()
    session.close()
    stationList = list(np.ravel(results))
    return jsonify(stationList)



#get dates and tempatures for the most active station for the previous year 
@app.route("/api/v1.0/tobs")

#retrieve the names of the date and temaptures for the last 12 months from the previous year date
def temperatures():
    previous_year_date =dt.date(2017,8,23)- dt.timedelta(days=365)    #get the previous twelve months for the previous year

    #query sqllite database to get the date and precipitation for the most active weather station
    active_station = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).\
              order_by(func.count(Measurement.station).desc()).first()

    results_last_twelve = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.station == active_station[0] ).\
    filter(Measurement.date >= previous_year_date).all()
    session.close() 

    temperature_list = list(np.ravel(results_last_twelve))
    return jsonify(temperature_list)


# /api/v1.0/start and /api/v1.0/end
@app.route ("/api/v1.0/<start>")
@app.route ("/api/v1.0/<start>/<end>")
def date_stats(start =None, end=None):

    #select statement
    selection=[func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        start_date = dt.datetime.strptime(start,"%m%d%Y")
        results=session.query(*selection).filter(Measurement.date >= start_date).all()
        session.close()

        temperature_list = list(np.ravel(results))
        return jsonify(temperature_list)
    else:
        start_date = dt.datetime.strptime(start,"%m%d%Y")
        end_date = dt.datetime.strptime(end,"%m%d%Y")
        results=session.query(*selection).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        session.close()
        
        temperature_list = list(np.ravel(results))
        return jsonify(temperature_list)


# app launcher 
if __name__ == '__main__':
    app.run(debug=True)


    

