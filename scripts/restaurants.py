from pymongo import MongoClient
from constants import yelp_businesses_url, mongodb_atlas_connection
from keys import yelp_api
import urllib
import requests
import re
import zipcodes
import json

def getIncomeZipcodes():
  income_zipcodes = []
  client = MongoClient(mongodb_atlas_connection)
  db = client['income']
  collection = db['zipcode']

  for document in collection.find():
    zipcode = document['zip']
    print("GOT ZIPCODE", zipcode)
    if len(zipcode) > 0 and zipcode.isnumeric() and zipcodes.is_real(str(zipcode)):
      income_zipcodes.append(zipcode)
  
  client.close()

  return income_zipcodes

def getRestaurants(income_zipcodes):
  zipcode_restaurants = []


  for index, zipcode in enumerate(income_zipcodes):
    req = requests.get(url=yelp_businesses_url, params={"location": zipcode, "categories": "restaurants"}, headers={"Authorization": "Bearer " + yelp_api})
    data = json.loads(req.text)
    
    print("GOT DATA", data)
    print("####     COUNT", index)

    restaurants = data['businesses']
    
    zipcode_restaurant = {'zipcode': zipcode, 'restaurants': restaurants}
    zipcode_restaurants.append(zipcode_restaurant)

  return zipcode_restaurants

def insertRestaurants(zipcode_restaurants):
  client = MongoClient(mongodb_atlas_connection)
  db = client['yelp']
  collection = db['restaurants_new']

  for zipcode_restaurant in zipcode_restaurants:
    print("INSERTING ZIPCODE AND RESTAURANT", zipcode_restaurant)
    collection.insert_one(zipcode_restaurant)
  
  client.close()

income_zipcodes = getIncomeZipcodes()
print(income_zipcodes, len(income_zipcodes))
zipcode_restaurants = getRestaurants(income_zipcodes)
insertRestaurants(zipcode_restaurants)