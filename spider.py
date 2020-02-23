import requests
from pandas import Series, DataFrame
from bs4 import BeautifulSoup
import codecs
import os
import re


class CatchHtml:
    __slots__ = "url", "deep", "text", "soup", "enc", 'file_path'

    def __init__(self, url, deep, file_path):
        self.url = url
        print(self.url)
        r = requests.get(self.url)
        r.encoding = r.apparent_encoding
        self.enc = r.encoding
        self.text = r.text
        self.soup = BeautifulSoup(self.text, "html.parser")
        self.deep = deep
        self.file_path = file_path
        self.find_all_a()

    def find_all_a(self):

        tags = []
        links = []
        deep = []

        pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        for link in self.soup.find_all('a'):
            url = link.get('href')
            if re.match(pattern, url):
                print(url)
                links.append(url)
                tags.append("a")
                deep.append(self.deep)

        a_data = DataFrame({
            "tag": tags,
            "link": links,
            "deep": deep
        })
        return a_data

    def find_all_img(self):
        topHostPostfix = (
            '.com', '.la', '.io', '.co', '.info', '.net', '.org', '.me', '.mobi',
            '.us', '.biz', '.xxx', '.ca', '.co.jp', '.com.cn', '.net.cn',
            '.org.cn', '.mx', '.tv', '.ws', '.ag', '.com.ag', '.net.ag',
            '.org.ag', '.am', '.asia', '.at', '.be', '.com.br', '.net.br',
            '.bz', '.com.bz', '.net.bz', '.cc', '.com.co', '.net.co',
            '.nom.co', '.de', '.es', '.com.es', '.nom.es', '.org.es',
            '.eu', '.fm', '.fr', '.gs', '.in', '.co.in', '.firm.in', '.gen.in',
            '.ind.in', '.net.in', '.org.in', '.it', '.jobs', '.jp', '.ms',
            '.com.mx', '.nl', '.nu', '.co.nz', '.net.nz', '.org.nz',
            '.se', '.tc', '.tk', '.tw', '.com.tw', '.idv.tw', '.org.tw',
            '.hk', '.co.uk', '.me.uk', '.org.uk', '.vg', ".com.hk")
        regx = r'[^\.]+(' + '|'.join([h.replace('.', r'\.') for h in topHostPostfix]) + ')$'
        pattern_url = re.compile(regx, re.IGNORECASE)

        tags = []
        links = []
        deep = []
        for link in self.soup.find_all('img'):
            pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            url = link.get('src')
            if url:
                if re.match(pattern, url) is None:
                    if pattern_url.search(url) is None:
                        links.append(self.url + url)
                    else:
                        links.append("http:"+url)
                else:
                    links.append(url)
                tags.append("img")
                deep.append(self.deep)

        img_data = DataFrame({
            "tag": tags,
            "link": links,
            "deep": deep
        })
        return img_data

    def get_soup(self):
        return self.soup

    def get_text(self):
        return self.text

    def get_root_path(self):
        return self.file_path

    def down_web(self, flag=False):
        root_name = self.url.rsplit('.')[1]
        temp_name = self.url.rsplit('.')[0]
        web_name = temp_name.rsplit('//')[1]
        if flag:
            file_name = self.file_path+root_name
        else:
            file_name = self.file_path
        is_exists = os.path.exists(file_name)
        if not is_exists:
            os.mkdir(file_name)

        file_name = file_name+'\\'+web_name
        is_exists = os.path.exists(file_name)
        if not is_exists:
            os.mkdir(file_name)
        fo = codecs.open(file_name + "\\" + "\index.html", "w", self.enc)
        fo.write(self.text)
        self.file_path = file_name + "\\"

    def down_img(self):
        img_list = self.find_all_img()
        imgs = img_list.loc[:, 'link']
        for img in imgs:
            response = requests.get(img)
            content = response.content
            file_name = img.rsplit('/', maxsplit=1)[1]
            if '?' in file_name:
                file_name = file_name.rsplit('?', maxsplit=1)[0]
            print(self.file_path+file_name)
            with open(self.file_path + file_name, mode='wb') as fp:
                fp.write(content)


class WebSpider:
    __slots__ = "url", "max_page", "max_deep", "need_mul", "root_page", "root_link_list", "root_path"

    def __init__(self, url, max_page, max_deep, need_mul, root_path):
        self.root_page = url
        self.max_page = max_page
        self.max_deep = max_deep
        self.root_path = root_path
        self.need_mul = need_mul
        cw = CatchHtml(self.root_page, 1, self.root_path)
        self.root_link_list = cw.find_all_a()

    def catch_web(self, url, fil_path, deep):
        page = CatchHtml(url, deep, fil_path)
        if deep == 1:
            page.down_web(True)
        else:
            page.down_web()
        if self.need_mul:
            page.down_img()
        page_list = page.find_all_a()
        pages = page_list.loc[:, 'link']
        deep += 1
        fil_path = page.get_root_path()
        page_cont = 1
        for pag in pages:
            page_cont += 1
            if deep > int(self.max_deep):
                break
            if page_cont > int(self.max_page):
                break
            self.catch_web(pag, fil_path, deep)

    def start(self):
        self.catch_web(self.root_page, self.root_path, 1)


#x = WebSpider("http://www.baidu.com", 4, 2, True, 'C:\\Users\\lflx1\\Desktop\\Spider\\')
#x.start()
