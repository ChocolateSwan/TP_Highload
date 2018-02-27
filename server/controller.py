from constants import MIME_TYPES, RESPONSE_CODES, RESPONSE_OK, RESPONSE_FAIL, DATETIME_TEMPLATE
from HTTP_request import Request
from HTTP_response import Response
import urllib.parse
import datetime
import fcntl
import re
import os

document_root = "/"

def build_response(code, 
					protocol, 
					content_type, 
					content_length) :
	if code == RESPONSE_CODES["OK"]:
		return RESPONSE_OK.format(protocol,
									code,
									content_type,
									content_length,
									datetime.datetime.utcnow().strftime(DATETIME_TEMPLATE)).encode()
	else:
		return RESPONSE_FAIL.format(protocol, code).encode()


def parse_request(data):
	request = Request()
	try:
		request.method = re.findall(r'^(\w+)', data)[0]
	except IndexError:
		request.method = None
	try:
		request.protocol = re.findall(r'HTTP/([1-9.]+)', data)[0]
	except IndexError:
		request.protocol = None
	try:
		request.url = re.findall(r'([^\s?]+)', data)[1]
	except IndexError:
		request.url = None
	# request.query = re.findall(r'[?&]([\w=]+)', rr)
	# request.query = {item.split("=")[0]: item.split("=")[1] for item in 
	# 	re.findall(r'[?&]([\w=]+)', rr)}
	# request.headers
	print (request.method, request.protocol, request.url, sep = "|") # убрать
	return request

def request_processing(data, document_root = ""):
	print(data)
	request = parse_request(data)

	response = None
	file_url = None

	if request.method not in ['GET', 'HEAD']:
		response = Response(RESPONSE_CODES["NOT_ALLOWED"], request.protocol)
		return response.build(), None

	protocol = request.protocol
	print (protocol)


	request.url = urllib.parse.unquote(request.url)
	print(request.url)
	request.url += 'index.html' if request.url[-1] == '/' else ''
	file_url = request.url[1:]
	print(file_url)


	if len(re.findall(r'\.\./', file_url)) > 1:
		response = Response(RESPONSE_CODES["FORBIDDEN"], request.protocol)
		return response.build(), None


	try:
		file = os.open(os.path.join(document_root, file_url), os.O_RDONLY)
		flag = fcntl.fcntl(file, fcntl.F_GETFL)
		fcntl.fcntl(file, fcntl.F_SETFL, flag | os.O_NONBLOCK)
	except (FileNotFoundError, IsADirectoryError):
		if 'index.html' in  request.url:
			print (111111)
			return Response(RESPONSE_CODES["FORBIDDEN"], request.protocol).build(), None
		else:
			print (222222)
			return Response(RESPONSE_CODES["NOT_FOUND"], request.protocol).build(), None #RESPONSE_CODES["NOT_FOUND"]

	except OSError:
		print (33333)
		return Response(RESPONSE_CODES["NOT_FOUND"], request.protocol).build(), None 
	try:
		print ("heloooooooooooo", file_url)
		content_type = MIME_TYPES[re.findall(r'\.(\w+)$', file_url)[0]]
	except KeyError:
		print ("key error")
		content_type = MIME_TYPES["default"]

	print(content_type)

	content_length = os.path.getsize(os.path.join(document_root, file_url))

	print(content_length)
	response = Response(RESPONSE_CODES["OK"], request.protocol, content_type, content_length)

	if request.method == 'HEAD':
		file = None
	r = response.build()

	return r, file
