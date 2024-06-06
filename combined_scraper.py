import time 
import pandas as pd
import os
import sys
import requests
from html.parser import HTMLParser

start_time = time.time()

class HandoutsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.handouts = []
        self.title_flag = False
        self.current_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_url = attr[1]
        if tag == "h4":
            for attr in attrs:
                if attr == ('class', 'h4 resources-grid__content--title'):
                    self.title_flag = True

    def handle_data(self, data):
        if self.title_flag and self.current_url:
            self.handouts.append({"Title": data.strip(), "URL": self.current_url})
            self.title_flag = False
            self.current_url = None

    def get_handouts(self):
        return self.handouts

def fetch_handouts():
    url = "https://ctrinstitute.com/resources/printable-handouts/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    parser = HandoutsParser()
    parser.feed(response.text)

    print("Fetching Handouts...")

    return parser.get_handouts()

class BlogParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blogs = []
        self.blog_title_flag = False
        self.current_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_url = attr[1]
        if tag == "h3":
            for attr in attrs:
                if attr == ('class', 'h3 blog-card__title'):
                    self.blog_title_flag = True

    def handle_data(self, data):
        if self.blog_title_flag and self.current_url:
            self.blogs.append({"Title": data.strip(), "URL": self.current_url})
            self.blog_title_flag = False
            self.current_url = None

    def get_blogs(self):
        return self.blogs

def fetch_blogs():
    page_number = 1
    all_blogs = []
    while True:
        print(f"Fetching Blog: page {page_number}...")
        response = requests.post("https://ctrinstitute.com/wp-admin/admin-ajax.php?action=blog_archive_filter", data={'paged': page_number}, headers={'User-Agent': 'Mozilla/5.0'}).json()
        posts_html = response['data']['posts']
        if not posts_html:
            break
        parser = BlogParser()
        parser.feed(posts_html)
        blogs = parser.get_blogs()
        if not blogs:
            break
        all_blogs.extend(blogs)
        page_number += 1
    return all_blogs

class BookParser(HTMLParser):
    """An HTMLParser class used to scrape Book data."""

    def __init__(self):
        super().__init__()
        self.books = []
        self.title_flag = False
        self.current_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_url = attr[1]

        if tag == "h3":
            for attr in attrs:
                if attr == ('class', 'h3 book-card__title'):
                    self.title_flag = True

    def handle_data(self, data):
        if self.title_flag and self.current_url:
            self.books.append({"Title": data.strip(), "URL": self.current_url})
            self.title_flag = False
            self.current_url = None

    def handle_endtag(self, tag):
        if tag == "h3" and self.title_flag:
            self.title_flag = False

    def get_books(self):
        return self.books

def fetch_book_page(page_number):
    url = "https://ctrinstitute.com/wp-admin/admin-ajax.php?action=product_archive_filter"
    params = {
        'paged': page_number,
        'filter_term': 47
    }
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return None

    # Check if the response content type is JSON or not
    if 'application/json' in response.headers.get('Content-Type', ''):
        json_response = response.json()
        return json_response.get('data', {}).get('posts', '') 
    else:
        return response.text

def fetch_all_books():
    page_number = 1
    all_books = []
    while True:
        print(f"Fetching Book : page {page_number}...")
        posts_html = fetch_book_page(page_number)

        if not posts_html:
            break

        parser = BookParser()
        parser.feed(posts_html)
        books = parser.get_books()

        if not books:
            break
        all_books.extend(books)
        page_number += 1
    return all_books

class PodcastParser(HTMLParser):
    """An HTMLParser class used to scrape Podcast data."""

    def __init__(self):
        super().__init__()
        self.podcasts = []
        self.title_flag = False
        self.current_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_url = attr[1]

        if tag == "h3":
            for attr in attrs:
                if attr == ('class', 'podcast-card__title'):
                    self.title_flag = True

    def handle_data(self, data):
        if self.title_flag and self.current_url:
            self.podcasts.append({"Title": data.strip(), "URL": self.current_url})
            self.title_flag = False
            self.current_url = None

    def handle_endtag(self, tag):
        if tag == "h3" and self.title_flag:
            self.title_flag = False

    def get_podcasts(self):
        return self.podcasts

def fetch_podcast_page(page_number):
    url = "https://ctrinstitute.com/wp-admin/admin-ajax.php?action=podcast_archive_filter"
    params = {
        'paged': page_number
    }
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return None

    # Check if the response content type is JSON or not
    if 'application/json' in response.headers.get('Content-Type', ''):
        json_response = response.json()
        return json_response.get('data', {}).get('posts', '') 
    else:
        return response.text

def fetch_all_podcasts():
    page_number = 1
    all_podcasts = []
    while True:
        print(f"Fetching Podcast : page {page_number}...")
        posts_html = fetch_podcast_page(page_number)

        if not posts_html:
            break

        parser = PodcastParser()
        parser.feed(posts_html)
        podcasts = parser.get_podcasts()

        if not podcasts:
            break
        all_podcasts.extend(podcasts)
        page_number += 1
    return all_podcasts

class WorkshopParser(HTMLParser):
    """An HTMLParser class used to scrape Workshop data."""

    def __init__(self):
        super().__init__()
        self.workshops = []
        self.title_flag = False
        self.current_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_url = attr[1]

        if tag == "h3":
            for attr in attrs:
                if attr == ('class', 'h3 book-card__title'):
                    self.title_flag = True

    def handle_data(self, data):
        if self.title_flag and self.current_url:
            self.workshops.append({"Title": data.strip(), "URL": self.current_url})
            self.title_flag = False
            self.current_url = None

    def handle_endtag(self, tag):
        if tag == "h3" and self.title_flag:
            self.title_flag = False

    def get_workshops(self):
        return self.workshops

