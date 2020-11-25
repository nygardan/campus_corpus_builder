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
    error_list = ['\n########\n',]
    keyword1='covid'
    keyword2='coronavirus'
    try:
        url = parse_url(url)
        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.text, 'lxml')
        links = [url]
        links += soup.find_all('a', attrs={'href': re.compile("^http")})

        for link in links:
            try:
                if isinstance(link, str):
                    address = link
                else:
                    address = link.get('href')
                page = requests.get(address, timeout=5)
                soup = BeautifulSoup(page.text, 'lxml')
                text = soup.find_all('p')
                new_list = [t.get_text() for t in text if keyword1 in t.get_text().lower() or keyword2 in t.get_text().lower()]
                print(new_list)
                output_list += new_list
                # for t in text:
                #     u = t.get_text()
                #     if keyword1 in u.lower() or keyword2 in u.lower():
                #         output_list.append(u)
            except Exception as e:
                print(str(e))
                error_list.append(str(e))
        print(output_list)
        print(error_list)
        return output_list, error_list

    except Exception as e:
        error_list.append(str(e))
        return output_list, error_list
