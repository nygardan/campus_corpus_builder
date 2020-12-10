# Crawl and scrape tutorials and base code:
# https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3
# Finalized for CSCI 765 12-9-2020, by Dan Nygard

from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import re

# Since our college websites come in different forms, this parses them into a URL
def parse_url(url):
    if url.startswith('https:'):
        return url
    elif url.startswith('www'):
        return 'https://' + url
    else:
        return 'https://www.' + url


# Our scraper pulls <p> html elements containing the words 'covid' or 'coronavirus'.
def web_scrape(url):
    output_list = []
    error_list = ['\n########\n',]
    keyword1='covid'
    keyword2='coronavirus'

    try:
        # Gather our links. We are set up to scrape two levels (the home page and all links on the home page)
        # Going further levels deep is fairly easy to code, but difficult to wait for the scrape results
        # as the number of links to scrape increases immensely with each level.
        url = parse_url(url)
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, 'lxml')
        links = [url]
        links += soup.find_all('a', attrs={'href': re.compile("^http")})

        # Scrape each link
        for link in links:
            try:
                if isinstance(link, str):
                    address = link
                else:
                    address = link.get('href')
                page = requests.get(address, timeout=5)                
                # The lxml parser should speed things up over the standard soup parser
                soup = BeautifulSoup(page.text, 'lxml')                
                # Get all text in the <p> elements
                text = soup.find_all('p', text=True)
                search_list = [t.get_text() for t in text]
                # Evaluate if a <p> element has covid :)
                new_list = [t for t in search_list if keyword1 in t.lower() or keyword2 in t.lower()]
                # This helps when you're watching the terminal - you can see progress through the scrape
                print(new_list)
                output_list += new_list
            except Exception as e:
                print(str(e))
                error_list.append(str(e))
        # Remove duplicates before returning the output_list.
        output_list = list(OrderedDict.fromkeys(output_list))

        # Give the terminal a final result and return the lists.
        print(output_list)
        print(error_list)
        return output_list, error_list

    except Exception as e:
        error_list.append(str(e))
        return output_list, error_list
