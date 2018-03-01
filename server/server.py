import os
import socket
import select

from controller import request_processing

PORT = 8902
DOCUMENT_ROOT =  ''

print("Starting server on port {}, document root: {}".format(PORT, DOCUMENT_ROOT))


EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', PORT))
serversocket.listen(1)
serversocket.setblocking(0)

for i in range(1):
	pid = os.fork()
	if pid == 0:
		break

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

try:
	print ("Start thread")
	connections = {}; requests = {}; responses = {}; files = {}
	while True:
		print ("Я работаю", pid)
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
				except socket.error:
					pass

			elif event & select.EPOLLIN:
				print ("Inn: pid = ", pid)
				try:
					while True:
						print ("Получаем данные ...")
						buffer = b""
						buffer = connections[fileno].recv(1024)
						if not buffer:
							break;
						requests[fileno] += buffer
				except socket.error:
					pass

				if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
					epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
					print('-'*40 + '\n' + requests[fileno].decode('UTF-8')[:-2])

				resp, file = request_processing(requests[fileno].decode(), '') # 'UTF-8'
				print('pid = ', pid, ' ', resp, file)

				buff = b""
				file_content = b""

				if file:
					while True:
						print ("Получаем файл ...")
						file_content += buff
						buff = os.read(file, 1024)
						if not buff:
							break

				responses[fileno] = resp + file_content

			elif event & select.EPOLLOUT:

				print ('Out: pid = ', pid)

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
	print ('KeyboardInterrupt =(') 

finally:
	print ("oops")
	epoll.unregister(serversocket.fileno())
	epoll.close()
	serversocket.close()







# 2 - 5769
# 3 - 3081
# 4 - 








