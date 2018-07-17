import requests
from lxml import etree
import re
import json
import time

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

#首页
def parse_first_page(url):
	r = requests.get(url=url,headers=headers)
	#生成一个tree对象
	tree = etree.HTML(r.text)
	#通过tree对象查找所有的数字,字母链接
	number_href_list = tree.xpath('//div[@class="bus_kt_r1"]/a/@href')
	char_href_list = tree.xpath('//div[@class="bus_kt_r2"]/a/@href')
	return number_href_list + char_href_list

#二级页面,公交信息
def parse_second_page(url,all_href,fp):
	#为了拼接完整的url,先将右边的/干掉
	url = url.rstrip('/')
	# print(url)
	for href in all_href:
		href = url + href
		r = requests.get(href,headers=headers)
		tree = etree.HTML(r.text)
		# print(tree)
		# exit()
		#解析,获取所有的公交href信息
		bus_href_list = tree.xpath('//div[@id="con_site_1"]/a/@href')
		bus_name_list = tree.xpath('//div[@id="con_site_1"]/a/text()')
		# print(bus_name_list)
		# exit()
		parse_third_page(url,bus_href_list,bus_name_list,fp)

#三级页面,车站信息
def parse_third_page(url,bus_href_list,bus_name_list,fp):
	for bus_href in bus_href_list:
		title = bus_name_list[bus_href_list.index(bus_href)]
		print('正在爬取%s......' %title)
		# print(title)
		# exit()
		#拼接完整的url
		bus_href = url + bus_href
		# print(bus_href)
		# exit()
		#向每一路公交的详情页发送请求
		r = requests.get(url=bus_href,headers=headers)
		#在下面的函数中,解析每一路公交的详细信息
		# print(r.text)
		# exit()
		parse_content(r.text,fp)
		print('结束爬取%s' %title)
		time.sleep(1)

#解析内容
def parse_content(content,fp):
	tree = etree.HTML(content)
	#获取线路名称
	name = tree.xpath('//div[@class="bus_i_t1"]/h1/text()')[0]
	#获取运行时间
	runtime = tree.xpath('//div[@class="bus_i_content"]/p[1]/text()')[0]
	#获取票价信息
	price = tree.xpath('//div[@class="bus_i_content"]/p[2]/text()')[0]
	#公交公司
	try:
		company = tree.xpath('//div[@class="bus_i_content"]/p[3]/a/text()')[0]
	except Exception as e:
		company = ''
	
	#更新时间
	gxsj = tree.xpath('//div[@class="bus_i_content"]/p[last()]/text()')[0]
	# # 获取公交路线长度
	# try:
	# 	length = tree.xpath('//div[@class="bus_label "]/p/text()')[0]
	# 	pattern = re.compile(r'\d+\.\d+')
	# 	ret = pattern.search(length)
	# 	length = ret.group()
	# except Exception as e:
	# 	length = ''

	#获取站数列表
	total_list = tree.xpath('//span[@class="bus_line_no"]/text()')
	pattern = re.compile(r'\d+')
	#获取上行总站数,使用正则将总站数拿走
	up_total = total_list[0]
	up_total = pattern.search(up_total).group()
	#获取下行总站数
	try:
		down_total = total_list[1]
		down_total = pattern.search(down_total).group()
	except Exception as e:
		down_total = ''
	
	#获取上行的公交站牌信息
	up_site_name = tree.xpath('//div[@class="bus_line_site "][1]//a/text()')
	#获取下行的公交站牌信息
	try:
		down_site_name = tree.xpath('//div[@class="bus_line_site "][2]//a/text()')
	except Exception as e:
		down_site_name = []
	
	# print(down_site_name)
	# exit()
	#将公交的详细信息保存到字典中
	item = {
		'线路名称':name,
		'运行时间':runtime,
		'票价信息':price,
		'公交公司':company,
		'更新时间':gxsj,
		# '线路长度': length,
		'上行站数':up_total,
		'上行站牌':up_site_name,
		'下行站数':down_total,
		'下行站牌':down_site_name,
	}
	string = json.dumps(item,ensure_ascii=False)
	fp.write(string + '\n')



def main():
	#打开文件
	fp = open('武汉公交线路.txt','w',encoding='utf8')
	url = 'http://wuhan.8684.cn/'
	#获取所有的数字,字母链接
	all_href = parse_first_page(url)
	#遍历列表,依次发送请求,解析二级页面
	parse_second_page(url,all_href,fp)
	fp.close()


if __name__ == '__main__':
	main()