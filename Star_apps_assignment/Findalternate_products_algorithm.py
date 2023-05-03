import requests
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import json


def FindAlternateGroups(store_domain):
    # Make a request to the store domain
    response = requests.get(store_domain+ '/products.json')

    data = response.json()

    # Extract the product URLs from the JSON data
    urls = []
    for product in data['products']:
        urls.append(store_domain + '/products/' + product['handle'])

    # Parse the HTML of each product page and extract the product names
    names = []
    for product in data["products"]:
        title = product["title"]
        names.append(title.strip())



    # Use K-means clustering to group the product URLs by name similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(names)
    kmeans = KMeans(n_clusters=5, n_init=10)
    kmeans.fit(X)
    labels = kmeans.labels_

    # Create a dictionary to store the product URLs by cluster label
    groups = {}
    for i, label in enumerate(labels):
        if label not in groups:
            groups[int(label)] = []
        groups[int(label)].append(urls[i])




    # convert the dictionary to JSON format with new line separators
    json_result = json.dumps(groups, indent=6, separators=(',', ':'),sort_keys=True)

    # save the JSON string to a file
    with open('glamaroustitijewels_alternate.json', 'w') as f:
        f.write(json_result)

    # Convert the groups dictionary to a JSON object and return it
    return json.dumps(groups)


store_domain = 'https://glamaroustitijewels.com'
alternates = FindAlternateGroups(store_domain)
print(alternates)
