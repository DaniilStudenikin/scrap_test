import json

import requests
from bs4 import BeautifulSoup
import re


def parse_products(response):
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'id': 'tabGoods'})
    trs = table.find_all('tr', {'style': [' background:none;', ' ']})
    indexes = (i for i in range(len(trs)))
    print(response.url)
    data = list()
    current_name = ''
    for i, elem in zip(indexes, trs):
        curname = elem.find('a', class_='goodlnk')
        print(curname)
        if curname is not None:
            current_name = curname.text

        article = elem.find('input', {'id': f'ecomCode{i + 1}'}).get('value')
        brand = elem.find('input', {'id': f'ecomManuf{i + 1}'}).get('value')
        id = elem.find('input', {'id': f'g{i + 1}'}).get('value')
        count = elem.find('span', {'href': '#'}).text
        time = elem.find('td', class_='hidden-sm hidden-xs article').text
        if time != 'Ожидается':
            time = re.sub("[^0-9]", "", time)

        price = elem.find('span', {'id': f'sp{i + 1}'}).text
        array = dict()
        array['name'] = current_name
        array['price'] = price
        array['article'] = article
        array['brand'] = brand
        array['count'] = count
        array['time'] = int(time)
        array['id'] = id
        data.append(array)
    return data


def main(name):
    url = f'https://www.autozap.ru/goods?code={name}&count=300&page=1&search=Найти'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data = list()

    if soup.find('h3', {'style': 'margin-bottom:0px;'}) is not None:
        url = "https://www.autozap.ru" + soup.find('tr',
                                                   {"onclick": "document.getElementById('goodLnk1').click();"}).find(
            'a').get('href')
        resp = requests.get(url)
        data = parse_products(resp)
    elif soup.find('h4', {'style': 'margin-bottom:0px;'}) is not None:
        data = parse_products(response)

    with open(f'{name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=3, ensure_ascii=False)

    print('Done!')


if __name__ == '__main__':
    itemName = input("Введите артикул товара: ")
    main(itemName)
