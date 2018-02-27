import urllib.parse
import datetime
import fcntl
import re
import os

from HTTP_request import Request
from constants import MIME_TYPES,\
						 RESPONSE_CODES,\
						  RESPONSE_OK,\
						   RESPONSE_FAIL,\
						    DATETIME_TEMPLATE,\
						     ALLOW_METHODS

def build_response(code, 
					protocol, 
					content_type  = '', 
					content_length = '') :
	if code == RESPONSE_CODES["OK"]:
		return RESPONSE_OK.format(protocol,
									code,
									content_type,
									content_length,
									datetime.datetime.utcnow().strftime(DATETIME_TEMPLATE)).encode()
	else:
		return RESPONSE_FAIL.format(protocol, 
									code).encode()


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
		request.url = urllib.parse.unquote(request.url)
	except IndexError:
		request.url = None
	# request.query = re.findall(r'[?&]([\w=]+)', rr)
	# request.query = {item.split("=")[0]: item.split("=")[1] for item in 
	# 	re.findall(r'[?&]([\w=]+)', rr)}
	# request.headers
	print (request.method, request.protocol, request.url, sep = "|") # убрать
	return request

def request_processing(data, document_root = ''):
	'''Обработка запроса, формирование ответа'''

	print(data)

	request = parse_request(data) 	

	protocol = request.protocol
	response = None
	file_url = None

	# Не тот метод
	if request.method not in ALLOW_METHODS:
		return build_response(RESPONSE_CODES["NOT_ALLOWED"], request.protocol), None

	# Много поднимаемся наверх по папкам
	if len(re.findall(r'\.\./', request.url)) > 1:
		return build_response(RESPONSE_CODES["FORBIDDEN"], request.protocol), None

	request.url += 'index.html' if request.url[-1] == '/' else ''
	file_url = request.url[1:]

	try:
		file = os.open(os.path.join(document_root, file_url), os.O_RDONLY)
		flag = fcntl.fcntl(file, fcntl.F_GETFL)
		fcntl.fcntl(file, fcntl.F_SETFL, flag | os.O_NONBLOCK)
	except (FileNotFoundError, IsADirectoryError):
		if 'index.html' in  request.url:
			return build_response(RESPONSE_CODES["FORBIDDEN"], request.protocol), None
		else:
			return build_response(RESPONSE_CODES["NOT_FOUND"], request.protocol), None 
	except OSError:
		return build_response(RESPONSE_CODES["NOT_FOUND"], request.protocol), None 

	try:
		content_type = MIME_TYPES[re.findall(r'\.(\w+)$', file_url)[0]]
	except KeyError:
		content_type = MIME_TYPES["default"]

	content_length = os.path.getsize(os.path.join(document_root, file_url))

	if request.method == 'HEAD':
		file = None

	return build_response(RESPONSE_CODES["OK"], protocol, content_type, content_length), file
