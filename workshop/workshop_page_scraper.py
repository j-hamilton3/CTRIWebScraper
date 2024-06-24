import requests
from html.parser import HTMLParser
import pandas as pd
import cloudscraper

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

        # Subtitles
        if tag == "h3":
            for attr in attrs:
                if attr[1] == "top-title__subtitle":
                    self.subtitle_flag = True

        # Price
        if tag == "div":
            for attr in attrs:
                if attr[1] == " product-price":
                    self.price_flag = True

        # Credit Hours
        if tag == "div":
            for attr in attrs:
                if attr[1] == "on-demand-workshop__credit-hours--hours":
                    self.credit_hours_flag = True
        
        # Trainer
        if tag == "p":
            for attr in attrs:
                if attr[1] == "on-demand-workshop__trainer":
                    self.trainer_flag = True
    
    def handle_data(self, data):

        # Subtitles
        if self.subtitle_flag:
            self.subtitle.append(data)

        # Price
        if self.price_flag:
            self.price.append(data.strip())

        # Credit Hours
        if self.credit_hours_flag:
            self.credit_hours.append(data)

        # Trainer
        if self.trainer_flag:
            self.trainer.append(data.replace("\n", " ").replace("Trainer:", "").strip()) # May need to format spaces.

    def handle_endtag(self, tag):

        # Subtitles
        if tag == "h3":
            self.subtitle_flag = False
        
        # Price
        if tag == "div":
            self.price_flag = False
            self.credit_hours_flag = False
        
        # Trainer
        if tag == "p":
            self.trainer_flag = False

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
    cloud_scraper = cloudscraper.create_scraper()
    response = cloud_scraper.get(url)

    html_content = response.content.decode('utf-8')

    return html_content
    
    
if __name__ == "__main__":
    html = fetch_workshop_description_page("https://ctrinstitute.com/product/on-demand-workshop-addictions-and-mental-health/")
    parser = WorkshopPageScraper()
    parser.feed(html)

    print(parser.get_workshop_information())