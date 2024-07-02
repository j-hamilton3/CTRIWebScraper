import requests 
from html.parser import HTMLParser
import pandas as pd
import cloudscraper

class BlogPageScraper(HTMLParser):
    """An HTMLParser class used to scraper Blog page data."""

    def __init__(self):
        super().__init__()
        self.image = []
        self.content = []
        self.trainer = []

        self.image_flag = False
        self.content_flag = False
        self.trainer_flag = False

    def handle_starttag(self, tag, attrs):
        pass

    def handle_data(self, data):
        pass

    def handle_endtag(self, tag):
        pass

    def get_blog_information(self):
        return {
            "blog_image": ' '.join(self.image),
            "blog_content": ' '.join(self.content),
            "blog_trainer":' '.join(self.trainer),
        }

def fetch_blog_description_page(url):
    cloud_scraper = cloudscraper.create_scraper()
    response = cloud_scraper.get(url)

    html_content = response.content.decode('utf-8')

    return html_content

if __name__ == "__main__":
    pass