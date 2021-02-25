import os

import requests
import fake_useragent
from bs4 import BeautifulSoup

if not os.path.exists('data'):
    os.mkdir('data')
link = 'https://kasta.ua/sitemap.xml'

session = requests.Session()
user = fake_useragent.UserAgent().random
headers = {'user-agent': user}

sitemap_index = session.get(link, headers=headers).text
soup = BeautifulSoup(sitemap_index, 'lxml')
sitemap_links = soup.find_all('loc')

tracking_sitemaps = []
for link in sitemap_links:
    link = str(link.contents[0])
    if not 'sitemap-products' in link:
        tracking_sitemaps.append(link)

url_num = 0
for sitemap in tracking_sitemaps:
    filename = sitemap[32:-4]
    session = requests.Session()
    sitemap_content = session.get(sitemap, headers=headers).text
    soup = BeautifulSoup(sitemap_content, 'lxml')
    url_with_tags = soup.find_all('loc')
    with open('data/' + filename + '.txt', 'w') as f:
        for i in url_with_tags:
            url = str(i.contents[0])
            if not '/campaigns/' in url and not '/uk/' in url:
                f.write(url + '\n')
                url_num += 1
print("Кличество URL = ", url_num)

