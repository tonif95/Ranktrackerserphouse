import requests
import json
import re
import pandas as pd
import datetime
import os

# Ask the user for their domain
dominio = input("Enter your website's domain: ")

# Ask the user for the queries separated by comma
queries = input("Enter the keywords separated by comma: ")
queries = queries.split(',')

# Initialize a list to store the results
results = []

for query in queries:
    url = 'https://api.serphouse.com/serp/live'
    params = {
        'q': query,
        'domain': 'google.com',
        'lang': 'es',
        'device': 'desktop',
        'serp_type': 'web',
        'loc': 'Madrid-Torrejon Airport,Community of Madrid,Spain',
        'loc_id': '9041200',
        'verbatim': '0',
        'gfilter': '0',
        'page': '1',
        'num_result': '100',
        'api_token': '[Enter your API token]'
    }
    headers = {
      'Authorization': 'Bearer {token}'
    }
        
    response = requests.request('GET', url, headers=headers, params=params)        
    data = json.loads(response.text)
    data_str = str(data)    
    urls = re.findall(r'\'link\': \'https://(?!www.google)\S+\'', data_str)
    positions = re.findall(r'\'position\':\s(\d+)', data_str)
    dictionary = {}
    for url, position in zip(urls, positions):
        dictionary[position] = url.split("'")[3]
        data = json.loads("{}")

    found = False
    for position, url in dictionary.items():
        if dominio in url:
            results.append({"query": query, "position": position, "date": datetime.datetime.now().strftime('%d-%m-%Y')})
            found = True            
            break

    if not found:
        resultados.append({"query": query, "position": position, "date": datetime.datetime.now().strftime('%d-%m-%Y')})

# Create a dataframe from the list of results
df = pd.DataFrame(results)

# Check if the results.csv file exists
if os.path.exists('results.csv'):
    # If it exists, append the new results without writing the headers
    df.to_csv('results.csv', index=False, mode='a', header=False)
else:
    # If it does not exist, create the file and write the headers
    df.to_csv('results.csv', index=False, mode='w', header=True)
