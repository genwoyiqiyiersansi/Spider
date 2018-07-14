import json
import jsonpath
import urllib.request
import urllib.parse
import time

#用来存放所有的评论信息
items = []

def handle_request(page, url):
	url = url.format(page)
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
	return urllib.request.Request(url=url, headers=headers)


def parse_content(content):
	# 如何解析content
	# 处理content，将其转化为合法的json格式字符串
	content = content.strip('() \n\t\r')
	# print(content)
	#将json格式转化为python对象
	obj = json.loads(content)
	# print(type(obj))
	#提取所有的评论
	comment_list = obj['comments']
	# print(comment_list)
	for comment in comment_list:
		#用户头像
		# avatar = comment['user']['avatar']
		avatar = jsonpath.jsonpath(comment,'$..avatar')[0]
		avatar = 'http:' + avatar
		#用户昵称
		nick = comment['user']['nick']
		# nick = jsonpath.jsonpath(comment,'$..nick')[0]
		#评论内容
		neirong = comment['content']
		#图片
		photo_list = comment['photos']
		photos = []
		for photo in photo_list:
			#获取小图
			little_image = photo['thumbnail']
			little_image = 'http:' + little_image
			#获取大图
			big_image = photo['url']
			big_image = 'http:' + big_image
			photos.append((little_image,big_image))
		#时间
		ping_time = comment['date']
		#手机信息
		# info = comment['auction']['sku']
		info = jsonpath.jsonpath(comment,'$..sku')[0]
		# print(info)
		# exit()
		item = {
			'用户头像':avatar,
			'用户昵称':nick,
			'评论内容':neirong,
			'晒图':photos,
			'评论时间':ping_time,
			'手机信息':info,
		}
		items.append(item)


def main():
	url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=559141739630&userNumId=100340983&currentPageNum={}&pageSize=20'
	start_page = int(input('请输入起始页码:'))
	end_page = int(input('请输入结束页码:'))
	# for page in range(1,2):
	for page in range(start_page,end_page+1):
		print('正在爬取第%s页......' % page)
		request = handle_request(page,url)
		content = urllib.request.urlopen(request).read().decode('utf8')
		parse_content(content)
		print('结束爬取第%s页' % page)
		time.sleep(2)

	#爬取完毕,写入文件
	string = json.dumps(items,ensure_ascii=False)
	with open('taobao.json','w',encoding='utf8') as fp:
		fp.write(string)


if __name__ == '__main__':
	main()
