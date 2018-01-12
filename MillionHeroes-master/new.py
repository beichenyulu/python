import urllib, urllib.request as urllib2, sys,json,base64,time,pyperclip,baiduSearch,os
import ssl,re,threading,pytesseract
from PIL import Image
from aip import AipOcr
'''检查设备'''
def CheckPhone():
	print('程序启动，当前版本号： V2.0.1')
	os.system("adb devices")
	print('确保手机连接电脑，并打开了USB调试模式')

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
class QandA():
	question = ''
	answer1 =''
	answer2 =''
	answer3 =''
	aList = []
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
	print('#########################################################################')
	for result in results:
		# print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
		if( result.abstract == '百度软广，当前代码版本不予摘要'):
			pass
		else:
			print(getReData(QandA.aList,result.abstract))
			print('{0}'.format(result.abstract))  # 此处应有格式化输出
			print('#########################################################################')
			count = count + 1
			if (count == 3):
				break
'''获取三个答案的结果'''
def getAnswerImgData():
	answerList = []
	for i in range(1,4):
		img = "answer%s.png"%i
		client = AipOcr(BaiDuApi.APP_ID, BaiDuApi.API_KEY, BaiDuApi.SECRET_KEY)
		image = get_file_content(img)
		""" 调用通用文字识别, 图片参数为本地图片 """
		client.basicGeneral(image)
		""" 带参数调用通用文字识别, 图片参数为本地图片 """
		reqDataDict = client.basicGeneral(image, BaiDuApi.options)
		# reaDataJson = json.loads(reqData)
		try:
			words_result = reqDataDict['words_result']
		# log_id = reqDataDict['log_id']
		# direction = reqDataDict['direction']
		# words_result_num = reqDataDict['words_result_num']
		# language = reqDataDict['language']
		except:
			pass
		else:
			answer = words_result[0]['words']
			answerList.append(answer)
	QandA.aList = answerList
	print(answerList)

def getQuestion():
	client = AipOcr(BaiDuApi.APP_ID, BaiDuApi.API_KEY, BaiDuApi.SECRET_KEY)
	image = get_file_content('crop_test1.png')
	""" 调用通用文字识别, 图片参数为本地图片 """
	client.basicGeneral(image)
	""" 带参数调用通用文字识别, 图片参数为本地图片 """
	reqDataDict = client.basicGeneral(image, BaiDuApi.options)
	# reaDataJson = json.loads(reqData)
	try:
		words_result = reqDataDict['words_result']
		question = words_result[0]['words'].split('.')
		QandA.question =(question[1])
		print('第%s的问题是：%s'%(question[0],question[1]))
	# log_id = reqDataDict['log_id']
	# direction = reqDataDict['direction']
	# words_result_num = reqDataDict['words_result_num']
	# language = reqDataDict['language']
	except:
		pass

def getReData(A,ABD):
	for a in A:
		# print(a)
		# 将正则表达式编译成Pattern对象
		pattern = re.compile(r'%s'%a)
		# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
		match = pattern.search(ABD)
		if match:
			# 使用Match获得分组信息
			print(a)
def Screen():
	os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
	os.system("adb pull /sdcard/screenshot.png ./screenshot.png")
	im = Image.open(r"screenshot.png")
	# im.save("screen/screenshot%s.png"%time.time())#图片备份
	img_size = im.size  # 屏幕分辨率
	w = im.size[0]
	# h = im.size[1]
	print("xx:{}".format(img_size))
	region = im.crop((70, 200, w - 70, 600))  # 裁剪的区域
	# region = im.crop((70, 200, w - 70, 700))  # 裁剪的区域
	region.save("crop_test1.png")
	answer1 = im.crop((70, 600, w - 70, 800))
	answer1.save("answer1.png")
	answer2 = im.crop((70, 800, w - 70, 1000))
	answer2.save("answer2.png")
	answer3 = im.crop((70, 1000, w - 70, 1200))
	answer3.save("answer3.png")
	print('截图完成')
"""主函数"""
def main():
	CheckPhone()
	com = input('是否开始答题？\n')
	while True:
		if com == 'exit':
			print('程序退出')
			break
		else:
			start = time.time()
			Screen()#截图
			# getQuestion()#获取问题
			# getAnswerImgData()#获取答案

			#双线程识别
			t1 = threading.Thread(target=getQuestion)
			t2 = threading.Thread(target=getAnswerImgData)
			for thread in (t1,t2):
				thread.start()
				thread.join()
			getAnswer(QandA.question)

			# getAnswerImgData()
			end = time.time()
			print('程序用时：' + str(end - start) + '秒')
			com = input('是否继续答题？\n')
	# ScreenAndGet()
def PilWord():
	imgData = Image.open('screenshot.png')
	print(imgData)
	str = pytesseract.image_to_string(imgData)
	# text = pytesseract.image_to_string(imgData, lang='chi_sim')
	print(str)
if __name__ == '__main__':
	# main()
	PilWord()
