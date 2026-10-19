# Autogen Webscraping

Takes a full-page screenshot of any URL with Puppeteer (`screenshot.js`), then sends the image to a vision-capable AutoGen agent and asks it a question about the page (e.g. "list all the items and their prices").

Updated to AutoGen v0.7 (the new `autogen_agentchat` API).

## Run it

```bash
pip install -r requirements.txt
npm install            # installs puppeteer for screenshot.js
```

Put your `OPENAI_API_KEY` in a `.env` file, then:

```bash
python vision_crawl.py
```

You'll be asked for the URL, what you want from it, and a file name for the screenshot (e.g. `screenshots/publix.jpg`).
