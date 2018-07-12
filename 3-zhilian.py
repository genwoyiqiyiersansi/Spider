import urllib.request
import urllib.parse
import time
from bs4 import BeautifulSoup


class ZhiLianSpider(object):

    def __init__(self, jl, kw, start_page, end_page):
        # 保存到成员属性中,这样在其他的方法中就可以直接使用
        self.jl = jl
        self.kw = kw
        self.start_page = start_page
        self.end_page = end_page

        self.items = []

    def handle_request(self, page):
        url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?'
        # 拼接url
        data = {
            'jl': self.jl,
            'kw': self.kw,
            'p': page,
        }
        # 将data数据转化为query_string类型
        query_string = urllib.parse.urlencode(data)
        # 拼接url
        url += query_string
        # print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        }
        # 返回请求对象
        return urllib.request.Request(url=url, headers=headers)

        # 解析内容
    def parse_content(self, content):
        # 生成soup对象
        soup = BeautifulSoup(content, 'lxml')
        # 首先找到所有的table
        table_list = soup.find_all('table', class_='newlist')[1:]
        # print(table_list)
        # print(len(table_list))
        # exit()
        #遍历所有的table,依次提取每一个工作的信息
        for table in table_list:
            #职位名称
            zwmc = table.select('.zwmc a')[0].text.strip('\xa0')
            #公司名称
            gsmc = table.select('.gsmc a')[0].text
            #职位月薪
            zwyx = table.select('.zwyx')[0].text
            #工作地点
            gzdd = table.select('.gzdd')[0].text
            # print(gzdd)
            # exit()
            item = {
                '职位名称':zwmc,
                '公司名称':gsmc,
                '职位月薪':zwyx,
                '工作地点':gzdd,
            }
            self.items.append(item)

    def run(self):
        # 搞个循环
        for page in range(self.start_page, self.end_page + 1):
            print('正在爬取第%s页......' % page)
            # 拼接url的过程,构建请求对象
            request = self.handle_request(page)
            content = urllib.request.urlopen(request).read().decode('utf8')
            # 给我请求对象,解析并且提取内容
            self.parse_content(content)
            print('结束下载第%s页' % page)
            time.sleep(2)

        #将所有的工作保存到文件中
        string = str(self.items)
        with open('work.txt','w',encoding='utf8') as fp:
            fp.write(string)

def main():
    # 输入工作地点
    jl = input('请输入工作地点:')
    # 输入工作关键字
    kw = input('请输入关键字:')
    # 输入起始页码
    start_page = int(input('请输入起始页码:'))
    # 输入结束页码
    end_page = int(input('请输入结束页码:'))
    zhilian = ZhiLianSpider(jl, kw, start_page, end_page)
    zhilian.run()


if __name__ == '__main__':
    main()
