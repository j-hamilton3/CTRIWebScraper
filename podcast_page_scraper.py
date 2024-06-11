import requests
from html.parser import HTMLParser
import pandas as pd

class PodcastPageScraper(HTMLParser):
    """An HTMLParser class used to scrape Podcast page data."""

    def __init__(self):
        super().__init__()
        self.description = []
        self.description_flag = False

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            for attr in attrs:
                if attr[1] == "podcast__text__content":
                    self.description_flag = True

    def handle_data(self, data):
        if self.description_flag:
            self.description.append(data)
    
    def handle_endtag(self, tag):
        if tag == "p":
            self.description_flag = False

    def get_podcast_description(self):
        return ''.join(self.description)

def fetch_podcast_description_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    # Check if the response content type is JSON or not
    if 'application/json' in response.headers.get('Content-Type', ''):
        json_response = response.json()
        return json_response.get('data', {}).get('posts', '') 
    else:
        return response.text
    

html = fetch_podcast_description_page("https://ctrinstitute.com/podcast/episode-23-becoming-a-trauma-informed-leader/")

parser = PodcastPageScraper()

parser.feed(html)
description = parser.get_podcast_description()
print(description)