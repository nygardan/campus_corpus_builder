# Crawl and scrape tutorials and base code:
# https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3

from bs4 import BeautifulSoup
import requests
import re


def web_scrape(url):
    
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.find_all('a', attrs={'href': re.compile("^http")})
        text = soup.find_all('p')
        output_list = []
        keyword1='covid'
        keyword2='coronavirus'
        for t in text:
            u = t.get_text()
            if keyword1 in u.lower() or keyword2 in u.lower():
                output_list.append(u)

        for link in links:
            address = link.get('href')
            page = requests.get(address)
            soup = BeautifulSoup(page.text, 'html.parser')
            text = soup.find_all('p')
            for t in text:
                u = t.get_text()
                if keyword1 in u.lower() or keyword2 in u.lower():
                    output_list.append(u)
        return output_list
    
    except:
        print("Could not complete scrape.")
