import requests
import re
import time
import numpy as np
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
}

host_url = 'https://www.moodyz.com/actress/'



def get_proxy():
    proxies = [
        'http://150.95.151.68:8195',
        'http://150.95.151.68:8191',
        'http://150.95.151.68:8282',
        'http://150.95.151.68:8299',
        'http://45.76.98.49:8118',
        'http://150.95.151.68:8186',
        'http://150.95.151.68:8288',
        'http://150.95.151.68:8192',
        'http://180.235.39.9:80',
        'http://150.95.151.68:8183',

        '',
        # 'http': 'http://207.148.108.127:80',
    ]

    # proxy = {'http:' + np.random.choice(proxies)}
    return {'http:': np.random.choice(proxies)}


def get_headers():
    headers = [
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    ]

    return {'User-Agent': np.random.choice(headers)}


def get_url(url):
    time.sleep(0.5)
    try:
        content = requests.get(url, headers=get_headers(), timeout=10, proxies=get_proxy())
        content.close()
        return BeautifulSoup(content.text, 'lxml')

    except:
        print('Connected Again .............')
        return get_url((url))


# soup = get_url('ss')
# print(soup.find_all('img', attrs={'src':re.compile('upload')}))

soup = get_url(host_url)
all_url = soup.find_all('a', attrs={'href': re.compile('actress/list')})
for url in all_url:
    postfix = url.get('href')
    base_url = 'https://www.moodyz.com'+ postfix
    soup = get_url(base_url)
    num_str = str(soup.find_all('p', attrs={'class':re.compile('pagination-tx')})[0])
    num_av = int(re.findall(re.compile('全(.*?)人'), num_str)[0])
    num_page = (num_av - 1)//30 + 1
    #match_item = soup.find_all('p')
    #tag = str(match_item[15])
    #num_av = int(re.findall(re.compile('全(.*?)ページ'), tag)[0])

    for page in range(num_page):
        print(base_url +  str(page + 1) + '/')
        soup = get_url(base_url + str(page + 1) + '/')
        imgs = soup.find_all('img', attrs={'src': re.compile('/contents/actress/')})
        for img in imgs:
            name = img.get('alt')
            img_url = 'https://www.moodyz.com' + img.get('src')
            print(img_url)
            # time.sleep(2)
            response = requests.get(img_url, headers=get_headers(), )
            response.close()
            with open('./moodyz/' + name + '.jpg', 'wb') as fd:
                # 每到128位就写入
                for chunk in response.iter_content(128):
                    fd.write(chunk)
