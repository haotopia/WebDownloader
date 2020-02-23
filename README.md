# 网站下载程序设计与实现

## 1．实验原理

  根据URL向服务器发起HTTP请求得到网站的原始html，对html进行分析，得到其中的<a>标签，获取其中的href属性，得到下一个网站的URL，通过对<img>标签的解析，获取其中的srt属性得到图片的URL。重复步骤下载到目标的深度和网站数量。

## 2.实验流程图

![网络采样流程图](\img\网络采样流程图.png)

## 3.工具介绍

### （1）Requests

requests是使用Apache2 licensed 许可证的HTTP库。用python编写。比urllib2模块更简洁。Request支持HTTP连接保持和连接池，支持使用cookie保持会话，支持文件上传，支持自动响应内容的编码，支持国际化的URL和POST数据自动编码。在python内置模块的基础上进行了高度的封装，从而使得python进行网络请求时，变得人性化，使用Requests可以轻而易举的完成浏览器可有的任何操作。

在本实验中用于HTTP请求相关操作

  （[https://2.python-requests.org//zh_CN/latest/user/quickstart.html](https://2.python-requests.org/zh_CN/latest/user/quickstart.html)）

### （2）BeautifulSoup4

  Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.( https://pypi.org/project/beautifulsoup4/)

翻译：Beautiful Soup是一个可以轻松从网页上抓取信息的库。它位于HTML或XML解析器的顶部，提供用于迭代，搜索和修改解析树的Python惯用法。

在本实验中该库用于对取得的网页进行分析

### （3）Pandas

（https://pandas.pydata.org/）

翻译：pandas是BSD许可的开源库，为Python编程语言提供了高性能，易于使用的数据结构和数据分析工具。

​    在本次实验中用于爬取的网站数据进行链接数据管理，包括索引，维护，去重等

### （4）PyQt5

(https://pypi.org/project/PyQt5/5.8.2/)

在本次实验中用于GUI设计。

## 4.关键代码解释

（因为本次实验GUI部分并非主题，在实验中不再过多赘述，对函数的详解也将结合官方手册进行说明）

### （1）    构造函数

```python
def __init__(self, url, deep, file_path):
    self.url = url
    print(self.url)
    r = requests.get(self.url) ## 取得Response 对象
    r.encoding = r.apparent_encoding
    self.enc = r.encoding
    self.text = r.text  ##获取到了目标的html文本
    self.soup = BeautifulSoup(self.text, "html.parser") 
    ##elf.text是被解析的html格式的内容，html.parser表示解析用的解析器
    self.deep = deep
    self.file_path = file_path
    self.find_all_a()
```

### （2）    对数据进行解析

得到一个BeautifulSoup对象后，一般通过BeautifulSoup类的基本元素来提取html中的内容

![bs](img\bs.png)

我们常用通过find_all()方法来查找标签元素：

**find_all(name, attrs, recursive, string, \**kwargs)** 

返回一个列表类型，存储查找的结果 

• name：对标签名称的检索字符串

• attrs：对标签属性值的检索字符串，可标注属性检索

• recursive：是否对子孙全部检索，默认True

• string：<>…</>中字符串区域的检索字符串

### （3）    使用到的正则和字符串操作

##### ①   匹配URL

``` python
'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
```

##### ②   拆分二级域名

```python
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
```



