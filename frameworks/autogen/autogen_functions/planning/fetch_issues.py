# filename: fetch_issues.py

import requests
import json


def fetch_issues():
    url = "https://api.github.com/repos/microsoft/FLAML/issues"
    params = {
        "state": "open",
        "labels": "good first issue"
    }
    response = requests.get(url, params=params)
    issues = response.json()
    for issue in issues:
        print(f"Issue ID: {issue['id']}, Title: {issue['title']}, URL: {issue['html_url']}")


fetch_issues()
