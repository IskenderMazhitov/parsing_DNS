import requests

import main


def get_img(url):
    content = requests.get(url, headers=main.headers).content
    print(content)
    return(content)

with open('data.csv') as file:
    count = 0
    for line in file.readlines():
        if count == 0:
            count += 1
            continue
        url = line.split(',')[-1].replace('\n', '')
        name = line.split(',')[1].replace('/', '')
        a = url.split('.')[-1]
        with open(f'images/{name}.{a}', 'wb') as img:
            response = get_img(url)
            img.write(response)
