import requests as r

KEY = "4a004d3faa4044fabc794a3ec713cff8"


headers = {
    "x-api-key": KEY,
    "Content-type": "application/json"
}

response = r.get("https://covid-api.thinklumo.com/data?airport=BOS", headers=headers)

from pprint import pprint 
# print(response.ok)
# print(response)
print(response.text)
# print("\n\n")
# print(response.json()["travel_advisories"])
