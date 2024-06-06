import requests
from html.parser import HTMLParser
import pandas as pd
import os

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
        print(f"Fetching page {page_number}...")
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

###########################

def get_desktop_path():
    """Get the path to the user's desktop directory."""
    return os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')

all_workshops = fetch_all_workshops()
print("**********************************")
print(f"*** Found {len(all_workshops)} workshops!")
print("**********************************")
for workshop in all_workshops:
    print(f"{workshop['Title']} - {workshop['URL']}")

print("*********************************")
print("*** Exporting to excel file.")
print("*********************************")

# Get the path to user's desktop.
desktop_path = get_desktop_path()
output_file = os.path.join(desktop_path, 'workshop_titles_and_links.xlsx')

# Export workshop data to excel file.
df = pd.DataFrame(all_workshops)
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Workshops', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Workshops']

    for idx, url in enumerate(df['URL'], start=2):
        worksheet.write_url(f'B{idx}', url)

print("Workshop titles and links have been exported to workshop_titles_and_links.xlsx in your documents folder.")

# Open the created Excel file.
if os.name == 'nt':  # Windows
    os.startfile(output_file)
    os.startfile(output_file)
