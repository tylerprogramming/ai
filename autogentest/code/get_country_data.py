# filename: get_country_data.py

import requests
import pandas as pd

# Send a GET request to the REST Countries API
response = requests.get("https://restcountries.com/v2/all")

# The response is a list of dictionaries
data = response.json()

# We're interested in the name and area (land mass)
countries = []
areas = []
for country_data in data:
    country_name = country_data.get('name')
    
    # Check if 'area' exists in the dictionary
    if 'area' in country_data:
        area = country_data.get('area')
    else:
        area = None  # Use None if the area is not available

    # Append the data to the respective list
    countries.append(country_name)
    areas.append(area)

# Create a DataFrame
df = pd.DataFrame({
    'Country': countries,
    'Land_Mass': areas
})

# Save the DataFrame in a CSV file
df.to_csv('countries.csv', index=False)