import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect database
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# references to tables (we already know them)
measurement = Base.classes.measurement
station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """list all available routes"""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        # f"/api/v1.0/<start> <br/>"
        # f"/api/v1.0/<start>/<end> <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """convert query results to a dictionary using date as the key and prcp as the value"""
    """return JSON representation of dictionary"""
    session = Session(engine)
    prcp_results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    prcp_data = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        # prcp_dict["date"] = date and prcp_dict["prcp"] = prcp isn't quite what we're being asked for
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    """return JSON list of stations"""
    session = Session(engine)
    stations_results = session.query(station.station).all()
    session.close()

    # convert list of tuples into "normal" list
    all_stations = list(np.ravel(stations_results))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """query dates and temps of most active station for last year"""
    """return JSON list of temp observations"""
    session = Session(engine)

    # find THE most active station
    mostActive_station = session.query(measurement.station)\
    .group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]
    # last/ most recent date in data set
    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    # convert date into datetime obj to perform calculations
    most_recent_cvt = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    


    session.close()

    return jsonify()

# @app.route("/api/v1.0/<start>")
# def temps_start(start_date):
#     """return JSON list of min/max/avg temps for all dates >= given start date"""


# @app.route("/api/v1.0/<start>/<end>")
# def temps_start_end(start_date, end_date):
    # """return JSON list of min/max/avg temps for all dates between given start and end dates (inclusive"""

if __name__ == "__main__":
    app.run(debug=True)
