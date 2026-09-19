# filename: plot_countries.py

import pandas as pd
import matplotlib.pyplot as plt

# Read countries and land masses from a CSV file.
data = pd.read_csv('countries.csv')

# Convert 'Land_Mass' to numeric, this will convert 'None' to 'NaN'
data['Land_Mass'] = pd.to_numeric(data['Land_Mass'], errors='coerce')

# Sort countries by land mass in descending order
# This will omit the countries with 'NaN' area
data_sorted = data.sort_values('Land_Mass', ascending=False)

# Select the top 10 countries with the largest land mass
top_10 = data_sorted.head(10)

# Plot a horizontal bar chart
plt.barh(top_10['Country'], top_10['Land_Mass'], color='blue')
plt.xlabel('Land Mass')
plt.ylabel('Country')
plt.title('Top 10 Countries by Land Mass')
plt.gca().invert_yaxis()
plt.show()