def fetch_workshop_page(page_number):
    url = "https://ctrinstitute.com/wp-admin/admin-ajax.php?action=product_archive_filter"
    params = {
        'paged': page_number,
        'filter_term': 34
    }
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return None

    # Check if the response content type is JSON or not
    if 'application/json' in response.headers.get('Content-Type', ''):
        json_response = response.json()
        return json_response.get('data', {}).get('posts', '') 
    else:
        return response.text

def fetch_all_workshops():
    page_number = 1
    all_workshops = []
    while True:
        print(f"Fetching Workshop: page {page_number}...")
        posts_html = fetch_workshop_page(page_number)

        if not posts_html:
            break

        parser = WorkshopParser()
        parser.feed(posts_html)
        workshops = parser.get_workshops()

        if not workshops:
            break
        all_workshops.extend(workshops)
        page_number += 1
    return all_workshops

class WebinarParser(HTMLParser):
    """An HTMLParser class used to scrape Webinar data."""

    def __init__(self):
        super().__init__()
        self.webinars = []
        self.title_flag = False
        self.current_url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.current_url = attr[1]

        if tag == "h3":
            for attr in attrs:
                if attr == ('class', 'h3 book-card__title'):
                    self.title_flag = True

    def handle_data(self, data):
        if self.title_flag and self.current_url:
            self.webinars.append({"Title": data.strip(), "URL": self.current_url})
            self.title_flag = False
            self.current_url = None

    def handle_endtag(self, tag):
        if tag == "h3" and self.title_flag:
            self.title_flag = False

    def get_webinars(self):
        return self.webinars

def fetch_webinar_page(page_number):
    url = "https://ctrinstitute.com/wp-admin/admin-ajax.php?action=product_archive_filter"
    params = {
        'paged': page_number,
        'filter_term': 33
    }
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return None

    # Check if the response content type is JSON or not
    if 'application/json' in response.headers.get('Content-Type', ''):
        json_response = response.json()
        return json_response.get('data', {}).get('posts', '') 
    else:
        return response.text

def fetch_all_webinars():
    page_number = 1
    all_webinars = []
    while True:
        print(f"Fetching Webinar: page {page_number}...")
        posts_html = fetch_webinar_page(page_number)

        if not posts_html:
            break

        parser = WebinarParser()
        parser.feed(posts_html)
        webinars = parser.get_webinars()

        if not webinars:
            break
        all_webinars.extend(webinars)
        page_number += 1
    return all_webinars

# Create/find the excel spreadsheet
def get_documents_path():
    return os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')

documents_path = get_documents_path()
output_file = os.path.join(documents_path, 'ctri_web_data.xlsx')

if (os.path.exists(output_file)):
    print("The ctri_web_data.xlsx file already exists.")
    print("Running this script will overwrite it.")
    will_overwrite = input("Please type YES to continue: ")
    will_overwrite = will_overwrite.upper().strip()

    if (will_overwrite != "YES"):
        input("Press ENTER to exit.")
        sys.exit()
    
try:
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        
        print("**** SCRAPING DATA FROM CTRINSTITUTE.COM ****")
        print("This will take a minute...")

        # Fetch and write workshops.
        workshops = fetch_all_workshops()
        df_workshops = pd.DataFrame(workshops)
        df_workshops.to_excel(writer, sheet_name="Workshops", index=False)
        worksheet = writer.sheets['Workshops']
        for idx, url in enumerate(df_workshops['URL'], start=2):
            worksheet.write_url(f'B{idx}', url)

        # Fetch and write webinars.
        webinars = fetch_all_webinars()
        df_webinars = pd.DataFrame(webinars)
        df_webinars.to_excel(writer, sheet_name="Webinars", index=False)
        worksheet = writer.sheets['Webinars']
        for idx, url in enumerate(df_webinars['URL'], start=2):
            worksheet.write_url(f'B{idx}', url)

        # Fetch and write blogs.
        blogs = fetch_blogs()
        df_blogs = pd.DataFrame(blogs)
        df_blogs.to_excel(writer, sheet_name='Blogs', index=False)
        worksheet = writer.sheets['Blogs']
        for idx, url in enumerate(df_blogs['URL'], start=2):
            worksheet.write_url(f'B{idx}', url)

        # Fetch and write books.
        books = fetch_all_books()
        df_books = pd.DataFrame(books)
        df_books.to_excel(writer, sheet_name="Books", index=False)
        worksheet = writer.sheets['Books']
        for idx, url in enumerate(df_books['URL'], start=2):
            worksheet.write_url(f'B{idx}', url)

        # Fetch and write podcasts.
        podcasts = fetch_all_podcasts()
        df_podcasts = pd.DataFrame(podcasts)
        df_podcasts.to_excel(writer, sheet_name="Podcasts", index=False)
        worksheet = writer.sheets['Podcasts']
        for idx, url in enumerate(df_podcasts['URL'], start=2):
            worksheet.write_url(f'B{idx}', url)

        # Fetch and write handouts.
        handouts = fetch_handouts()
        df_handouts = pd.DataFrame(handouts)
        df_handouts.to_excel(writer, sheet_name='Handouts', index=False)
        worksheet = writer.sheets['Handouts']
        for idx, url in enumerate(df_handouts['URL'], start=2):
            worksheet.write_url(f'B{idx}', url)

    end_time = time.time()
    runtime = end_time - start_time


    print(f"**** SCRAPING COMPLETED in {round(runtime, 2)} seconds. ****")
    print("Data has been exported to ctri_web_data.xlsx in your documents folder.")

    # Open the created Excel file.
    if os.name == 'nt':  # Windows
        os.startfile(output_file)
    
except PermissionError:
    print("PERMISSION ERROR : Please close the ctri_web_data.xlsx file to and rerun this script.")