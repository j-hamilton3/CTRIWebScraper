import requests
from html.parser import HTMLParser
import pandas as pd
import os

class HandoutsParser(HTMLParser):
    """An HTMLParser class used to scrape Printable Handouts data."""

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

    def handle_endtag(self, tag):
        if tag == "h4" and self.title_flag:
            self.title_flag = False

    def get_handouts(self):
        return self.handouts

def fetch_handouts_page():
    url = "https://ctrinstitute.com/resources/printable-handouts/"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    return response.text

def fetch_all_handouts():
    posts_html = fetch_handouts_page()

    if not posts_html:
        return []

    parser = HandoutsParser()
    parser.feed(posts_html)
    handouts = parser.get_handouts()

    return handouts

def get_documents_path():
    """Gets the path to the user's documents folder."""
    return os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')

all_handouts = fetch_all_handouts()
print("**********************************")
print(f"*** Found {len(all_handouts)} handouts!")
print("**********************************")
for handout in all_handouts:
    print(f"{handout['Title']} - {handout['URL']}")

print("*********************************")
print("*** Exporting to excel file.")
print("*********************************")

# Get the path to user's desktop.
documents_path = get_documents_path()
output_file = os.path.join(documents_path, 'handout_titles_and_links.xlsx')

# Export workshop data to excel file.
df = pd.DataFrame(all_handouts)
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Handouts', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Handouts']

    for idx, url in enumerate(df['URL'], start=2):
        worksheet.write_url(f'B{idx}', url)

print("Handout titles and links have been exported to handout_titles_and_links.xlsx in your documents folder.")

# Open the created Excel file.
if os.name == 'nt':  # Windows
    os.startfile(output_file)
    os.startfile(output_file) 