from mime_types import MIME_TYPES
from response_codes import RESPONSE_CODES
import datetime
import fcntl
import re
import os

document_root = "./"

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


class Response:
	"""HTTP Response """
	def __init__(self, code, protocol, content_type, content_length):
		self.code = code
		self.protocol = protocol
		self.data = "data"
		self.content_type = content_type
		self.content_length = content_length
		self.date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

	def __success(self):
		return 'HTTP/{} {}\r\n' \
			'Content-Type: {}\r\n' \
			'Content-Length: {}\r\n'\
			'Date: {}\r\n' \
			'Server: Server\r\n\r\n'.format(self.protocol,
											self.code,
											self.content_type,
											self.content_length,
											self.date)

	def __not_found(self):
		return 'HTTP/{} {}\r\n' \
               'Server: Server'.format(self.protocol, self.code)

	def build(self):
		if self.code == RESPONSE_CODES["OK"]:
			return self.__success().encode() #+ self.data
		if (self.code == RESPONSE_CODES[NOT_FOUND] 
			or self.code == RESPONSE_CODES[NOT_ALLOWED] 
			or self.code == RESPONSE_CODES[FORBIDDEN]):
			return self.__not_found().encode()


		




def parse_request(data, document_root = ""):
	# self.data = data.decode('UTF-8')
	print(data)
	request = Request()
	request.method = re.search(r'^\w+', data).group()
	request.protocol = re.findall(r'HTTP/([1-9.]+)', data)[0]
	# request.url = re.findall(r'(https?://[^\s?]+)', data)[0]
	# request.query = re.findall(r'[?&]([\w=]+)', rr)
	# request.query = {item.split("=")[0]: item.split("=")[1] for item in 
	# 	re.findall(r'[?&]([\w=]+)', rr)}
	# request.headers
	print (request.method, request.protocol, request.query, sep = "|")

	response = None
	request.url = "/" # УБРААААААААААААААААААААААТЬ
	file_url = None

	if request.error:
		response = Response(RESPONSE_CODES["NOT_ALLOWED"], request.protocol)
		# TODO написсать return

	else:
		protocol = request.protocol
		print (protocol)
		if request.url[-1:] == '/':
			file_url = request.url[1:] + 'index.html'
		else:
			file_url = request.url[1:]

		print(file_url)
		if False:
			q = 90
			print ("wwwwwwwwwwwwwwwwwwwwwwww")
		# if len(file_url.split('../')) > 1:
		# 	response = Response(RESPONSE_CODES["FORBIDDEN"], request.protocol)
		# 	self.file = None
			# TODO написсать return

		else:
			print ("qqqqqqqqqqqqqqq")
			print (os.path.join(document_root, "apple.jpg"))
			try:
				file = os.open(os.path.join(document_root, "apple.jpg"), os.O_RDONLY)
				flag = fcntl.fcntl(file, fcntl.F_GETFL)
				fcntl.fcntl(file, fcntl.F_SETFL, flag | os.O_NONBLOCK)
				print(file)
			except (FileNotFoundError, IsADirectoryError):
				if (request.url[-1:]) == '/':
					return Response(ResponseCode.FORBIDDEN, request.protocol).build()
				else:
					return Response(ResponseCode.NOT_FOUND, request.protocol).build()

			except OSError:
				print(request.url)
				return Response(ResponseCode.NOT_FOUND, request.protocol).build()
			content_type = None
			try:
				content_type = MIME_TYPES[re.findall(r'\.\w+', file_url)[0]]
			except KeyError:
				content_type = MIME_TYPES["default"]

			print(content_type)

			content_length = os.path.getsize(os.path.join(document_root, "apple.jpg"))

			print(content_length)
			response = Response(RESPONSE_CODES["OK"], request.protocol, content_type, content_length)

			if request.method == 'HEAD':
				file = None
	r = response.build()

	return r





















