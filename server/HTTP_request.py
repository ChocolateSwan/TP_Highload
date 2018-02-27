class Request:
	""" HTTP Request """
	def __init__(self):
		self.error = None
		self.data = None
		self.method = None
		self.protocol = None
		self.url = None
		self.headers = None
		self.query = None
	def set_method (self, method):
		if method in ['GET', 'HEAD']:
			self.method = method
		else:
			self.error = True
	def set_url(self, url):
		pass
		#проверить на пустоту '/'