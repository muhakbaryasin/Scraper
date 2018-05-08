from ..RequestController import RequestController

class ScraperController(RequestController):
	
	def __init__(self, request):
		RequestController.__init__(self, request)
		
		# Add your request controller tuple under this code
		self.REQ_SCRAPER = ( ('url', self.TEXT), ('method', self.TEXT) )
