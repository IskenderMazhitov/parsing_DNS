import csv
import requests
from bs4 import BeautifulSoup as BS


headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
INIT_URL = "https://www.planeta.kg"


def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['category'], data['title'], data["price"], data['image']))


def get_html(url):
    res = requests.get(url, headers=headers).text
    return BS(res, "lxml")


def get_sub_categories(url):
    html = get_html(url)
    sub_categories = html.find_all('div', {"class": "product"})
    return [sc.find('a').get('href') for sc in sub_categories]


def get_init_categories(html):
    parent = html.find('div', {'class': 'sub-menu'})
    categories = parent.find_all('a')
    return [c.get('href') for c in categories]


def get_product(url):
    html = get_html(url)
    products = html.find_all('div', {'class': 'card-product'})
    if not products:
        return

    data = {}
    for product in products:
        img = product.find('div', {'class': 'img-rating-stock'}).find('img').get('src')
        data["image"] = INIT_URL + img
        data["title"] = product.find('p', {"class": "name"}).text
        data["price"] = product.find('div', {"class": "price"}).text.replace('\n', '').strip()
        data["category"] = url.split('/')[-2]
        write_to_csv(data)


def main():
    html = get_html(INIT_URL)
    init_categories = get_init_categories(html)
    for init_category in init_categories:

        products = get_product(INIT_URL + init_category)
        if not products:
            categories = get_sub_categories(INIT_URL + init_category)
            for category in categories:

                products = get_product(INIT_URL + category)
                if not products:
                    sub_categories = get_sub_categories(INIT_URL+category)
                    for sub_category in sub_categories:

                        products = get_product(INIT_URL + sub_category)
                        if not products:

                            sub_sub_categories = get_sub_categories(INIT_URL + sub_category)
                            for sub_sub_category in sub_sub_categories:
                                products = get_product(INIT_URL + sub_sub_category)
                                if not products:
                                    print("Sorry")


if __name__ == "__main__":
    with open('data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('category', 'title', 'price', 'image'))
    main()
