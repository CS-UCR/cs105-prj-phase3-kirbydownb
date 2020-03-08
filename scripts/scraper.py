from bs4 import BeautifulSoup
from constants import ot_url, mongodb_atlas_connection
import urllib
import requests

client = pymongo.MongoClient(mongodb_atlas_connection)

# visit that url, and grab the html of said page
result = requests.get(ot_url)
content = result.content

# we need to convert this into a soup object
soup = BeautifulSoup(content, 'html.parser')
print(soup.prettify())