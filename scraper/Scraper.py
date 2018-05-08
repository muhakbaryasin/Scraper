import requests

class Scraper(object):
	def __init__(self, url, method='GET', id=None, headers=None):
		self.setUrl(url)
		self.setMethod(method)
		self.setParams( {} )
		
		if id is not None:
			self.setId(id)
		
		self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
		
		if headers is not None:
			self.updateHeaders(headers)		
		
		pass
	
	def setMethod(self, method):
		if type(method) is not str and (method != 'GET' or method != 'POST'):
			raise Exception("Method must be a string GET/POST")

		self.method = method

	def setUrl(self, url):
		if type(url) is not str:
			raise Exception("Url must be a string.")

		self.url = url

	def setId(self, id):
		if type(url) is not str:
			raise Exception("Id must be a string.")

		self.id = id

	def updateHeaders(self, headers):
		if type(headers) is not dict:
			raise Exception("Headers must be a dict.")
		
		self.headers.update(headers)
	
	def setParams(self, params):
		if type(params) is not dict:
			raise Exception("Params must be a dict.")
	
		self.params = params
	
	def updateParams(self, params):
		if type(params) is not dict:
			raise Exception("Params must be a dict.")
	
		self.params.update(params)
	
	def getParams(self):
		return self.params
	
	def getHeaders(self):
		return self.headers
	
	def getMethod(self):
		return self.method
	
	def execute(self):
		if self.getMethod() == "GET":
			req = requests.get(self.url, data=self.getParams(), headers=self.headers)
		elif self.getMethod() == "POST":
			req = requests.post(self.url, data=self.getParams(), headers=self.headers)

		print(req.headers)
		print(req.request.body)
		return req
