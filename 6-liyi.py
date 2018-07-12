import urllib.request
import urllib.parse
import os
import time

def handle_request(url, baname, page):
    pn = (page - 1) * 50
    # 拼接url
    data = {
        'ie': 'utf8',
        'kw': baname,
        'pn': pn,
    }
    #将字典转化为query_string格式
    query_string = urllib.parse.urlencode(data)
    #拼接url
    url += query_string
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    #构建请求对象
    request = urllib.request.Request(url=url, headers=headers)

    return request

# 根据请求对象,下载指定的响应内容到本地
def download(request, baname, page):
    # 根据吧名,创建文件夹的过程
    # 判断文件夹是否存在,不存在才创建
    if not os.path.exists(baname):
        os.mkdir(baname)
    # 文件的名字
    filename = '第%s页.html' % page
    print('正在下载%s....' % filename)
    # 拼接文件的全路径
    filepath = os.path.join(baname, filename)
    #发送请求
    response = urllib.request.urlopen(request)
    # 将内容读进来
    content = response.read()
    # 将内容写入到文件中
    with open(filepath, 'wb') as fp:
        fp.write(content)
    print('结束下载%s' % filename)


def main():
    url = 'https://tieba.baidu.com/f?'
    # 要爬取的贴吧的名字
    baname = input('请输入要爬取的吧名:')
    # 起始页码,结束页码
    start_page = int(input('请输入起始页码:'))
    end_page = int(input('请输入结束页码:'))
    # 搞个循环
    for page in range(start_page, end_page + 1):
        # 根据不同的page生成不同的url,然后生成不同的请求
        request = handle_request(url, baname, page)
        # 发送请求,获取响应
        download(request, baname, page)
        #停顿一下
        time.sleep(2)


if __name__ == '__main__':
    main()
