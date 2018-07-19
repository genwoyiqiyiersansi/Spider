import requests
from shibie import shibie
import  time

#搞一个会话
s = requests.Session()

i = 0

while 1:

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
	}

	# 先将验证码下载到本地
	get_url = 'https://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx'
	r = s.get(get_url,headers=headers)

	#需要向图片src发送请求，将验证码下载到本地
	image_src = 'https://so.gushiwen.org/RandCode.ashx'
	r = s.get(image_src,headers=headers)
	with open('code.png','wb') as fp:
		fp.write(r.content)

	# code = input('请输入验证码:')
	#让tesseract自动识别
	code = shibie('code.png')

	post_url = 'https://so.gushiwen.org/user/login.aspx?from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx '

	data = {
		'__VIEWSTATE':'3/7LLbfHhB6YKGQ6z0DI5yy707AsUcHKhL8Dm3cn5sVVAMhmE6aBfanjFbE06gXwWYig/D4JuXVa1QoPPCdbzUD877i+CPJhG+beZNAkx+Ts+32EGXy2lOKTMD8=',
		'__VIEWSTATEGENERATOR':'C93BE1AE',
		'code': code,
		'denglu':'登录',
		'email':'xxx',
		'from':'',
		'pwd':'xxx',
	}

	r = s.post(post_url, headers=headers, data=data)
	
 	# print(r.text)
	if '退出登录' in r.text:
		print('登录成功')
		break

	i += 1
	print('这是第%s次登录失败' % i)
	time.sleep(2)
