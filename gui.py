from blog.blog_scraper import blogs_to_excel
from book.book_scraper import books_to_excel
from handout.printable_handouts_scraper import handouts_to_excel
from podcast.podcast_scraper import podcasts_to_excel
from topic.topic_scraper import topics_to_excel
from webinar.webinar_scraper import webinars_to_excel
from workshop.workshop_scraper import workshops_to_excel
from combined_scraper import all_resources_to_excel
from tkinter import *


root = Tk()
root.title("CTRI Web Scraper")

all_data_label = Label(root, text='Scrape all data from ctrinstitute.com:')
all_data_time_warning = Label(root, text='(This takes around 8 minutes...)')
all_data_label.pack()
all_data_time_warning.pack()

all_data_button = Button(root, text="Get All Data")
all_data_button.pack()

specific_data_label = Label(root, text='Scrape specific data from ctrinstitute.com:')
specific_data_label.pack()

blog_data_button = Button(root, text="Get Blog Data")
blog_data_button.pack()

book_data_button = Button(root, text="Get Book Data")
book_data_button.pack()

handout_data_button = Button(root, text="Get Handout Data")
handout_data_button.pack()

podcast_data_button = Button(root, text="Get Podcast Data")
podcast_data_button.pack()

topic_data_button = Button(root, text="Get Topic Data")
topic_data_button.pack()

webinar_data_button = Button(root, text="Get Webinar Data")
webinar_data_button.pack()

workshop_data_button = Button(root, text="Get Workshop Data")
workshop_data_button.pack()

root.mainloop()

