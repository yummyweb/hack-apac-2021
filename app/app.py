import os 
from flask import Flask, json, jsonify, request, render_template
import numpy as np
# import caer
# import cv2 as cv
import requests
import socket

HOST_NAME = os.environ.get("OPENSHIFT_APP_DNS", "localhost")
APP_NAME = os.environ.get("OPENSHIFT_APP_NAME", "hack-apac-2021")
IP = os.environ.get("OPENSHIFT_PYTHON_IP", "127.0.0.1")
PORT = int(os.environ.get("OPENSHIFT_PYTHON_PORT", 8001))
HOME_DIR = os.environ.get("OPENSHIFT_HOMEDIR", os.getcwd())
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # return "Hello World!"
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "This is another hello world!"
    # return render_template("index.html")

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

# print("IP = ", IP)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT, threaded=True)
    