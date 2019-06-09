import requests
import re
import time
import numpy as np
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
}

host_url = 'https://www.dmm.co.jp/digital/videoa/-/actress/=/keyword=a/'
def get_proxy():
    proxies = [
        'http://150.95.151.68:8185',
        'http://150.95.151.68:8191',
        'http://150.95.151.68:8282',
        'http://150.95.151.68:8299',
        'http://45.76.98.49:8118',
        'http://150.95.151.68:8186',
        'http://150.95.151.68:8288',
        'http://150.95.151.68:8192',
        'http://180.235.39.9:80',
        'http://150.95.151.68:8286',

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

    return {'User-Agent':np.random.choice(headers)}

def get_url(url):
    #time.sleep(0.5)
    try:
        content = requests.get(url, headers=get_headers(), timeout=10, proxies=get_proxy())
        content.close()
        return BeautifulSoup(content.text, 'lxml')

    except:
        print('Connected Again .............')
        return get_url((url))
pages = [i + 1 for i in range(1, 191)]
#soup = get_url('ss')
#print(soup.find_all('img', attrs={'src':re.compile('upload')}))

soup = get_url(host_url)
all_url = soup.find_all('a', attrs={'href':re.compile('https://www.dmm.co.jp/digital/videoa/-/actress/')})
for i in range(10, 43):
    base_url = str(all_url[i].get('href'))
    soup = get_url(base_url)
    match_item = soup.find_all('p')
    tag = str(match_item[15])
    num_av = int(re.findall(re.compile('全(.*?)ページ'), tag)[0])

    for num in range(num_av):
        print(base_url + 'page=' + str(num + 1) + '/')
        soup = get_url(base_url + 'page=' + str(num + 1) + '/')
        urls = soup.find_all('a', attrs={'href': re.compile('https://www.dmm.co.jp/digital/videoa/-/list/=/article=actress')})
        imgs = soup.find_all('img', attrs={'src': re.compile('medium')})
        for i, img in enumerate(imgs):
            url = urls[i].get('href')
            soup = get_url(url)
            name = img.get('alt')
            items = soup.find_all('a', attrs={'href':re.compile('https://www.dmm.co.jp/digital/videoa/-/detai')})
            with open('./av_img_message/' + name + '.txt', 'a', encoding='utf-8') as f:
                def write_message(item):
                    item_url = item.get('href')
                    item_soup = get_url(item_url)
                    # print(item_soup)
                    message = item_soup.find_all('tr')
                    date = message[5].text.replace('\n', '')
                    actress = message[7].text.replace('\n', '')
                    director = message[8].text.replace('\n', '')
                    av_name = message[9].text.replace('\n', '')
                    maker = message[10].text.replace('\n', '')
                    level = message[11].text.replace('\n', '')
                    style = message[12].text.replace('\n', '')
                    code = message[13].text.replace('\n', '')
                    f.write(date + '\n')
                    f.write(actress + '\n')
                    f.write(director + '\n')
                    f.write(av_name + '\n')
                    f.write(maker + '\n')
                    f.write(level + '\n')
                    f.write(style + '\n')
                    f.write(code + '\n')


                pool = ThreadPool(8)
                results = pool.map(write_message, items)
                '''
                for i, item in enumerate(items):
                    item_url = item.get('href')
                    item_soup = get_url(item_url)
                    #print(item_soup)
                    message = item_soup.find_all('tr')
                    date = message[5].text.replace('\n', '')
                    actress = message[7].text.replace('\n', '')
                    director = message[8].text.replace('\n', '')
                    av_name = message[9].text.replace('\n', '')
                    maker = message[10].text.replace('\n', '')
                    level = message[11].text.replace('\n', '')
                    style = message[12].text.replace('\n', '')
                    code = message[13].text.replace('\n', '')
                    f.write(date + '\n')
                    f.write(actress + '\n')
                    f.write(director + '\n')
                    f.write(av_name + '\n')
                    f.write(maker + '\n')
                    f.write(level + '\n')
                    f.write(style + '\n')
                    f.write(code + '\n')
            '''
            #print(soup)
            img_url = img.get('src')
            print(img_url)
            # time.sleep(2)
            response = requests.get(img_url, headers=get_headers(), )
            response.close()
            with open('./av_img/' + name + '.jpg', 'wb') as fd:
                # 每到128位就写入
                for chunk in response.iter_content(128):
                    fd.write(chunk)
        '''
        for page in pages:
            print(page)
            url = host_url + str(page)
            soup = get_url(url)
            celebritys = soup.find_all('img', attrs={'src':re.compile('upload')})
            for celberity in celebritys:
                #print(celberity)
                name = celberity.get('alt')
                print(name)
                img_url = celberity.get('src')
        
                print(img_url)
                #time.sleep(2)
                response = requests.get(img_url, headers=get_headers(), )
                response.close()
                with open('./av_img/' + name + '.jpg', 'wb') as fd:
                    # 每到128位就写入
                    for chunk in response.iter_content(128):
                        fd.write(chunk)
        '''