# filename: search_arxiv_papers.py
import requests

# Define the search query
query = "trust calibration AI"

# Make a request to the arXiv API
url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results=10"
response = requests.get(url)

# Parse the XML response to extract paper titles and links
from xml.etree import ElementTree as ET
root = ET.fromstring(response.content)

for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
    title = entry.find('{http://www.w3.org/2005/Atom}title').text
    link = entry.find('{http://www.w3.org/2005/Atom}id').text
    print(f"Title: {title}\nLink: {link}\n")
