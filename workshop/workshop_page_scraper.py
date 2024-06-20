import requests
from html.parser import HTMLParser
import pandas as pd

class WorkshopPageScraper(HTMLParser):
    """An HTMLParser class used to scrape Workshop page data."""

    def __init__(self):
        super().__init__()
        self.subtitle = []
        self.price = []
        self.credit_hours = []
        self.trainer = []
        self.learning_objectives = []
        self.topics_reviewed = []
        self.target_audience = []


        self.subtitle_flag = False
        self.price_flag = False
        self.credit_hours_flag = False
        self.trainer_flag = False
        self.learning_objectives_flag = False
        self.topics_reviewed_flag = False
        self.target_audience_flag = False
        

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            for attr in attrs:
                if attr[1] == "podcast__text__content":
                    self.description_flag = True
        
        if tag == "source" and not self.audio_path:
            for attr in attrs:
                self.audio_path.append(attr[1])

    def handle_data(self, data):
        if self.price_flag:
            self.price.append(data)
    
    def handle_endtag(self, tag):
        if tag == "p":
            self.description_flag = False

    def get_workshop_information(self):
        return {
            "workshop_subtitle": ''.join(self.subtitle), 
            "workshop_price": ' '.join(self.price), 
            "workshop_credit_hours": ' '.join(self.credit_hours), 
            "workshop_trainer": ' '.join(self.trainer),
            "workshop_learning_objectives": ' '.join(self.learning_objectives),
            "workshop_topics_reviewed": ' '.join(self.topics_reviewed),
            "workshop_target_audience": ' '.join(self.target_audience),
        }

def fetch_workshop_description_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)

    # Check if the response content type is JSON or not
    if 'application/json' in response.headers.get('Content-Type', ''):
        json_response = response.json()
        return json_response.get('data', {}).get('posts', '') 
    else:
        return response.text
    
if __name__ == "__main__":
    html = fetch_workshop_description_page("https://ctrinstitute.com/product/on-demand-workshop-addictions-and-mental-health/?utm_medium=cpc&utm_source=google&utm_campaign=ctri-branded")
    
    parser = WorkshopPageScraper()
    parser.feed(html)

    print(parser.get_workshop_information())