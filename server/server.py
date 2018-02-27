import socket
import select
import os
from controller import request_processing

def handler():
	if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
		epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
		print('-'*40 + '\n' + requests[fileno].decode()[:-2])

PORT = 8902

print("Starting server on port {}, document root: не важно пока".format(PORT))


EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', PORT))
serversocket.listen(1)
serversocket.setblocking(0)



for i in range(4-3):
	pid = os.fork()
	if pid == 0:
		break

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

try:
	print ("qqqqqqqqqqqqqqqqqqqq")
	connections = {}; requests = {}; responses = {}; files = {}
	while True:
		# print ("pid", pid)
		events = epoll.poll(1)
		for fileno, event in events:
			if fileno == serversocket.fileno():
				try:
					while True:
						connection, address = serversocket.accept()
						connection.setblocking(0)
						epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
						connections[connection.fileno()] = connection
						requests[connection.fileno()] = b''
						responses[connection.fileno()] = response
				except socket.error:
					pass
			elif event & select.EPOLLIN:
				print ("inn pid", pid)
				try:
					while True:
						print ("что не так")
						buffer = b""
						buffer = connections[fileno].recv(1024)
						if not buffer:
							break;
						requests[fileno] += buffer
						print(requests[fileno].decode())
				except socket.error:
					print ("что не так2")
					pass
				print ("что не так1")
				if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
					epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
					print('-'*40 + '\n' + requests[fileno].decode('UTF-8')[:-2])
				print ('#'*40)
				r, file = request_processing(requests[fileno].decode(), '') # 'UTF-8'
				# print (file)
				#buffer = os.read(file, FILE_BLOCK_SIZE) #&&&&&&&&&&&&&
				#11111111111111111111111111111111111111111
				buff = b""
				file_content = b""
				if file:
					while True:
						file_content += buff
						buff = os.read(file, 1024)
						if not buff:
							break
				#111111111111111111111111111111111111111111
				# print (file_content)
				responses[fileno] = r + file_content
				print (r)
			elif event & select.EPOLLOUT:
				print ("out pid", pid)
				try:
					while len(responses[fileno]) > 0:
						byteswritten = connections[fileno].send(responses[fileno])
						responses[fileno] = responses[fileno][byteswritten:]
				except socket.error:
					pass
				if len(responses[fileno]) == 0:
					epoll.modify(fileno, select.EPOLLET)
					connections[fileno].shutdown(socket.SHUT_RDWR)
			elif event & select.EPOLLHUP:
				epoll.unregister(fileno)
				connections[fileno].close()
				del connections[fileno]
except KeyboardInterrupt:
	print ("НИЧОССИИ ТЫ") 
finally:
	epoll.unregister(serversocket.fileno())
	epoll.close()
	serversocket.close()
















