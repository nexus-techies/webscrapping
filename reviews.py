from selectorlib import Extractor
import requests
import csv
from dateutil import parser as dateparser

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')
review_page_limit = 4
pagination_index = 10

def scrape(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    return e.extract(r.text)


def create_urllist(url):
    if "amazon" in url.lower():
        return url + "&pageNumber="
    else:
        return url + "&page="

with open("urls.txt",'r') as urlfile, open('data.csv','w', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["title","content","date","variant","images","verified","author","rating","product","url"],quoting=csv.QUOTE_ALL)
    writer.writeheader()
    url_raw = urlfile.readlines()[0]

    for i in range(review_page_limit):
        url = create_urllist(url_raw) + str(i)
        data = scrape(url)
        if data:
            try:
                for r in data['reviews']:
                    r["product"] = data["product_title"]
                    r['url'] = url
                    if 'verified' in r and r['verified']:
                        if 'Verified Purchase' in r['verified']:
                            r['verified'] = 'Yes'
                        else:
                            r['verified'] = 'Yes'
                    else:
                        r['verified'] = 'No'
                    r['rating'] = r['rating'].split(' out of')[0]
                    date_posted = r['date'].split('on ')[-1]
                    if r['images']:
                        r['images'] = "\n".join(r['images'])
                    r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
                    writer.writerow(r)
            except TypeError:
                break
