from pyramid.view import view_config

from .ScraperController import ScraperController
from .Scraper import Scraper

import base64
import json

import logging
log = logging.getLogger(__name__)

class MainView(object):
	def __init__(self, request):
		self.request = request
		self.reqon = ScraperController(request)
		
	@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
	def my_view(self):
		return {'project': 'scraper'}

	@view_config(route_name='scraper', renderer='json')
	def scraper(self):
		try:
			self.reqon.checkComplete(self.reqon.REQ_SCRAPER)
			
			if 'url' not in self.request.params:
				return {'code': 'ok', 'message' : 'Parameter url nya bung'}
			
			url = self.request.params['url']
			
			if 'method' not in self.request.params:
				return {'code': 'ok', 'message' : 'Parameter method nya bung'}
			
			method = self.request.params['method']
			
			if 'json_headers' in self.request.params:
				json_headers = json.loads( base64.b64decode( self.request.params['json_headers'] ).decode() )
			else: json_headers = None
			
			if 'json_params' in self.request.params:
				json_params = json.loads( base64.b64decode( self.request.params['json_params'] ).decode() )
			else: json_params = None
			
			scraper = Scraper(url=url, method=method, headers=json_headers)
			
			if json_params is not None:
				scraper.updateParams(json_params)
			
			res = scraper.execute()
			
			try:
				resp = res.json()
			except:
				resp = res.text.replace('\n', '')
			
			return {'code' : 'ok', 'message' : 'success', 'data' : resp}
	
	except Exception as e:
			log.exception('error scraper')
			return {'code' : 'ok', 'message' : 'error - {}'.format(str(e)) , 'data' : resp}
	
		
		
	


