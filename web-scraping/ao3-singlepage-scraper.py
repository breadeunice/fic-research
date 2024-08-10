# https://medium.com/nerd-for-tech/mining-fanfics-on-ao3-part-1-data-collection-eac8b5d7a7fa

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time
from datetime import datetime


# Record the start time
start_time = time.time()

# Setting up our parser
page = requests.get("https://archiveofourown.org/tags/ENHYPEN%20(Band)/works")
soup = BeautifulSoup(page.text, "html.parser")

# Every work is stored as an article within the DOM
works = soup.find_all("li", {"role": "article"})

# Helper function which returns a given stat (if it exists)
# Otherwise, returns default value of 0
def get_stat(stats, stat): 
    try: 
        return int(stats.find("dd", {"class": stat}).text.replace(",", ""))
    except:
        return 0

# Helper function which returns all tags of one category as string
# concatenated by commas
# Otherwise, returns default value "N/A"
def get_tags(tags, tag): 
    try: 
        tags_html = tags.find_all("li", {"class": tag})
        all_tags = ", ".join([tag.text for tag in tags_html])
        return all_tags
    except:
        return "N/A"

# We will store all results as a list of dictionaries where each 
# dictionary represents a given work
works_dict = []

# Loop through all works and collects all their information
for work in works:
    # Get title of the work
    title = work.find("h4", {"class": "heading"}).find("a").text

    # Find the author (if none, that means it's an anonymous work)
    try: 
        author = work.find("h4", {"class": "heading"}).find("a", {"rel": "author"}).text
    except: 
        author = 'anonymous'

    # Get ID of work
    work_id = work.find("h4", {"class": "heading"}).find("a").get("href")[7:]

    # Get last updated date
    date_updated = work.find("p", {"class": "datetime"}).text

    # Get ratings, pairing type, warning(s), and work status
    rating = work.find('span', {'class':re.compile(r'rating\-.*rating')}).text
    pairing_type = work.find('span', {'class':re.compile(r'category\-.*category')}).text
    warnings = work.find('span', {'class':re.compile(r'warning\-.*warnings')}).text
    work_status = work.find('span', {'class':re.compile(r'complete\-.*iswip')}).text

    # Get all the fandoms, convert to one string of all fandoms for work separated by commas
    fandoms_html = work.find("h5", {"class": "fandoms heading"}).find_all("a")
    fandoms = ', '.join([fandom.text for fandom in fandoms_html])

    # Gets all relationship, character, and freeform tags for a given work
    all_tags = work.find("ul", {"class": "tags commas"})
    pairings = get_tags(all_tags, "relationships")
    characters = get_tags(all_tags, "characters")
    freeform_tags = get_tags(all_tags, "freeforms")
    
    # Gets all stats (language + # chapters, words, comments, kudos, bookmarks, & hits) for a given work 
    stats = work.find("dl", {"class": "stats"})
    language = stats.find("dd", {"class": "language"}).text
    chapters_num = stats.find("dd", {"class": "chapters"}).text
    words_num = get_stat(stats, "words")
    comments_num = get_stat(stats, "comments")
    kudos_num = get_stat(stats, "kudos")
    bookmarks_num = get_stat(stats, "bookmarks")
    hits_num = get_stat(stats, "hits")

    # Get the detailed fic information (from when you actually open the fic)

    works_dict.append({"title": title, "author": author, "id": work_id, "date_updated": date_updated, 
                       "rating": rating, "pairing_type": pairing_type, "pairings": pairings, "fandoms": fandoms, 
                       "warnings": warnings, "work_status": work_status, "fandoms": fandoms, "characters": characters, 
                       "tags": freeform_tags, "language": language, "chapters_num": chapters_num, "words_num": words_num,
                       "coments_num": comments_num, "kudos_num": kudos_num, "bookmarks_num": bookmarks_num, "hits_num": hits_num})
    
quotes_df = pd.DataFrame(works_dict)
timestamp = datetime.now().strftime('%Y.%m.%d')
filename = 'results\enhypen_ao3_works' + timestamp + '.csv'
quotes_df.to_csv(filename,index=None)

# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Total time taken: {elapsed_time:.2f} seconds")
print(f"Saved to: {filename}")
print("Done!")


    




