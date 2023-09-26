import requests
import json
import pandas as pd

# user key
user_key = "bd327e31a3b0a4148ccdc00fdeb89969"


query={
    "field_ids": [
        "facet_ids",
        "uuid",
        "location_identifiers",
        "short_description",
        "linkedin"
    ],
    "query": [
        {
            "type": "predicate",
            "field_id": "location_identifiers",
            "operator_id": "includes",
            "values": [
                "6106f5dc-823e-5da8-40d7-51612c0b2c4e"  # UUID for Europe
            ]
        },
        {
            "type": "predicate",
            "field_id": "categories",
            "operator_id": "includes",
            "values": [
                "b8ca872c-983d-f8dd-3639-2660511203ef"# Category 1 ID
            ]
        },
        {
            "type": "predicate",
            "field_id": "facet_ids",
            "operator_id": "includes",
            "values": [
                "company"
            ]
        }
    ],
    "limit": 3

}


headers = {
    "X-cb-user-key":user_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

url = "https://api.crunchbase.com/api/v4/searches/organizations"
response = requests.post(url, headers=headers, json=query)

# Check the response
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)

companies_data = []

entities = data['entities']
for entity in entities:
    company_data = {
        'company': entity['properties']['identifier']['value'],
        'short desc': entity['properties']['short_description'],
        'linkedin': entity['properties']['linkedin']['value']
    }
    companies_data.append(company_data)

df = pd.DataFrame(companies_data)

df.to_csv('company_data.csv', index=False)