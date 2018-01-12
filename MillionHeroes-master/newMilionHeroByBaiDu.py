import urllib, urllib.request as urllib2, sys,json,base64,time,pyperclip,baiduSearch,os
import ssl,re
from PIL import Image
from aip import AipOcr

""" 你的 APPID AK SK 等参数"""
class BaiDuApi():
	APP_ID = '10674400'
	API_KEY = 'VgVx1a9WdnMog65AhvlNhpta'
	SECRET_KEY = '8mAAeMiKV8wyMlh83V6jyc7RQGawoExE'
	options = {}
	options["language_type"] = "CHN_ENG"
	options["detect_direction"] = "true"
	options["detect_language"] = "true"
	options["probability"] = "true"

""" 读取图片 """
def get_file_content(filePath):
	with open(filePath, 'rb') as fp:
		return fp.read()
"""获取百度答案"""
def getAnswer(question):
	keyword = ''.join(question.split())  # 识别的问题文本
	print(keyword)
	convey = 'n'
	if convey == 'y' or convey == 'Y':
		results = baiduSearch.search(keyword, convey=True)
	elif convey == 'n' or convey == 'N' or not convey:
		results = baiduSearch.search(keyword)
	else:
		print('输入错误')
		exit(0)
	count = 0
	print('#######################################################')
	for result in results:
		# print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
		print('{0}'.format(result.abstract))  # 此处应有格式化输出
		print('#########################################################################')
		count = count + 1
		if (count == 3):
			break


"""主函数"""
def main():
	print('程序启动，版本 V1.0.1')
	os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
	os.system("adb pull /sdcard/screenshot.png ./screenshot.png")
	im = Image.open(r"screenshot.png")
	im.save("screen/screenshot%s.png" % time.time())  # 图片备份
	# img_size = im.size #屏幕分辨路
	w = im.size[0]
	# h = im.size[1]
	# print("xx:{}".format(img_size))
	region = im.crop((70, 200, w - 70, 600))  # 裁剪的区域
	# region = im.crop((70, 200, w - 70, 700))  # 裁剪的区域
	region.save("crop_test1.png")
	answer1 =im.crop((70, 600, w - 70, 800))
	answer1.save("answer1.png")
	answer2 =im.crop((70, 800, w - 70, 1000))
	answer2.save("answer2.png")
	answer3 =im.crop((70, 1000, w - 70, 1200))
	answer3.save("answer3.png")
	client = AipOcr(BaiDuApi.APP_ID, BaiDuApi.API_KEY, BaiDuApi.SECRET_KEY)
	image = get_file_content('crop_test1.png')
	""" 调用通用文字识别, 图片参数为本地图片 """
	client.basicGeneral(image)
	""" 带参数调用通用文字识别, 图片参数为本地图片 """
	reqDataDict = client.basicGeneral(image, BaiDuApi.options)
	try:
		words_result = reqDataDict['words_result']
	except:
		pass
	else:
		question = words_result[0]['words'].split('.')
		getAnswer(question[1])
if __name__ == '__main__':
	print('程序开始，版本号：V1.0.1')
	com = input('是否开始答题？\n')
	while True:
		if com == 'exit':
			print('程序退出')
			break
		elif com == 5 or com == '55':
			os.system('adb devices')
			print('程序用时：' + str(end - start) + '秒')
			com = input('是否继续答题？\n')
		else:
			start = time.time()
			main()
			end = time.time()
			print('程序用时：' + str(end - start) + '秒')
			com = input('是否继续答题？\n')
