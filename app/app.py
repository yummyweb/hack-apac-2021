from babel import numbers
import os 
from flask import Flask, json, jsonify, request, render_template
import numpy as np
import requests
import socket
from amadeus import Client, ResponseError
from secret import *
from pyairports.airports import Airports
import pycountry
from geopy.geocoders import Nominatim


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
airports = Airports()
geocoder = Nominatim(user_agent="XED")

def generate_amadeus_access_token():
    r = requests.post(
            "https://test.api.amadeus.com/v1/security/oauth2/token", 
            data={
                "grant_type": "client_credentials", 
                "client_id": AMADEUS_API_KEY, 
                "client_secret": AMADEUS_API_SECRET
            }
        )
    if r.json()["state"] == "approved":
        return r.json()["access_token"]
    else:
        return None
    
def amadeus_get(endpoint : str):
    r = requests.get(
            "https://test.api.amadeus.com" + endpoint, 
            headers={
                "authorization": "Bearer " + AMADEUS_ACCES_TOKEN
            }
        )
    if r.status_code != 200:
        print(f"[INFO] Status code is _NOT_ 200, but {r.status_code}. Re-generating AMADEUS_ACCESS_TOKEN")
        new_token = generate_amadeus_access_token()
        r = requests.get(
            "https://test.api.amadeus.com" + endpoint,
            headers={
                "authorization": "Bearer " + new_token
            }
        )
    return r.json()

def get_airport(city):
    resp = amadeus_get(f"/v1/reference-data/locations?subType=CITY,AIRPORT&keyword={city}")
    return resp["data"][1]

def get_city_code(city):
    resp = amadeus_get(f"/v1/reference-data/locations?subType=CITY,AIRPORT&keyword={city}")
    return resp["data"][0]

def get_jwt():
    r = requests.post("https://api.makcorps.com/auth", data={
        "username": "antriksh1234",
        "password": "qixmit-1sikfe-vanvuM"
    })
    return r.json()["access_token"]

def get_hotels(city):
    r = requests.get(f"https://api.makcorps.com/free/{city}", headers={
        "authorization": "JWT " + str(get_jwt())
    })
    print(r.json())
    return r.json()["Comparison"]

@app.route("/", methods=["GET"])
def index():
    return render_templaste("index.html")

@app.route("/results", methods=["POST"])
def results():
    try:
        origin_airport = get_airport(request.form["origin"])
        destination_airport = get_airport(request.form["to"])
        destination_city = str(request.form["to"])
        r = requests.get(f"https://eu1.locationiq.com/v1/search.php?key={LOCATION_IQ}&city={destination_city}&format=json")
        destination_lat = str(r.json()[0]["lat"])
        destination_lng = str(r.json()[0]["lon"])
        try:
            destination_content = amadeus_get(f"/v1/reference-data/locations/pois?latitude={destination_lat}&longitude={destination_lng}")["data"]
        except:
            destination_content = None
        covid_data = get_covid_data(str(request.form["origin"]), str(request.form["to"]))
        hotel_list = get_hotels(destination_city)
        resp = client.shopping.flight_offers_search.get(
            originLocationCode=str(origin_airport["iataCode"]),
            destinationLocationCode=str(destination_airport["iataCode"]),
            departureDate=str(request.form["date"]),
            adults=1)

        flights = {
            "flights": []
        }
        for d in resp.data[:6]:
            price = numbers.format_currency(float(d["price"]["total"]), d["price"]["currency"], locale="en")
            flight = {
                "travel": [],
                "price": price
            }
            for s in d["itineraries"][0]["segments"]:
                depAirport = airports.airport_iata(s["departure"]["iataCode"])
                arrAirport = airports.airport_iata(s["arrival"]["iataCode"])
                airline = client.reference_data.airlines.get(airlineCodes=s["carrierCode"])
                flight["travel"].append({
                    "departure": {
                        "airport": depAirport[0]
                    },
                    "arrival": {
                        "airport": arrAirport[0]
                    },
                    "airline": airline.data[0]["commonName"]
                })

            flights["flights"].append(flight)
        
        flights["covid"] = covid_data
        if destination_content:
            flights["destination"] =  destination_content[:6] if len(destination_content) > 6 else destination_content
        else:
            flights["destination"] = []
        
        flights["hotels"] =  hotel_list[:10] if len(hotel_list) > 10 else hotel_list
        return render_template("results.html", flights=flights)
    except ResponseError as error:
        print(f"[Error] {error}")
        return render_template("results.html")


