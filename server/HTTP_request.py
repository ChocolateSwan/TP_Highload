class HTTP_request:
	''' параметры HTTP запроса'''
	def __init__(self):
		self.method = None
		self.protocol = None
		self.url = None
		self.headers = None
		self.query = None