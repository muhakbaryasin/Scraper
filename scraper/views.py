from pyramid.view import view_config

from .ScraperController import ScraperController
from .Scraper import WebDriver, Rest

import base64
import json
from time import sleep

from .Filelogger import FileLogger

import logging
log = logging.getLogger(__name__)

class MainView(object):
	def __init__(self, request):
		self.request = request
		self.reqon = ScraperController(request)
		
	@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
	def my_view(self):
		return {'project': 'scraper'}

	@view_config(route_name='webdriver', renderer='json')
	def webdriver(self):
		try:
			#self.reqon.checkComplete(self.reqon.REQ_SCRAPER)
			if 'url' not in self.request.params:
				return {'code': 'ok', 'message' : 'Parameter url nya bung'}
			
			id = None
			
			if 'id' in self.request.params and self.request.params['id'] != '':
				id = self.request.params['id']
			
			url = self.request.params['url']
			wd = WebDriver(url=url, id=id)
			
			if wd.id is not None:
				id = wd.id
			
			if 'json_actions' in self.request.params:
				json_actions = json.loads( base64.b64decode( self.request.params['json_actions'] ).decode() )
			else: json_params = None
			
			wd.session.save_screenshot("trigana.png")
			
			for each_action in json_actions:
				print(each_action)
				element = each_action['element']
				selected_element = None
				
				if element == '':
					print('no element')
				elif element[0] == '#':
					selected_element = wd.session.find_elements_by_id(element[1:])
				elif element[0] == '.':
					selected_element = wd.session.find_elements_by_class(element[1:])
				elif element[0] == '<':
					selected_element = wd.session.find_elements_by_tag_name(element[1:-1])
				
				
				if selected_element is list and len(selected_element) < 1:
					raise Exception('Element {} is not found.'.format(element))
				
				if 'action' not in each_action:
					raise Exception('Please specify action')
				
				action = each_action['action']
				
				if action == '':
					print('dont act')
				elif action == 'click':
					wd.clickElement(selected_element)
				elif action == 'send_keys':
					wd.sendKeys(selected_element, each_action['value'] )
				elif action == "select_option_by_value":
					wd.selectOptionByValue(selected_element, each_action['value'] )
				elif action == 'execute_script':
					wd.executeScript( each_action['value'] )
				else:
					message = 'action {} is not registered'.format(action)
					raise Exception(message)
				
				wd.session.save_screenshot(each_action['element']+each_action['action']+each_action['value']+".png")			
			
			pgs = None
			
			if 'sign_text' in self.request.params and self.request.params['sign_text'] != '':
				sign_text = self.request.params['sign_text']
				attempt = 0
				
				while wd.session.page_source.find(sign_text) < 0 and attempt < 11:
					pgs = wd.session.page_source
					attempt += 1
					sleep(1)
			
			fl = FileLogger(file_log_name = 'last.html', reference = 'none', data = pgs, mode = 'w')
			wd.session.save_screenshot("last.png")
			wd.session.quit()
			
			return {'code' : 'OK', 'message' : 'ok', 'id' : wd.id, 'b64encoded_page_source' : base64.b64encode( pgs.encode() ).decode()}
		except Exception as e:
			try:
				wd.session.quit()
			except:
				pass
			log.exception('webdriver')
			return {'code' : 'ERROR', 'message' : 'error - {}'.format(str(e)) , 'data' : None}
		
	@view_config(route_name='rest', renderer='json')
	def rest(self):
		try:
			#self.reqon.checkComplete(self.reqon.REQ_SCRAPER)
			
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
			
			rest = Rest(url, method=method, headers=json_headers)
			
			if json_params is not None:
				rest.updateParams(json_params)
			
			res = rest.execute()
			
			try:
				resp = res.json()
			except:
				resp = res.text.replace('\n', '')
			
			return {'code' : 'OK', 'message' : 'success', 'data' : resp, 'id' : rest.id}
	
		except Exception as e:
			log.exception('error scraper')
			return {'code' : 'ERROR', 'message' : 'error - {}'.format(str(e)) , 'data' : None}