def get_covid_data(origin: str, destination : str):
    """
        `origin` and `destination` need to be city names.
        Eg: Boston/Chicago/Delhi etc
    """
    destination_country_name = geocoder.geocode(str(destination))[0].split(",")[-1].strip()  # Example: India
    if destination_country_name == "España":
        destination_country_name = "Spain"
    elif destination_country_name == "Deutschland":
        destination_country_name = "Germany"
    destination_country_code = pycountry.countries.search_fuzzy(destination_country_name)[0].alpha_2 # IN

    origin_country_name = geocoder.geocode(str(destination))[0].split(",")[-1].strip() # Example: United States
    if origin_country_name == "España":
        origin_country_name = "Spain"
    elif origin_country_name == "Deutschland":
        origin_country_name = "Germany"
    origin_country_code = pycountry.countries.search_fuzzy(origin_country_name)[0].alpha_2 # US

    output = amadeus_get(f"/v1/duty-of-care/diseases/covid19-area-report?countryCode={destination_country_code}")
    if output is None:
        raise ValueError("output is None")
    
    summary = output["data"]["summary"]
    disease_risk_level = output["data"]["diseaseRiskLevel"] # High/Medium/Low
    print("Disease risk level = ", disease_risk_level)
    hotspots = output["data"]["hotspots"]

    display_hotspots = False
    if origin.strip() in hotspots:
        display_hotspots = True

    # Access Restrictions
    access_restrictions = output["data"]["areaAccessRestriction"]["entry"]
    access_restrictions_ban = access_restrictions["ban"] # Partial/Complete
    access_restrictions_text = access_restrictions["text"] 

    # Is origin country a banned country to travel from, for the destination country?
    origin_country_banned = False
    for i in access_restrictions["bannedArea"]:
        if i["areaType"] == "country" and i["iataCode"] == origin_country_code:
            origin_country_banned = True
        
    # What about land/maritime borders?
    maritime_border_ban_text = ""
    land_border_ban_text = ""
    for i in access_restrictions["borderBan"]:
        if "maritime" in i["borderType"]:
            maritime_border_ban_text = i["status"].strip()
        else:
            land_border_ban_text = i["status"].strip()

    # Covid testing guidelnes
    testing = output["data"]["areaAccessRestriction"]["diseaseTesting"]
    is_testing_required = True if "Yes" in testing["isRequired"] else False
    when_is_testing_required = testing["when"] # Before/After Travel
    testing_requirement = testing["requirement"]
    testing_rules = testing["rules"] # URL to testing requirements 

    # Quarantine
    # print(output["data"]["areaAccessRestriction"]["quarantineModality"])
    quarantine = output["data"]["areaAccessRestriction"]["quarantineModality"]
    quarantine_requirements_text = quarantine["text"]
    quarantine_requirements_mandatory = False if "not required" in quarantine_requirements_text else True

    # Mask usage
    mask = output["data"]["areaAccessRestriction"]["mask"]
    mask_is_required = mask["isRequired"] # "Yes"/"No"/"Yes, Conditional"
    mask_learn_more_text = mask["text"] # More details about mask usage

    # Vaccine stats
    vaccine = output["data"]["areaAccessRestriction"]["diseaseVaccination"]
    vaccination_is_required = True if "Yes" in vaccine["isRequired"] else False

    vaccination_stats = output["data"]["areaVaccinated"]
    single_dose_percent = ""
    two_doses_percent = ""
    for i in vaccination_stats:
        if i["vaccinationDoseStatus"].strip() == "oneDose":
            single_dose_percent = str(i["percentage"]) + "%"
        else:
            two_doses_percent = str(i["percentage"]) + "%"

    """
        Return a dictionary with ALL of the variable to be displayed in the banner. Arrange it as per your wish. We'll remove unnecessary stuff later
    """
    return dict({
        "mask": {
            "required": mask_is_required,
            "text": mask_learn_more_text
        },
        "testing": {
            "required": is_testing_required,
            "text": "<strong>" + when_is_testing_required.lower() + "</strong>"
        },
        "quarantine": {
            "required": quarantine_requirements_mandatory,
            "text": quarantine_requirements_text
        },
        "hotspot": {
            "display_hostspots": display_hotspots,
            "disease_risk_level": disease_risk_level
        }
    })

# get_covid_data("Boston", "Chicago")

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
            originLocationCode="MAD",
            destinationLocationCode="ATH",
            departureDate="2022-06-01",
            adults=1)
        return jsonify(resp.data)
    except ResponseError as error:
        return error

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=PORT, threaded=True)
    