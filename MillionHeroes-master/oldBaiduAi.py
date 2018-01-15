def getBaiduAcc_token():
	grant_type = 'client_credentials'
	client_id ='*******'
	client_secret = '*******'
	host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=%s&client_id=%s&client_secret=%s'%(grant_type,client_id,client_secret)
	request = urllib2.Request(host)
	request.add_header('Content-Type', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	content = response.read()
	if (content):
		jsonData = json.loads(content)
		access_token = jsonData['access_token']
		expires_in = jsonData['expires_in']
		scope = jsonData['scope']
		session_key = jsonData['session_key']
		refresh_token = jsonData['refresh_token']
		session_secret = jsonData['session_secret']
		return access_token

##获取百度识别返回值##
def getImageWords(image):
	access_token = getBaiduAcc_token()
	language_type = 'CHN_ENG'
	probability = True
	url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=%s&image=%s'%(access_token,image)
	request = urllib2.Request(url)
	request.add_header('Content-Type', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	content = response.read()
	if (content):
		print(content)
