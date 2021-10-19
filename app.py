{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "0280ca64",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "import datetime as dt\n",
    "import numpy as np\n",
    "\n",
    "\n",
    "\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "\n",
    "from flask import Flask, jsonify\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "fd5732a9",
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///hawaii.sqlite\")\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "session = Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "f012ead3",
   "metadata": {},
   "outputs": [],
   "source": [
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "900e2c73",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [18/Oct/2021 20:45:11] \"\u001b[37mGET / HTTP/1.1\u001b[0m\" 200 -\n",
      "127.0.0.1 - - [18/Oct/2021 20:45:11] \"\u001b[33mGET /favicon.ico HTTP/1.1\u001b[0m\" 404 -\n"
     ]
    }
   ],
   "source": [
    "# Flask Setup\n",
    "#################################################\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route(\"/\")\n",
    "def home():\n",
    "    \"\"\"List all available api routes.\"\"\"\n",
    "    return (\n",
    "        f\"Wecome to the 'Home' page<br/>\"\n",
    "        f\"Available Routes: <br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/<start><br/>\"\n",
    "        f\"/api/v1.0/<start>/<end><br/>\"\n",
    "    )\n",
    "\n",
    "@app.route(\"/api/v1.0/percipitation\")\n",
    "def percipitation():\n",
    "    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)\n",
    "    yearprcp = session.query(Measurement.date, Measurement.prcp).\\\n",
    "                    filter(Measurement.date >= year_ago).all()\n",
    "    prcp = {date:prcp for date,prcp in yearprcp}\n",
    "    return jsonify(prcp)\n",
    "\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    \n",
    "    results = session.query(Station.station).all()\n",
    "\n",
    "    all_stations = list(np.ravel(results))\n",
    "\n",
    "    return jsonify(all_stations)\n",
    "\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "\n",
    "def tobs():\n",
    "    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)\n",
    "    tempobs = session.query(Measurement.station,Measurement.tobs).\\\n",
    "              filter(Measurement.station == 'USC00519281').\\\n",
    "              filter(Measurement.date >=  year_ago).all()\n",
    "    temps = list(np.ravel(tempobs))\n",
    "    return jsonify(temps)\n",
    "    \n",
    "          \n",
    "    \n",
    "     \n",
    "    \n",
    "@app.route(\"/api/v1.0/<start>\")\n",
    "def start_temp(start):\n",
    "    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "        filter(Measurement.date >= start).all()\n",
    "    return jsonify(results)\n",
    "\n",
    "@app.route(\"/api/v1.0/<start>/<end>\")\n",
    "def start_end_temp(start,end):\n",
    "    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "        filter(Measurement.date >= start).\\\n",
    "        filter(Measurement.date <= end).all()\n",
    "    return jsonify(results)\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=False)\n",
    "     \n",
    "\n",
    "    \n",
    "        \n",
    "        \n",
    "    \n",
    "\n",
    " \n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b1d34bc",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
