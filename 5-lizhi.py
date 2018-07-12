import urllib.request
import urllib.parse
import re
import time

def main():
	url = 'http://www.yikexun.cn/lizhi/qianming/list_50_{}.html'
	start_page = int(input('请输入起始页码:'))
	end_page = int(input('请输入结束页码:'))
	#在这里打开文件
	fp = open('lizhi.html','w',encoding='utf8')
	for page in range(start_page,end_page+1):
		print('正在爬取第%s页......' % page)
		#拼接url,生成请求对象
		request = handle_request(url,page)
		#获取响应,urlopen一个response对象,read一个字节类型,decode读为字符串类型
		content = urllib.request.urlopen(request).read().decode('utf8')
		#解析内容函数
		parse_content(content,fp)
		print('结束爬取第%s页' % page)
		time.sleep(2)
	fp.close()

def handle_request(url,page=None):
	if page:
		url = url.format(page)
		# print(url)
	headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
	}
	#返回请求
	return urllib.request.Request(url=url,headers=headers)

def parse_content(content,fp):
	#写正则表达式,提取所有的标题和链接
	pattern = re.compile(r'<h3><a href="(/lizhi/qianming/\d+\.html)">(.*?)</a></h3>')
	ret = pattern.findall(content)

	# print(ret)
	# print(len(ret))
	# i = 0
	for herf_title in ret:
		#取出链接
		href = 'http://www.yikexun.cn' + herf_title[0]
		#取出标题
		title = herf_title[1]
		print('正在爬取%s......' % title)
		# 因为只有第一个title两边有b标签，所以这里写了一个小小的判断，只在循环第一次执行
		# if i == 0:
			#将title两边的b表情去掉
		title = title.strip('<>b/')
			# i += 1
		#print(title)

		#获取内容的函数
		text = get_text(href)
		#将标题和内容写入文件
		string = '<h1>%s</h1>%s' % (title,text)
		fp.write(string)
		print('结束爬取%s...' % title)
		time.sleep(2)

def get_text(href):
	# 构建请求对象，发送请求，解析响应，返回解析后的内容
	request = handle_request(href)
	content = urllib.request.urlopen(request).read().decode('utf8')
	pattern = re.compile(r'<div class="neirong">(.*?)</div>', re.S)

	ret = pattern.search(content)
	# print(ret.group(1))
	# exit()
	text = ret.group(1)
	#将图片链接去除掉
	pattern = re.compile(r'<img .*?>')
	text = pattern.sub('',text)
	return text

if __name__ == '__main__':
	main()