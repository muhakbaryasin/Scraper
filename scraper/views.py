from pyramid.view import view_config
from .Scraper import Scraper

import base64
import json

@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
	return {'project': 'scraper'}

@view_config(route_name='scraper', renderer='json')
def scraper(request):
	if 'url' not in request.params:
		return {'code': 'ok', 'message' : 'Parameter url nya bung'}
	
	url = request.params['url']
	
	if 'method' not in request.params:
		return {'code': 'ok', 'message' : 'Parameter method nya bung'}
	
	method = request.params['method']
	
	if 'json_headers' in request.params:
		json_headers = json.loads( base64.b64decode( request.params['json_headers'] ).decode() )
	else: json_headers = None
	
	if 'json_params' in request.params:
		json_params = json.loads( base64.b64decode( request.params['json_params'] ).decode() )
	else: json_params = None
	
	scraper = Scraper(url=url, method=method, headers=json_headers)
	
	# import pdb; pdb.set_trace()
	if json_params is not None:
		scraper.updateParams(json_params)
	
	res = scraper.execute()
	# import pdb; pdb.set_trace()
	try:
		resp = res.json()
	except:
		resp = res.text
	
	return {'code' : 'ok', 'message' : 'success', 'data' : resp}
	
	
		
		
	


