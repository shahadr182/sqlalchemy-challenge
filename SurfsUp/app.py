# Import the dependencies.
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///mydatabase.db")

# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(results))

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()
      # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperature observations"""
    # Query all temperature observations
    results = session.query(Measurement.date, Measurement.tobs).all()

    # Convert list of tuples into normal list
    all_temperatures = list(np.ravel(results))

    return jsonify(all_temperatures)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of all temperature observations starting from the given start date"""
    # Query temperature observations
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_temperatures = []
    for date, min_temp, avg_temp, max_temp in results:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Minimum Temperature"] = min_temp
        temp_dict["Average Temperature"] = avg_temp
        temp_dict["Maximum Temperature"] = max_temp
        all_temperatures.append(temp_dict)
        return jsonify(all_temperatures)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a list of all temperature observations between the given start and end dates"""
    # Query temperature observations
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_temperatures = []
    for date, min_temp, avg_temp, max_temp in results:
        temp_dict    


    
