import requests
from bs4 import BeautifulSoup
import feedparser
from openai import OpenAI
from pydantic import BaseModel


# def get_article_summary(url):
#     # First, try to fetch the content as a regular web page
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         # Try to parse as RSS feed
#         feed = feedparser.parse(response.content)
        
#         if feed.entries:
#             # If we have entries, it's likely an RSS feed
#             entry = feed.entries[0]
#             title = entry.title
#             description = entry.description if 'description' in entry else entry.summary if 'summary' in entry else "No description available"
            
#             # Clean up the description (remove HTML tags)
#             soup = BeautifulSoup(description, 'html.parser')
#             clean_description = soup.get_text()
            
#             return f"Title: {title}\nSummary: {clean_description}"
#         else:
#             # If no entries, it might be a regular HTML page
#             soup = BeautifulSoup(response.content, 'html.parser')
#             title = soup.title.string if soup.title else "No title found"
            
#             # Try to find a meta description
#             meta_desc = soup.find('meta', attrs={'name': 'description'})
#             description = meta_desc['content'] if meta_desc else "No description found"
            
#             return f"Title: {title}\nDescription: {description}"
#     else:
#         return f"Error: Unable to fetch the content. Status code: {response.status_code}"

# # URL of the Google News RSS feed or article
# url = "https://www.businessinsider.com/travis-kelce-grotesquerie-character-casting-ryan-murphy-2024-9"

# try:
#     result = get_article_summary(url)
#     print(result)
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")

def get_full_article(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("response.content", response.status_code)
            soup = BeautifulSoup(response.content, 'html.parser')

            # This part will vary depending on the website's structure
            article_body = soup.find_all('h1')  # Most websites use <p> tags for text
            article_text = "\n".join([p.get_text() for p in article_body])
            return article_text
        else:
            return f"Failed to retrieve article. Status code: {response.status_code}"
    except Exception as e:
        return str(e)
    
class Story(BaseModel):
    story: str

def get_google_news_rss(topic, limit=5):
    client = OpenAI()

    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system", "content": "You are a helpful assistant that can parse websites and return the full article text."
            },
            {
                "role": "user", "content": f"Get the RSS feed for {topic}",
            }
        ],
        response_format=Story
    )

    print(response)

# Example usage:
get_google_news_rss("https://www.businessinsider.com/travis-kelce-grotesquerie-character-casting-ryan-murphy-2024-9")