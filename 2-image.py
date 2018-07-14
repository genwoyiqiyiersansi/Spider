from lxml import etree
import time
import urllib.request
import urllib.parse
import os


def handle_request(url, url_er, page):
    if page == 1:
        url = url
    else:
        url = url_er.format(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    return urllib.request.Request(url=url, headers=headers)


def parse_content(content):
    # 生成tree对象
    tree = etree.HTML(content)
    # 写xpath,来获取所有图片的img_src
    image_src_list = tree.xpath('//div[@id="container"]//img/@src2')
    image_alt_list = tree.xpath('//div[@id="container"]//img/@alt')
    # print(image_src_list)
    # print(len(image_src_list))
    for image_src in image_src_list:
        dirname = 'meinv'
        if not os.path.exists(dirname):
        	os.mkdir(dirname)
        filename = image_alt_list[image_src_list.index(image_src)]
        suffix = image_src.split('.')[-1]
        filename = filename + '.' + suffix
        filepath = os.path.join(dirname, filename)
        # print(filename)
        # print(filepath)
        print('正在下载%s......' % filename)
        urllib.request.urlretrieve(image_src, filepath)
        print('结束下载%s' % filename)
        time.sleep(2)


def main():
    start_page = int(input('请输入起始页码:'))
    end_page = int(input('请输入结束页码:'))
    url = 'http://sc.chinaz.com/tag_tupian/YaZhouMeiNv.html'
    url_er = 'http://sc.chinaz.com/tag_tupian/yazhoumeinv_{}.html'
    for page in range(start_page, end_page + 1):
        print('正在下载第%s页......' % page)
        request = handle_request(url, url_er, page)
        content = urllib.request.urlopen(request).read().decode('utf8')
        # 解析内容函数
        parse_content(content)
        print('结束下载第%s页' % page)
        time.sleep(2)

if __name__ == '__main__':
    main()
