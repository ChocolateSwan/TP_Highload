import datetime
from constants import RESPONSE_CODES, RESPONSE_OK, RESPONSE_FAIL

class Response:
	"""HTTP Response """
	def __init__(self, code, protocol="", content_type="", content_length=""):
		self.code = code
		self.protocol = protocol
		self.data = "data"
		self.content_type = content_type
		self.content_length = content_length
		self.date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

	def __success(self):
		return RESPONSE_OK.format(self.protocol,
											self.code,
											self.content_type,
											self.content_length,
											self.date)

	def __not_found(self):
		return RESPONSE_FAIL.format(self.protocol, self.code)

	def build(self):
		if self.code == RESPONSE_CODES["OK"]:
			return self.__success().encode() #+ self.data
		else:
			return self.__not_found().encode()