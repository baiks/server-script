import socket
import ssl

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname='localhost')
ssl_socket.connect(('localhost', 44447))
ssl_socket.send('4;0;1;28;0;5;3;0;'.encode())
received_data = ssl_socket.recv(1024)
print('Received data from server:', received_data.decode())
ssl_socket.close()
