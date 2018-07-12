import urllib.request
import urllib.parse
import re
import os
import time

def handle_request(url,page):
	url += str(page) + '/'
	# print(url)
	headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
	}
	#创建请求对象
	request = urllib.request.Request(url=url,headers=headers)
	return request

def parse_content(request):
	#发送请求
	response = urllib.request.urlopen(request)
	#读取内容
	content = response.read().decode('utf8')
	with open('jiexi.html','w',encoding='utf8') as fp:
		fp.write(content)
	#解析内容,提取这一页所有的图片链接
	pattern = re.compile(r'<div class="thumb">.*?<a href=".*?" target="_blank">.*?<img src="(.*?)" alt="(.*?)" />.*?</div>', re.S)

	#查找内容,返回的是一个元组[(),()]('//pic.qiushibaike.com/system/pictures/12067/120676438/medium/app120676438.jpeg', '这个栈道')
	ret = pattern.findall(content)
	# print(ret)
	# exit()
	# print(len(ret))
	download(ret)

def download(ret):
	for image_info in ret:
		#取出图片的链接
		image_src = image_info[0]
		#取出图片的标题
		image_alt = image_info[1]
		# 拼接完整的url
		image_src = 'https:' + image_src
		#创建文件夹
		dirname = 'qiutu'
		if not os.path.exists(dirname):
			os.mkdir(dirname)
		#得到后缀名
		suffix = image_src.split('.')[-1]
		#文件名字
		filename = image_alt + '.' + suffix
		#拼接路径
		filepath = os.path.join(dirname,filename)
		print('正在下载%s......' %filename)
		#下载图片
		urllib.request.urlretrieve(image_src,filepath)
		print('结束下载%s' %filename)
		time.sleep(3)



def main():
	start_page = int(input('请输入要爬取得起始页码:'))
	end_page = int(input('请输入要爬取得结束页码:'))
	url = 'https://www.qiushibaike.com/pic/page/'
	for page in range(start_page,end_page+1):
		print('正在下载第%s页......' %page)
		#拼接url,构建请求对象
		request = handle_request(url,page)
		#发送请求,获取响应,并且解析内容
		parse_content(request)
		print('结束下载第%s页' %page)
		time.sleep(3)



if __name__ == '__main__':
	main()
