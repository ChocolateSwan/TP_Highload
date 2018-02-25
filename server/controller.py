from mime_types import *
import re

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


class Response(object):
	"""HTTP Response """
	def __init__(self, arg):

		




def parse_request(data, document_root = ""):
	# self.data = data.decode('UTF-8')
	print(data)
	request = Request()
	request.method = re.search(r'^\w+', data).group()
	request.protocol = re.findall(r'HTTP/([1-9.]+)', data)[0]
	request.url = re.findall(r'(https?://[^\s?]+)', data)[0]
	# request.query = re.findall(r'[?&]([\w=]+)', rr)
	request.query = {item.split("=")[0]: item.split("=")[1] for item in 
		re.findall(r'[?&]([\w=]+)', rr)}
	# request.headers
	print (request.method, request.protocol, request.url, sep = "|")

	if request.error:
		self.response = Response(ResponseCode.NOT_ALLOWED, request.protocol)





