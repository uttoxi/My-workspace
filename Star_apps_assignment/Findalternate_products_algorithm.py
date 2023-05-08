import requests
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import json


def FindAlternateGroups(store_domain):
    # Make a request to the store domain
    response = requests.get(store_domain + '/collections/all//products.json')

    data = response.json()

    # Extract the product URLs from the JSON data
    urls = []
    for product in data['products']:
        urls.append(store_domain + '/products/' + product['handle'])

    # Parse the HTML of each product page and extract the product names,catagory,tags
    names = []
    catagory =[]
    tags = []

    for product in data["products"]:
        title = product["title"]
        ptype = product["product_type"]
        tag = product["tags"]


        names.append(title.strip())
        catagory.append(ptype)

        tags.append(tag)





    # Use K-means clustering to group the product URLs by name similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(names,tags)
    kmeans = KMeans(n_clusters=18, n_init=500,max_iter=200000,tol=0.005,random_state=4000)

    kmeans.fit(X)
    labels = kmeans.labels_

    # Create a dictionary to store the product URLs by cluster label
    groups = {}
    for i, label in enumerate(labels):
        if label not in groups:
            groups[int(label)] = []
        groups[int(label)].append(urls[i])




    # Remove keys with length= 1, convert the dictionary to JSON format with new line separators
   
    for key in list(groups.keys()):
        # Check the length of the value
        if len(groups[key]) == 1:
            # Remove the key if the length is 1
            del groups[key]
    json_result = json.dumps(groups, indent=6, separators=(',', ':'),sort_keys=True)

    # save the JSON string to a json file
    with open('Alternate1.json', 'w') as f:
        f.write(json_result)

    # Convert the groups dictionary to a JSON object and return it
    return json.dumps(groups)


store_domain =  'https://boysnextdoor-apparel.co'
#               'https://boysnextdoor-apparel.co'
#               'https://www.woolsboutiqueuomo.com'
#               'https://sartale2022.myshopify.com'
#               'https://berkehome.pl'
#               'https://glamaroustitijewels.com'
#               'https://lampsdepot.com'
#               'https://kitchenoasis.com'
alternates = FindAlternateGroups(store_domain)
print(alternates)
