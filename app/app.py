import os 
from flask import Flask, json, jsonify, request, render_template
import numpy as np
import requests
import socket
from amadeus import Client, ResponseError
from secret import *

HOST_NAME = os.environ.get("OPENSHIFT_APP_DNS", "localhost")
APP_NAME = os.environ.get("OPENSHIFT_APP_NAME", "hack-apac-2021")
IP = os.environ.get("OPENSHIFT_PYTHON_IP", "127.0.0.1")
PORT = int(os.environ.get("OPENSHIFT_PYTHON_PORT", 8001))
HOME_DIR = os.environ.get("OPENSHIFT_HOMEDIR", os.getcwd())
app = Flask(__name__)
client = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET
)

@app.route("/", methods=["GET", "POST"])
def index():
    # return "Hello World!"
    return render_template("index.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/stats")
def stats():
    return jsonify({
        "host_name": HOST_NAME,
        "app_name": APP_NAME,
        "ip": IP,
        "port": PORT,
        "home_dir": HOME_DIR,
        "host": socket.gethostname()
    })

@app.route("/response")
def response():
    try:
        resp = client.shopping.flight_offers_search.get(
            originLocationCode='MAD',
            destinationLocationCode='ATH',
            departureDate='2022-06-01',
            adults=1)
        return jsonify(resp.data)
    except ResponseError as error:
        return error

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT, threaded=True)
    