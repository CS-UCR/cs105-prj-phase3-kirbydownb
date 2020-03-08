import urllib3
from constants import income_url, first, second, income_url_lower_page_limit, income_url_upper_page_limit
from bs4 import BeautifulSoup
from constants import mongodb_atlas_connection
from pymongo import MongoClient

# Create MongoDB instance
client = MongoClient(mongodb_atlas_connection)
db = client['income']
collection = db['zipcode']

def getUpcomingEvents(url):
  for i in range(income_url_lower_page_limit, income_url_upper_page_limit):
    req = urllib3.PoolManager()
    
    if i == income_url_lower_page_limit:
        url = income_url
    else:
        url = first + str(i) + second

    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')
    events = soup.findAll('tr')
    
    for event in events:
      try:
        event_details = dict()
        income = event.find('b').text
        zip_code = event.find('a').text
        
        event_details['income'] = income
        event_details['zip'] = zip_code

        print('INSERTING INCOME', event_details)
        collection.insert_one(event_details)
      except:
        pass

getUpcomingEvents(income_url)