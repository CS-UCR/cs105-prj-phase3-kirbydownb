from pymongo import MongoClient
from constants import yelp_businesses_url, mongodb_atlas_connection, num_restaurant_limit, num_zipcode_limit
from keys import yelp_api
import urllib
import requests
import re
import json

def storeRestaurants(restaurants_collection, result):
  for document in restaurants_collection:
    zipcode = document['zipcode']
    restaurants = document['restaurants']
    data = {'zipcode': zipcode, 'restaurants': restaurants[:num_restaurant_limit]}

    print("APPENDING TOP RESTAURANT DATA", data)
    result.append(data)
  
  return result

def getRestaurants():
  all_restaurants = []
  client = MongoClient(mongodb_atlas_connection)
  yelp_db = client['yelp']
  restaurants_collection = yelp_db['restaurants']

  top_income_restaurants = list(restaurants_collection.find())[:num_zipcode_limit]
  bottom_income_restaurants = list(restaurants_collection.find())[-num_zipcode_limit:]

  storeRestaurants(top_income_restaurants, all_restaurants)
  storeRestaurants(bottom_income_restaurants, all_restaurants)
  
  client.close()

  return all_restaurants

def getReviews(restaurant_data):
  all_reviews = []

  for obj in restaurant_data:
    zip_code = obj['zipcode']
    restaurants = obj['restaurants']

    for restaurant in restaurants:
      rid = restaurant['id']
      name = restaurant['name']

      yelp_reviews_url = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(rid)

      try:
        req = requests.get(url=yelp_reviews_url, headers={"Authorization": "Bearer " + yelp_api})
        data = json.loads(req.text)
        reviews = data['reviews']
        
        restaurant_review = {'rid': rid, 'name': name, 'reviews': reviews, 'zipcode': zip_code}
        print("GOT REVIEW", restaurant_review)
        
        all_reviews.append(restaurant_review)
      except:
        print("ERROR GETTING REVIEWS FOR", rid)

  return all_reviews

def insertReviews(reviews):
  client = MongoClient(mongodb_atlas_connection)
  yelp_db = client['yelp']
  reviews_collection = yelp_db['reviews']

  for review in reviews:
    try:
      print("INSERTING REVIEW", review)
      reviews_collection.insert_one(review)
    except:
      print("ERROR INSERTING REVIEW", review)
    
  client.close()

restaurants = getRestaurants()
reviews = getReviews(restaurants)
insertReviews(reviews)