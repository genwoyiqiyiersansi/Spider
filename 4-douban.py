import json
import urllib.request
import urllib.parse

url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=20&limit=20'

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }

request = urllib.request.Request(url=url,headers=headers)

content = urllib.request.urlopen(request).read().decode('utf8')

# print(content)

#将json格式数据转化为python对象
obj = json.loads(content)
# print(type(obj))

#现在的obj是一个列表,列表里面都是字典
lt = []
#遍历列表,依次提取每一个字典里面的电影的名字和评分
for movie in obj:
	title = movie['title']
	score = movie['score']
	image_url = movie['cover_url']
	item = {
		'电影名字':title,
		'电影评分':score,
		'电影海报':image_url,
	}
	lt.append(item)

	string = json.dumps(lt,ensure_ascii=False)
	with open('movie.txt','w',encoding='utf8') as fp:
		fp.write(string)