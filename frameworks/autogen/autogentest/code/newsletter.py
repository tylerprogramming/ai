# Step 1: Set up a Flask project with necessary dependencies
from flask import Flask
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


# Step 2: Create a web scraper to retrieve news articles from the specified websites
def scrape_news():
    news_articles = []

    # Retrieve news articles from https://www.ainews.co/
    ainews_url = "https://www.ainews.co/"
    ainews_response = requests.get(ainews_url)
    ainews_soup = BeautifulSoup(ainews_response.text, 'html.parser')
    ainews_headlines = ainews_soup.find_all('h2', class_='entry-title')

    for headline in ainews_headlines:
        news_articles.append(headline.text.strip())

    # Retrieve news articles from https://www.aitrends.com/
    aitrends_url = "https://www.theguardian.com/technology/artificialintelligenceai"
    aitrends_response = requests.get(aitrends_url)
    aitrends_soup = BeautifulSoup(aitrends_response.text, 'html.parser')
    aitrends_headlines = aitrends_soup.find_all('h2', class_='entry-title')

    for headline in aitrends_headlines:
        news_articles.append(headline.text.strip())

    return news_articles


# Step 3: Schedule a task to run every morning at 8 AM
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_news, 'cron', hour=20, minute=3)
scheduler.start()


# Step 4: Configure the Flask app to send an email with the retrieved news articles
@app.route('/')
def send_email():
    # Retrieve news articles
    news_articles = scrape_news()

    # Create email content
    email_content = "<h1>AI News</h1>"
    for i, article in enumerate(news_articles[:3]):
        email_content += f"<h2>Article {i + 1}</h2>"
        email_content += f"<p>{article}</p>"

    print(email_content)

    # Configure email settings
    # sender_email = "sharandtyler@gmail.com"
    # sender_password = "Rcia@0716!"
    # receiver_email = "tylerreedytlearning@gmail.com"
    #
    # # Create email message
    # message = MIMEMultipart()
    # message['From'] = sender_email
    # message['To'] = receiver_email
    # message['Subject'] = "AI News"
    # message.attach(MIMEText(email_content, 'html'))
    #
    # # Send email
    # with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #     server.starttls()
    #     server.login(sender_email, sender_password)
    #     server.send_message(message)

    return "Email sent!"


if __name__ == '__main__':
    app.run()
