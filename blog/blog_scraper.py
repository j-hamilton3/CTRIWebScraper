import requests
from html.parser import HTMLParser
import pandas as pd
import os

class BlogParser(HTMLParser):
    """An HTMLParser class used to parse blog data."""

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
            self.blogs.append({"Title": data, "URL": self.current_url})
            self.blog_title_flag = False
            self.current_url = None

    def handle_endtag(self, tag):
        if tag == "h3" and self.blog_title_flag:
            self.blog_title_flag = False

    def get_blogs(self):
        return self.blogs

def fetch_blog_page(page_number):
    url = "https://ctrinstitute.com/wp-admin/admin-ajax.php?action=blog_archive_filter"
    params = {
        'paged': page_number
    }
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.post(url, data=params, headers=headers)
    return response.json()

def fetch_all_blogs():
    page_number = 1
    all_blogs = []
    while True:
        print(f"Fetching page {page_number}...")
        response = fetch_blog_page(page_number)
        
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

def get_desktop_path():
    """Get the path to the user's desktop directory."""
    return os.path.join(os.path.join(os.path.expanduser('~')), 'Documents')

all_blogs = fetch_all_blogs()
print("**********************************")
print(f"*** Found {len(all_blogs)} blogs!")
print("**********************************")
for blog in all_blogs:
    print(f"{blog['Title']} - {blog['URL']}")

print("*********************************")
print("*** Exporting to excel file.")
print("*********************************")

# Get the path to user's desktop.
desktop_path = get_desktop_path()
output_file = os.path.join(desktop_path, 'blog_titles_and_links.xlsx')

# Export blog data to excel file.
df = pd.DataFrame(all_blogs)
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Blogs', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Blogs']

    for idx, url in enumerate(df['URL'], start=2):
        worksheet.write_url(f'B{idx}', url)

print("Blog titles and links have been exported to blog_titles_and_links.xlsx in your documents folder.")

# Open the created Excel file.
if os.name == 'nt':  # Windows
    os.startfile(output_file)
