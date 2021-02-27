import os
import time
import multiprocessing

import requests
import fake_useragent
from bs4 import BeautifulSoup

file_list = os.listdir('../data')
data = {}
if not os.path.exists('../metas'):
    os.mkdir('../metas')

# разбить все на методы, сделать метод run(), запустить в multiprocessing


def extract_page_data(soup: BeautifulSoup) -> list:
    title = soup.title.string
    h1 = str(soup.find('h1').contents[0])
    descr = str(soup.find('meta', attrs={'name': 'description'})['content'])
    pagination_block = soup.find('div', class_='pagination__inner')
    pagination_pages = pagination_block.contents
    if pagination_pages[len(pagination_pages) - 2].contents[0] == '...':
        number_of_pages = pagination_pages[len(pagination_pages) - 3].contents[0]
    else:
        number_of_pages = pagination_pages[len(pagination_pages) - 2].contents[0]
    prods_quantity = int(number_of_pages) * 24
    data_list = [title, h1, descr, prods_quantity]
    return data_list


for file in file_list:
    data[file] = {}
    session = requests.Session()
    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    file_path = os.path.join('../data/', file)

    with open(file_path) as f:
        with open(f'../metas/meta_{file}', 'w', encoding='utf-8') as m:
            m.write('URL;Title;H1;Description;Products Quantity;Prod Quantity over 40;Status code\n')
            link_num = 0
            for link in f:
                start_time = time.time()
                link = link.strip()
                response = session.get(link, headers=headers)
                if response.status_code == 404:
                    m.write(f'{link};DEFAULT;NO H1;NO DESCRIPTION;NO PRODUCTS;False;{response.status_code}\n')
                    continue
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'lxml')
                data[file][link] = extract_page_data(soup)
                response2 = session.get(link + '?offset=24', headers=headers)
                response2.encoding = 'utf-8'
                soup2 = BeautifulSoup(response2.text, 'lxml')
                prods_number = 24
                prods = soup2.find_all('article', class_='product__item group')
                if len(prods) > 15:
                    data[file][link].append(True)
                else:
                    data[file][link].append(False)

                title = data[file][link][0].strip()
                h1 = data[file][link][1].strip()
                descr = data[file][link][2].strip()
                prod_num = data[file][link][3]
                prods_num_over_40 = data[file][link][4]
                m.write(f'{link};{title};{h1};{descr};{prod_num};{prods_num_over_40};{response.status_code}\n')
                link_num += 1
                print(f'Number of URLs processed: {link_num} ({time.time() - start_time:.2f} seconds)')
    print(f'Data for file {file} was collected')


# def separate_large_files():
#     meta_files = os.listdir('../data')
#     for file in meta_files:
#         with open(f'../data/{file}') as f:
#             for i, l in enumerate(f):
#                 pass
#             if i > 1499:
#                 filenumber = 1

