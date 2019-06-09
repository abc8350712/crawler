import requests
import re
import time
import numpy as np
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
}
requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数

host_url = 'http://www.mingxing.com/ziliao/index?&p='
def get_headers():
    headers = [
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    ]

    return {'User-Agent':np.random.choice(headers)}


def sleep():
    time.sleep(2 * np.random.random())

def get_url(url):
    sleep()
    try:

        content = requests.get(url, headers=get_headers(), timeout=10, keep_alive=False)
        content.close()
        return BeautifulSoup(content.text, 'lxml')

    except:
        print('Connected Again .............')
        get_url((url))
pages = [i + 1 for i in range(1, 191)]
#soup = get_url('ss')
#print(soup.find_all('img', attrs={'src':re.compile('upload')}))

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
        with open('./img/' + name + '.jpg', 'wb') as fd:
            # 每到128位就写入
            for chunk in response.iter_content(128):
                fd.write(chunk)
