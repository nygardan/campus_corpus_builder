# Crawl and scrape tutorials and base code:
# https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3

from bs4 import BeautifulSoup
import requests
import re

def parse_url(url):
    if url.startswith('https:'):
        return url 
    elif url.startswith('www'):
        return 'https://' + url
    else:
        return 'https://www.' + url

def web_scrape(url):
    output_list = []
    keyword1='covid'
    keyword2='coronavirus'
    try:
        page = requests.get(parse_url(url), timeout=5)
        soup = BeautifulSoup(page.text, 'lxml')
        links = soup.find_all('a', attrs={'href': re.compile("^http")})
        text = soup.find_all('p')
        
        for t in text:
            u = t.get_text()
            if keyword1 in u.lower() or keyword2 in u.lower():
                output_list.append(u)

        for link in links:
            try:
                address = link.get('href')
                page = requests.get(address, timeout=5)
                soup = BeautifulSoup(page.text, 'lxml')
                text = soup.find_all('p')
                for t in text:
                    u = t.get_text()
                    if keyword1 in u.lower() or keyword2 in u.lower():
                        output_list.append(u)
            except Exception as e:
                output_list.append(str(e))
            
        return output_list
    
    except Exception as e:
        output_list.append(str(e))
        return output_list
